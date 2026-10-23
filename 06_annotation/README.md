# 06_annotation: anotación con Prokka

## Propósito
Anotación estructural y funcional del ensamblado filtrado (`contigs_cov100.fasta`, 74 contigs, 2 790 840 pb).

## Herramientas
Prokka 1.14.6 (Galaxy Australia, 1.14.6+galaxy2), corrida del 20/10/2026. Parámetros y línea de comando en
`scripts/galaxy/prokka_galaxy.md` (`--genus Staphylococcus --species aureus --strain B378 --kingdom Bacteria --compliant`, 8 CPU).

## Archivos (en `prokka/`)
| Archivo | Contenido |
|---|---|
| `prokka_B378_gff.gff3` | Anotación GFF3 con los nombres de contig de Prokka (`BLAGNNMM_n`) |
| `B378_prokka_nodenames.gff3` | GFF3 con los contigs renombrados a `NODE_n_length_L_cov_C` (para IGV) [VERIFICAR: sin script de origen] |
| `prokka_B378_gbk.genbank`, `_faa.fasta`, `_ffn.fasta`, `_fna.fasta`, `_fsa.fasta` | GenBank, proteínas, genes (nt), contigs y secuencias para envío |
| `prokka_B378_tsv.tabular` | Tabla por CDS: `locus_tag ftype length_bp gene EC_number COG product` |
| `prokka_B378_tbl.txt`, `prokka_B378_err.txt` | Tabla de rasgos y mensajes de validación |
| `prokka_B378_txt.txt`, `prokka_B378_log.txt` | Resumen y registro de la corrida |

Resumen (`prokka_B378_txt.txt`): CDS 2576, genes 2636, ARNr 4, ARNt 55, ARNtm 1.
Tamaño: 21 MB.

## Excluido por .gitignore
Nada. Se regenera con Prokka sobre `03_assembly/S1_full/contigs_cov100.fasta` (ver `scripts/galaxy/prokka_galaxy.md`).

## Correspondencia con el informe
Sección 2.6 (anotación); mapa de genes de multicopia y región *ebh* (`scripts/analisis/fig26_prokka_multicopia_ebh.py`)
[VERIFICAR: figura y tabla].
