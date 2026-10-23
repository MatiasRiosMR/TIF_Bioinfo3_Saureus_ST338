# 08_genes_mge: virulencia, resistencia y elementos móviles

## Propósito
Búsqueda de genes de virulencia y resistencia, tBLASTn de genes del artículo de referencia, BLAST de contigs de multicopia,
profagos y estimación del número de copias.

## Herramientas y versiones
ABRicate (bases CARD y VFDB), BLAST+ (tBLASTn; BLASTn web de NCBI), PHASTEST (web). Versión confirmada solo para BLAST 2.16.0 (`envs/quast_env.yml`). Entrada de ABRicate: `contigs_cov100.fasta`.

## Archivos
| Archivo | Contenido |
|---|---|
| `abricate_card_S1.tsv` | CARD; 14 hits. Columnas ABRicate: `#FILE SEQUENCE START END STRAND GENE COVERAGE COVERAGE_MAP GAPS %COVERAGE %IDENTITY DATABASE ACCESSION PRODUCT RESISTANCE` |
| `abricate_vfdb_S1.tsv` | VFDB; 75 hits, mismas columnas |
| `tblastn_genes_S1.tsv` | tBLASTn de `proteinas_genes_chen2024.fasta` contra el ensamblado; sin encabezado, 25 columnas (las 12 primeras son el formato tabular de BLAST; el resto) |
| `proteinas_genes_chen2024.fasta` | Proteínas consulta (UniProt) |
| `copias_estimadas_S1.tsv` | `contig largo_pb cov_kmer profundidad_media copias_estimadas clase` (11 contigs); lo genera `fig28_copias_estimadas.py` |
| `blast_ncbi/blast_multicopia_S1_hits_unificado.csv` | Hits BLASTn de NCBI; columnas `query subject pct_identity aln_len mismatches gap_opens q_start q_end s_start s_end evalue bitscore` |
| `blast_ncbi/blast_multicopia_S1_resumen.tsv` | Resumen por contig (5 filas): registros, hits casi completos, mejor hit |
| `blast_ncbi/raw/` | Salidas crudas de NCBI (alineamiento y hits del lote 1) |
| `phastest/` | `summary.txt`, `detail.txt`, `phage_regions.fna`, `predicted_*.json` (PHASTEST) |

Tamaño: ≈1,1 MB versionado (más 0,7 MB de la base BLAST local).

## Excluido por .gitignore
`blastdb_contigs_cov100/` (base `makeblastdb` de Galaxy). Se regenera con `makeblastdb -dbtype nucl -in 03_assembly/S1_full/contigs_cov100.fasta`.

## Notas
`blast_resumen_tramos.py` escribe otro encabezado que el de `blast_multicopia_S1_resumen.tsv`; este último no sale de ese script tal como está.

## Correspondencia con el informe
Sección 2.7 (resultados de virulencia, resistencia, multicopia, profagos) y Figuras de multicopia.
