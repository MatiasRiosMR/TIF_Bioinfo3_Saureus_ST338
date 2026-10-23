# scripts: comandos del TP Final de Bioinformática 3

Aislamiento B378 (*S. aureus* ST338, SRR26803856), ensamblado de novo y caracterización frente a MRSA252 (BX571856.1).
Comandos del Anexo C del informe, numerados en orden de ejecución.

## Uso
1. Activar el entorno `tif_bioinfo3` (`envs/tif_bioinfo3.yml`); QUAST usa `quast_env`, que el script activa solo.
2. Ejecutar desde cualquier carpeta: `PROJ=<raíz del proyecto> bash scripts/07_spades_completo.sh` (por defecto `PROJ=~/tp_final`).

## Scripts ejecutados (orden 00 → 11)
| Script | Sección | Herramienta | Qué hace |
|---|---|---|---|
| `00_crear_carpetas.sh` | 2.0.2 | `mkdir` | Crea la estructura de carpetas |
| `01_descarga_lecturas_ncbi.sh` | 2.0.4 | sra-tools 3.4.1, pigz | `prefetch`, `vdb-validate`, `fasterq-dump`, compresión a `00_raw/` |
| `02_descarga_referencia.sh` | 2.0.5 | wget, SAMtools | Descarga y verifica MRSA252 (2 902 619 pb) |
| `03_qc_lecturas_crudas.sh` | 2.1 | FastQC, MultiQC | QC de lecturas crudas (comando reconstruido: confirmar) |
| `04_recorte_trimmomatic.sh` | 2.2.1 | Trimmomatic 0.41 | `ILLUMINACLIP:TruSeq3-PE-2.fa:2:30:10:2:True LEADING:3 TRAILING:3 SLIDINGWINDOW:4:20 MINLEN:50` |
| `05_qc_posterior_recorte.sh` | 2.2.2 | FastQC, MultiQC | QC posterior y comparativo |
| `06_spades_prueba_5pct.sh` | 2.3.1 | seqtk, SPAdes | Prueba con el 5 % de los pares |
| `07_spades_completo.sh` | 2.3.2 | SPAdes 4.3.0 | Ensamblado completo, `--isolate` |
| `08_metricas_ensamblado.sh` | 2.3.2 | awk | Contigs, largo, N50, grupos por cobertura de k-mers, GC |
| `09_quast_completo.sh` | 2.4.1 | QUAST 5.3.0 | QUAST contra MRSA252 → `04_assembly_qc/quast_full/` |
| `10_cobertura_real_bowtie2.sh` | 2.4.1 | Bowtie2 2.5.5, SAMtools 1.24 | Profundidad real por contig → `04_assembly_qc/S1_coverage.tsv` |
| `11_filtrar_cov100.sh` | 2.4 | awk | Filtro ≥500 pb y k-mers ≥100 → `contigs_cov100.fasta` (74 contigs) |

Numeración de secciones: la de los comentarios de cada script.

## Subcarpetas
| Carpeta | Contenido |
|---|---|
| `analisis/` | Figuras y tablas derivadas (ver `analisis/README.md`) |
| `envs/` | `exportar_entornos.sh` (ver `envs/README.md`) |
| `galaxy/` | Registro de Prokka 1.14.6, BUSCO 6.1.0 y subida de archivos a Galaxy Australia (`.md`) |
| `planificados/` | `12_comparacion_referencia_igv.sh` (Bowtie2 a MRSA252, bigWig, QUAST del filtrado) y `13_submuestreos_100x_30x.sh` (≈100× y ≈30×, iso y car, QUAST) |

## Estado de los scripts planificados
Ambos conservan la cabecera "PLANIFICADO, todavía no se ejecutó", pero existen sus salidas (`09_igv/S1_ref.bam`, `09_igv/S1_ref.bw`,
`04_assembly_qc/quast_cov100/`, `10_depth/S1_*_{iso,car}/`, `10_depth/quast_comp/`). El script 13 calcula las fracciones con 762,5×,
mientras la mediana sobre MRSA252 es 702× (`S1_ref.depth.tsv`).

## No incluido
- MLST, ABRicate, BLAST+, PHASTEST y D-Genies: hay resultados en `07_typing/`, `08_genes_mge/` y `04_assembly_qc/dgenies_cov100/`, pero no scripts.
- La descarga inicial desde ENA (descartada por calidades simplificadas; ver el registro de decisiones del informe).
- Los scripts usan `PROJ`, pero `spades.log`, `params.txt` y `09_igv/cargar_igv.batch` conservan rutas absolutas de la máquina de origen.
