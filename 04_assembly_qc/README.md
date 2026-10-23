# 04_assembly_qc: calidad del ensamblado y comparación con MRSA252

## Propósito
Métricas del ensamblado completo y filtrado, completitud génica, comparación con MRSA252 y tablas de apoyo del análisis.

## Herramientas
QUAST 5.3.0 (`quast_env`), BUSCO 6.1.0 en Galaxy Australia (`bacillales_odb12`, `prok_genome_min`, Prodigal),
D-Genies (minimap2, web), SAMtools 1.24 / Bowtie2 2.5.5 (cobertura), Python y R (`scripts/analisis/`).

## Archivos
| Ruta | Origen | Contenido |
|---|---|---|
| `quast_full/` | `scripts/09_quast_completo.sh` | QUAST de `contigs.fasta` vs MRSA252 (`report.tsv/html/pdf`, gráficos, alineamientos) |
| `quast_cov100/` | `scripts/planificados/12_comparacion_referencia_igv.sh` | QUAST de `contigs_cov100.fasta` vs MRSA252 |
| `busco_full/` | Galaxy (`scripts/galaxy/busco_galaxy.md`) | `busco_short_summary.txt`, `busco_full_table.tsv` |
| `dgenies_cov100/` | D-Genies (web) | `map_contigs_cov100_to_MRSA252.paf` (minimap2, columnas PAF + tags) y `.png` |
| `S1_coverage.tsv` | `scripts/10_cobertura_real_bowtie2.sh` | `samtools coverage`: `#rname startpos endpos numreads covbases coverage meandepth meanbaseq meanmapq`; una fila por contig (17 258) |
| `contigs_filtrados_atipicos.tsv` | `analisis_contigs_gc_cobertura.R` | `contig largo cov gc copias z_gc atipico`; 74 contigs filtrados |
| `regiones_sin_correspondencia_MRSA252.tsv` | `regiones_sin_correspondencia_MRSA252.py` | `contig inicio fin largo_pb`; 6 tramos sin correspondencia |
| `gc_tramos_B378.tsv` | `fig29_contexto_genomico.py` | `n contig inicio fin largo_pb GC_tramo GC_medio_ventanas p_empirico` |

Tamaño: 21 MB (`quast_full` 9,8 MB, `quast_cov100` 9,1 MB, `S1_coverage.tsv` 1,1 MB).

## Excluido por .gitignore
`**/icarus_viewers/`. Se regenera repitiendo QUAST (comandos en los scripts citados).

## Resultados clave
Completo: 17 258 contigs, N50 43 072, fracción del genoma 86,236 %. Filtrado: 74 contigs, N50 70 746, 85,415 %, 47 misassemblies.
BUSCO: C 93,9 % (403/429), F 1,6 %, M 4,4 %.

## Correspondencia con el informe
Secciones 2.4 y 2.5: tablas de QUAST y BUSCO, mapa de contigs (D-Genies), regiones sin correspondencia [VERIFICAR: tablas y figuras].
Los comandos de D-Genies y de `regiones_sin_correspondencia_MRSA252.py` no figuran en `scripts/00-11` [VERIFICAR].
