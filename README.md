# Ensamblado de novo y caracterización genómica de *Staphylococcus aureus* B378 (ST338, CC59)

**Universidad Nacional de Entre Ríos (UNER) · Facultad de Ingeniería (FIUNER)**

Licenciatura en Bioinformática · Bioinformática 3

*Trabajo Práctico Final, Modalidad C: ensamblado de novo y caracterización genómica*

| | |
|---|---|
| Autor | Matías Rios (matias.rios@ingenieria.uner.edu.ar, GitHub: [MatiasRiosMR](https://github.com/MatiasRiosMR)) |
| Docentes | Dra. Ileana Tossolini y Dr. Juan Cabrera |
| Año | 2026 |
| Entrega | 05/11/2026, aula virtual |
| Repositorio | https://github.com/MatiasRiosMR/TIF_Bioinfo3_Saureus_ST338 |

## Contenido

1. [Resumen](#resumen)
2. [Pregunta y objetivos](#pregunta-y-objetivos)
3. [Resultados principales](#resultados-principales)
4. [Datos de entrada](#datos-de-entrada)
5. [Estructura del repositorio](#estructura-del-repositorio)
6. [Flujo de trabajo y orden de ejecución](#flujo-de-trabajo-y-orden-de-ejecución)
7. [Entorno de software](#entorno-de-software)
8. [Reproducción de figuras y tablas](#reproducción-de-figuras-y-tablas)
9. [Limitaciones](#limitaciones)
10. [Cómo citar](#cómo-citar) y [Contacto](#contacto)

## Resumen

Se ensambló de novo el aislamiento *S. aureus* B378 (ST338, complejo clonal CC59) a partir de lecturas Illumina pareadas
(SRR26803856, BioProject PRJNA1039716) y se lo caracterizó frente al genoma de referencia MRSA252 (BX571856.1, 2 902 619 pb).
El análisis abarca control de calidad, ensamblado, evaluación de calidad, anotación, tipificación por MLST, búsqueda de genes de
virulencia, resistencia y elementos genéticos móviles, mapeo contra la referencia y análisis de cobertura. Además se evaluó el
efecto de la profundidad de secuenciación (submuestreos de ≈100× y ≈30×) y del modo de SPAdes (`--isolate` y `--careful`).

## Pregunta y objetivos

**Pregunta.** ¿Qué porción del genoma de B378 se recupera con un ensamblado de novo de lecturas cortas y qué diferencias
estructurales y de contenido génico presenta frente a MRSA252?

**Objetivos.**
1. Ensamblar el genoma y evaluar la calidad del ensamblado.
2. Anotar el genoma y tipificarlo por MLST.
3. Buscar genes de virulencia, resistencia y elementos genéticos móviles.
4. Localizar regiones sin cobertura y de cobertura alta al mapear las lecturas contra MRSA252.
5. Medir el efecto de la profundidad de secuenciación y del modo de SPAdes sobre el ensamblado.

## Resultados principales

Cada cifra proviene del archivo indicado.

| Resultado | Valor | Fuente |
|---|---|---|
| Pares de lecturas: totales / conservados tras el recorte | 8 416 403 / 7 781 558 (92,46 %) | `logs/trimmomatic_S1.log` |
| Ensamblado completo (SPAdes 4.3.0, `--isolate`) | 17 258 contigs, 8 388 158 pb | `04_assembly_qc/quast_full/report.tsv` |
| Tiempo y memoria del ensamblado completo | 22 min 39 s; 4,6 GB | `logs/spades_full.time` |
| Ensamblado filtrado (≥500 pb y cobertura de k-mers ≥100) | 74 contigs, 2 790 840 pb, N50 70 746, GC 32,76 % | `04_assembly_qc/quast_cov100/report.tsv` |
| Fracción de MRSA252 cubierta (filtrado) | 85,415 % | `04_assembly_qc/quast_cov100/report.tsv` |
| BUSCO (`bacillales_odb12`, n = 429) | completos 93,9 %; fragmentados 1,6 %; ausentes 4,4 % | `04_assembly_qc/busco_full/busco_short_summary.txt` |
| Tipo de secuencia (MLST) | ST338 (*saureus*) | `07_typing/mlst_S1.tsv` |
| Alineamiento de lecturas: ensamblado / MRSA252 | 96,75 % / 83,68 % | `logs/bt2_asm.log`, `logs/bt2_ref.log` |
| Mediana de profundidad sobre MRSA252 | 702× | `09_igv/S1_ref.depth.tsv` (local, no versionado) |
| Regiones de MRSA252 sin cobertura (≥1 kb) | 50 (152 914 pb en total) | `09_igv/regiones_cov0.bed` |
| *mecA* | NODE_60 (100 % de cobertura, 99,85 % de identidad) | `08_genes_mge/abricate_card_S1.tsv` |
| *blaZ* | NODE_45, posición 14 287–15 132 | `06_annotation/prokka/B378_prokka_nodenames.gff3` |
| *ebh* | Anotado como dos CDS (`ebh_1`, `ebh_2`) en NODE_15 | `06_annotation/prokka/B378_prokka_nodenames.gff3` |

Tablas de detalle: [`04_assembly_qc/`](04_assembly_qc/README.md), [`08_genes_mge/`](08_genes_mge/README.md) y
[`10_depth/`](10_depth/README.md). Capturas de IGV: [`09_igv/capturas_finales/`](09_igv/capturas_finales/README.md).

## Datos de entrada

Los datos crudos no se incluyen en el repositorio.

| Dato | Accesión | Obtención |
|---|---|---|
| Lecturas Illumina pareadas | SRR26803856 (PRJNA1039716) | `scripts/01_descarga_lecturas_ncbi.sh`: `prefetch`, `vdb-validate`, `fasterq-dump --split-files` y `pigz` |
| Genoma de referencia MRSA252 | BX571856.1 | `scripts/02_descarga_referencia.sh` (ENA); el FASTA sí se versiona en `05_reference/` |

Excluido por `.gitignore`: `00_raw/`, `00_raw_ncbi/` y `02_trim/` (≈5 GB); BAM/BAI e índices Bowtie2 (`*.bt2`); intermedios de
SPAdes (`K*/`, `corrected/`, `scaffolds.*`, grafos); `09_igv/pistas/` y `09_igv/S1_ref.depth.tsv`; `10_depth/test/`; lecturas
submuestreadas (`*.fq.gz`); `icarus_viewers/` y la base BLAST local. Cada README de carpeta indica cómo regenerarlos.

## Estructura del repositorio

Cada carpeta numerada tiene su propio `README.md`. El árbol completo y la tabla archivo → origen → informe están en
[`docs/ESTRUCTURA.md`](docs/ESTRUCTURA.md).

```
.
├── 01_qc/              FastQC y MultiQC de lecturas crudas (raw/) y recortadas (trim/)
├── 03_assembly/        Ensamblado SPAdes (S1_full/): contigs.fasta y contigs_cov100.fasta
├── 04_assembly_qc/     QUAST (completo y filtrado), BUSCO, D-Genies, cobertura por contig, tablas de análisis
├── 05_reference/       MRSA252.fasta y su índice .fai
├── 06_annotation/      Anotación Prokka (Galaxy) del ensamblado filtrado
├── 07_typing/          MLST
├── 08_genes_mge/       ABRicate (CARD, VFDB), tBLASTn, BLAST de NCBI, PHASTEST, copias estimadas
├── 09_igv/             Mapeo a MRSA252, bigWig, BED de regiones, script de IGV y capturas finales
├── 10_depth/           Submuestreos 100× y 30× (iso y car), QUAST comparativo, métricas
├── envs/               YAML de los entornos conda (tif_bioinfo3, quast_env)
├── figuras/            Figuras generadas con scripts/analisis/
├── logs/               Registros de descarga, recorte, SPAdes, Bowtie2 y lista de paquetes
├── docs/               Estructura detallada
└── scripts/            00-11 (ejecutados), analisis/, envs/, galaxy/, planificados/
```

## Flujo de trabajo y orden de ejecución

```
SRA (SRR26803856) → FastQC/MultiQC → Trimmomatic → FastQC/MultiQC
   → SPAdes → QUAST / BUSCO → filtro (≥500 pb, k-mers ≥100) → Prokka · MLST · ABRicate · BLAST · PHASTEST
   → Bowtie2 + SAMtools + deepTools (contra MRSA252) → IGV
   → submuestreos 100× / 30× (--isolate y --careful) → QUAST comparativo
```

1. `scripts/00_crear_carpetas.sh` a `scripts/11_filtrar_cov100.sh`, en ese orden. Detalle en [scripts/README.md](scripts/README.md).
2. Prokka y BUSCO se ejecutaron en Galaxy Australia; sus parámetros están en `scripts/galaxy/`.
3. Mapeo contra MRSA252 y submuestreos: `scripts/planificados/12_comparacion_referencia_igv.sh` y `13_submuestreos_100x_30x.sh`.
4. Figuras y tablas derivadas: `scripts/analisis/`.

Los scripts aceptan la variable `PROJ` con la raíz del proyecto (por defecto `~/tp_final`):
`PROJ=/ruta/al/proyecto bash scripts/07_spades_completo.sh`.

## Entorno de software

| Entorno | Archivo | Herramientas |
|---|---|---|
| `tif_bioinfo3` | `envs/tif_bioinfo3.yml` | FastQC 0.12.1, MultiQC 1.35, Trimmomatic 0.41, SPAdes 4.3.0, seqtk 1.5, Bowtie2 2.5.5, SAMtools 1.24, minimap2 2.31, sra-tools 3.4.1, pigz 2.8, Python 3.14.7, matplotlib 3.11.1, numpy 2.5.2, R 4.4.3 |
| `quast_env` | `envs/quast_env.yml` | QUAST 5.3.0, BLAST 2.16.0, bedtools 2.31.1, Python 3.9.23 |
| Galaxy Australia | `scripts/galaxy/` | Prokka 1.14.6, BUSCO 6.1.0 (`bacillales_odb12`) |

Recreación: `conda env create -f envs/tif_bioinfo3.yml` y `conda env create -f envs/quast_env.yml`.
La lista completa de paquetes está en `logs/conda_list_tif_bioinfo3.txt`.

## Reproducción de figuras y tablas

Desde la raíz del repositorio y con el entorno `tif_bioinfo3` activo. Entradas y salidas en las rutas del repositorio.

```bash
# Contigs: largo, cobertura de k-mers, profundidad real, GC
python3 scripts/analisis/fig20_largo_vs_cobertura.py 03_assembly/S1_full/contigs.fasta figuras/fig20_largo_vs_cobertura.png
python3 scripts/analisis/fig23_profundidad_real.py 03_assembly/S1_full/contigs.fasta 04_assembly_qc/S1_coverage.tsv figuras/fig23_profundidad_real.png
Rscript scripts/analisis/analisis_contigs_gc_cobertura.R 03_assembly/S1_full/contigs.fasta figuras/analisis_gc

# Comparación con MRSA252
python3 scripts/analisis/regiones_sin_correspondencia_MRSA252.py 04_assembly_qc/dgenies_cov100/map_contigs_cov100_to_MRSA252.paf 03_assembly/S1_full/contigs.fasta 04_assembly_qc/regiones_sin_correspondencia_MRSA252.tsv
python3 scripts/analisis/fig24_mapa_contigs.py 04_assembly_qc/dgenies_cov100/map_contigs_cov100_to_MRSA252.paf figuras/fig24_mapa_contigs.png
python3 scripts/analisis/fig29_contexto_genomico.py 04_assembly_qc/dgenies_cov100/map_contigs_cov100_to_MRSA252.paf 03_assembly/S1_full/contigs.fasta 04_assembly_qc/regiones_sin_correspondencia_MRSA252.tsv figuras/fig29A_mapa.png figuras/fig29B_gc.png 04_assembly_qc/gc_tramos_B378.tsv

# Cobertura sobre MRSA252
samtools depth -a 09_igv/S1_ref.bam > 09_igv/S1_ref.depth.tsv
python3 scripts/analisis/fig25_cobertura_MRSA252.py 09_igv/S1_ref.depth.tsv 09_igv/fig25_cobertura.png

# Multicopia y genes
python3 scripts/analisis/fig26_prokka_multicopia_ebh.py 06_annotation/prokka/prokka_B378_gff.gff3 03_assembly/S1_full/contigs_cov100.fasta figuras/fig26_prokka_multicopia_ebh.png
python3 scripts/analisis/fig27_blast_multicopia.py figuras/fig27_blast_multicopia.png 08_genes_mge/blast_ncbi/blast_multicopia_S1_hits_unificado.csv
python3 scripts/analisis/fig28_copias_estimadas.py 04_assembly_qc/S1_coverage.tsv figuras/fig28_copias_estimadas.png 08_genes_mge/copias_estimadas_S1.tsv

# Profundidad de secuenciación y modo de SPAdes
python3 scripts/analisis/fig30_profundidad_vs_ensamblado.py 10_depth/quast_comp/report.tsv figuras/fig30.png 10_depth/metricas_submuestreos.tsv
Rscript scripts/analisis/fig23_informe.R 10_depth/metricas_submuestreos.tsv figuras/fig23_informe.png
```

Las capturas de IGV (Figuras 16–21, 26 y 27) se tomaron manualmente; `09_igv/cargar_igv.batch` carga las pistas y las regiones.
La correspondencia entre archivos, scripts e informe está en [`docs/ESTRUCTURA.md`](docs/ESTRUCTURA.md) y en [`figuras/README.md`](figuras/README.md).

## Limitaciones

- Con lecturas cortas, las repeticiones y los elementos de múltiples copias (ARNr, secuencias de inserción, fagos) quedan colapsados o fragmentados.
- Solo el 85,4 % de MRSA252 tiene correspondencia en el ensamblado filtrado; el filtro por cobertura de k-mers descarta contigs cortos.
- Prokka, BUSCO, PHASTEST y D-Genies se ejecutaron en servicios web; sus parámetros y versiones dependen de los registros guardados.
- La comparación se hizo contra una única referencia (MRSA252).
- Las lecturas y los alineamientos no están en el repositorio y deben regenerarse.

## Cómo citar

Rios, M. (2026). *Ensamblado de novo y caracterización genómica de Staphylococcus aureus B378 (ST338)*. Trabajo Práctico Final,
Bioinformática 3, Licenciatura en Bioinformática, FIUNER-UNER. https://github.com/MatiasRiosMR/TIF_Bioinfo3_Saureus_ST338

## Contacto

Matías Rios, matias.rios@ingenieria.uner.edu.ar, GitHub: [MatiasRiosMR](https://github.com/MatiasRiosMR)
