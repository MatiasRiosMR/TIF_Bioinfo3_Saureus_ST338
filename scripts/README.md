# Scripts y comandos del TP Final de Bioinformática 3

Aislamiento **B378** (*Staphylococcus aureus* ST338, run SRR26803856), ensamblado de novo y caracterización frente a MRSA252 (BX571856.1).
Contenido del Anexo C del informe. Los comandos son los del informe, ordenados por etapa y numerados en el orden de ejecución.

## Cómo usarlo

1. Copiar `scripts/`, `analisis/`, `galaxy/` y `envs/` a la carpeta del proyecto (`~/tp_final`).
2. Activar el entorno `tif_bioinfo3` (QUAST usa `quast_env`; el script lo activa solo).
3. Ejecutar cada script desde cualquier carpeta: `PROJ=~/tp_final bash scripts/07_spades_completo.sh`.
   Si no se define `PROJ`, se usa `~/tp_final`.

## Scripts ejecutados (computadora personal)

| Script | Sección | Qué hace |
|---|---|---|
| `00_crear_carpetas.sh` | 2.0.2 | Crea la estructura de carpetas |
| `01_descarga_lecturas_ncbi.sh` | 2.0.4 | Descarga, valida (vdb-validate), convierte (fasterq-dump) y comprime el run |
| `02_descarga_referencia.sh` | 2.0.5 | Descarga y verifica MRSA252 |
| `03_qc_lecturas_crudas.sh` | 2.1 | FastQC y MultiQC de las lecturas crudas (comando reconstruido: confirmar) |
| `04_recorte_trimmomatic.sh` | 2.2.1 | Recorte de adaptadores y bases de baja calidad |
| `05_qc_posterior_recorte.sh` | 2.2.2 | FastQC y MultiQC antes y después del recorte |
| `06_spades_prueba_5pct.sh` | 2.3.1 | Submuestreo del 5 % y ensamblado de prueba |
| `07_spades_completo.sh` | 2.3.2 | Ensamblado con la cobertura completa |
| `08_metricas_ensamblado.sh` | 2.3.2 | Contigs, largo total, N50 y grupos por cobertura de k-mers |
| `09_quast_completo.sh` | 2.4.1 | QUAST contra MRSA252 |
| `10_cobertura_real_bowtie2.sh` | 2.4.1 | Profundidad real por contig (Bowtie2 y SAMtools) |
| `11_filtrar_cov100.sh` | 2.4 | FASTA filtrado (74 contigs con cobertura de k-mers ≥ 100) |

## Análisis y gráficos (`analisis/`)

| Script | Figura | Entrada |
|---|---|---|
| `fig20_largo_vs_cobertura.py` | Figura 20 | `contigs.fasta` |
| `fig23_profundidad_real.py` | Figura 23 | `contigs.fasta` y `S1_coverage.tsv` (de `10_cobertura_real_bowtie2.sh`) |

Son reconstrucciones de los scripts con los que se hicieron las figuras (requieren Python con numpy, pandas y matplotlib).

## Pasos en Galaxy Australia (`galaxy/`)

Prokka y BUSCO se ejecutaron en Galaxy; sus parámetros, versiones y comandos quedaron registrados en `galaxy/`.
MLST, ABRicate, BLAST+ y PHASTEST (Sección 2.7) todavía no se ejecutaron.

## Planificados, todavía no ejecutados (`scripts/planificados/`)

| Script | Sección | Qué hace |
|---|---|---|
| `12_comparacion_referencia_igv.sh` | 2.5 y 2.8 | Alineamiento contra MRSA252, bigWig para IGV, índice del ensamblado filtrado y QUAST del filtrado |
| `13_submuestreos_100x_30x.sh` | 2.9 | Submuestreos (0,1311 y 0,0393), ensamblados con SPAdes `--isolate` y `--careful`, y QUAST |
| `../analisis/grafico_n50_planificado.R` | 2.9 | Gráfico de N50 |

## Entorno (`envs/`)

`exportar_entornos.sh` guarda los YAML y las listas de paquetes (Sección 3.2).

## Lo que este paquete no incluye

- La descarga inicial desde ENA (descartada por calidades simplificadas; ver Sección 4 del informe).
- Los comandos de los análisis que todavía no se hicieron (Sección 2.7 en adelante, salvo lo planificado).
