# Ensamblado de novo y caracterización genómica de *Staphylococcus aureus* B378 (ST338, CC59)

**Universidad Nacional de Entre Ríos (UNER), Facultad de Ingeniería (FIUNER)**
Licenciatura en Bioinformática, asignatura Bioinformática 3
Trabajo Práctico Final, Modalidad C (ensamblado de novo y caracterización genómica)

| | |
|---|---|
| Autor | Matías Rios, matias.rios@ingenieria.uner.edu.ar, GitHub: MatiasRiosMR |
| Docentes | Dra. Ileana Tossolini y Dr. Juan Cabrera |
| Año | 2026 |
| Fecha de entrega | 05/11/2026 (aula virtual) |
| Repositorio | https://github.com/MatiasRiosMR/TIF_Bioinfo3_Saureus_ST338.git |

## Resumen

Se ensambló de novo el aislamiento *S. aureus* B378 (ST338, complejo clonal CC59) a partir de lecturas Illumina pareadas
(SRR26803856, BioProject PRJNA1039716) y se lo caracterizó frente al genoma de referencia MRSA252 (BX571856.1, 2 902 619 pb).
Pipeline: FastQC/MultiQC → Trimmomatic → SPAdes → QUAST/BUSCO → Prokka → ABRicate/BLAST (virulencia, resistencia, elementos
móviles) → PHASTEST → mapeo y cobertura (Bowtie2, SAMtools, deepTools) → IGV. Se evaluó además el efecto de la profundidad
(submuestreos ≈100× y ≈30×) y del modo de SPAdes (`--isolate` y `--careful`).

## Pregunta y objetivos

Pregunta: ¿qué porción del genoma de B378 se recupera con un ensamblado de novo de lecturas cortas y qué diferencias
estructurales y de contenido génico presenta frente a MRSA252?
Objetivos: (1) ensamblar y evaluar la calidad; (2) anotar y tipificar (MLST); (3) buscar genes de virulencia, resistencia y
elementos móviles; (4) localizar regiones sin cobertura y de cobertura alta al mapear contra MRSA252; (5) medir el efecto de
la profundidad y del modo de SPAdes. [VERIFICAR: redacción de la pregunta y los objetivos contra el informe final]

## Datos de entrada (no incluidos en el repositorio)

| Dato | Accesión | Obtención |
|---|---|---|
| Lecturas Illumina pareadas | SRR26803856 (PRJNA1039716) | `scripts/01_descarga_lecturas_ncbi.sh`: `prefetch`, `vdb-validate`, `fasterq-dump --split-files`, `pigz` |
| Referencia MRSA252 | BX571856.1 | `scripts/02_descarga_referencia.sh` (ENA, `wget`); se versiona en `05_reference/` |

Excluidos por `.gitignore`: `00_raw/`, `00_raw_ncbi/`, `02_trim/` (≈5 GB), BAM/BAI, índices Bowtie2 (`*.bt2`), intermedios de
SPAdes (`K*/`, `corrected/`, `scaffolds.*`, grafos), `09_igv/pistas/`, `09_igv/S1_ref.depth.tsv`, `10_depth/test/`,
lecturas submuestreadas (`*.fq.gz`), `icarus_viewers/` y la base BLAST local.

## Estructura (ver [docs/ESTRUCTURA.md](docs/ESTRUCTURA.md))

Salida de `tree -L 2 -I '00_raw*|02_trim'`, anotada. Cada carpeta numerada tiene su propio `README.md`.

```
.
├── 01_qc/              FastQC y MultiQC, lecturas crudas (raw/) y recortadas (trim/)
├── 03_assembly/        Ensamblado SPAdes (S1_full/): contigs.fasta y contigs_cov100.fasta
├── 04_assembly_qc/     QUAST (completo y filtrado), BUSCO, D-Genies, cobertura por contig, tablas de análisis
├── 05_reference/       MRSA252.fasta y .fai (los índices .bt2 no se versionan)
├── 06_annotation/      Prokka (Galaxy) sobre el ensamblado filtrado
├── 07_typing/          MLST (mlst_S1.tsv)
├── 08_genes_mge/       ABRicate (CARD, VFDB), tBLASTn, BLAST NCBI, PHASTEST, copias estimadas
├── 09_igv/             Mapeo a MRSA252, bigWig, BED de regiones, script de IGV, capturas finales
├── 10_depth/           Submuestreos 100× y 30× (iso y car), QUAST comparativo, métricas
├── envs/               YAML de los entornos conda (tif_bioinfo3, quast_env)
├── figuras/            Figuras generadas con scripts/analisis/
├── logs/               Registros de descarga, recorte, SPAdes, Bowtie2 y lista de paquetes
├── docs/               ESTRUCTURA.md
└── scripts/            00-11 (ejecutados), analisis/, envs/, galaxy/, planificados/
```

## Orden de ejecución

1. `scripts/00_crear_carpetas.sh` a `scripts/11_filtrar_cov100.sh`, en ese orden (detalle en [scripts/README.md](scripts/README.md)).
2. Prokka y BUSCO se corrieron en Galaxy Australia (`scripts/galaxy/`); MLST, ABRicate, BLAST y PHASTEST no tienen script
   en el repositorio [VERIFICAR: comandos y versiones].
3. `scripts/planificados/12_comparacion_referencia_igv.sh` y `13_submuestreos_100x_30x.sh` (cabecera "PLANIFICADO"): sus salidas
   existen en `09_igv/` y `10_depth/` [VERIFICAR: si se ejecutaron tal cual].
4. Figuras y tablas derivadas: `scripts/analisis/` (ver abajo).

Todos los scripts aceptan `PROJ=<raíz del proyecto>` (por defecto `~/tp_final`).

## Entorno

Entorno conda `tif_bioinfo3` (`envs/tif_bioinfo3.yml`): FastQC 0.12.1, MultiQC 1.35, Trimmomatic 0.41, SPAdes 4.3.0, seqtk 1.5,
Bowtie2 2.5.5, SAMtools 1.24, minimap2 2.31, sra-tools 3.4.1, pigz 2.8, Python 3.14.7, matplotlib 3.11.1, numpy 2.5.2, R 4.4.3.
Entorno `quast_env` (`envs/quast_env.yml`): QUAST 5.3.0, Python 3.9.23, BLAST 2.16.0, bedtools 2.31.1.
Galaxy Australia: Prokka 1.14.6, BUSCO 6.1.0 (`bacillales_odb12`). deepTools (`bamCoverage`), ABRicate, mlst, BLAST+ de ABRicate/NCBI,
PHASTEST, D-Genies, IGV (2.13.2 figura en `logs/conda_list_tif_bioinfo3.txt`) y los paquetes de R de `analisis_contigs_gc_cobertura.R`
(ggplot2, mclust, patchwork, ggrepel, ragg): [VERIFICAR versiones].

## Reproducir las figuras

Desde la raíz del repositorio, con `tif_bioinfo3` activo. Los scripts de R usan ggplot2, patchwork, ragg, scales, mclust y ggrepel, que no figuran en `envs/tif_bioinfo3.yml` [VERIFICAR: instalación y versiones].

```bash
python3 scripts/analisis/fig20_largo_vs_cobertura.py 03_assembly/S1_full/contigs.fasta figuras/fig20_largo_vs_cobertura.png
python3 scripts/analisis/fig23_profundidad_real.py 03_assembly/S1_full/contigs.fasta 04_assembly_qc/S1_coverage.tsv figuras/fig23_profundidad_real.png
Rscript scripts/analisis/analisis_contigs_gc_cobertura.R 03_assembly/S1_full/contigs.fasta figuras/analisis_gc
python3 scripts/analisis/regiones_sin_correspondencia_MRSA252.py 04_assembly_qc/dgenies_cov100/map_contigs_cov100_to_MRSA252.paf 03_assembly/S1_full/contigs.fasta 04_assembly_qc/regiones_sin_correspondencia_MRSA252.tsv
python3 scripts/analisis/fig24_mapa_contigs.py 04_assembly_qc/dgenies_cov100/map_contigs_cov100_to_MRSA252.paf figuras/fig24_mapa_contigs.png
samtools depth -a 09_igv/S1_ref.bam > 09_igv/S1_ref.depth.tsv
python3 scripts/analisis/fig25_cobertura_MRSA252.py 09_igv/S1_ref.depth.tsv 09_igv/fig25_cobertura.png
python3 scripts/analisis/fig26_prokka_multicopia_ebh.py 06_annotation/prokka/prokka_B378_gff.gff3 03_assembly/S1_full/contigs_cov100.fasta figuras/fig26_prokka_multicopia_ebh.png
python3 scripts/analisis/fig27_blast_multicopia.py figuras/fig27_blast_multicopia.png 08_genes_mge/blast_ncbi/blast_multicopia_S1_hits_unificado.csv
python3 scripts/analisis/fig28_copias_estimadas.py 04_assembly_qc/S1_coverage.tsv figuras/fig28_copias_estimadas.png 08_genes_mge/copias_estimadas_S1.tsv
python3 scripts/analisis/fig29_contexto_genomico.py 04_assembly_qc/dgenies_cov100/map_contigs_cov100_to_MRSA252.paf 03_assembly/S1_full/contigs.fasta 04_assembly_qc/regiones_sin_correspondencia_MRSA252.tsv figuras/fig29A_mapa.png figuras/fig29B_gc.png 04_assembly_qc/gc_tramos_B378.tsv
python3 scripts/analisis/fig30_profundidad_vs_ensamblado.py 10_depth/quast_comp/report.tsv figuras/fig30.png 10_depth/metricas_submuestreos.tsv
Rscript scripts/analisis/fig23_informe.R 10_depth/metricas_submuestreos.tsv figuras/fig23_informe.png
```

Los argumentos de entrada/salida de `fig26`, `fig27`, `fig29` y `fig30` se infirieron de los nombres de archivos existentes
[VERIFICAR]. Las capturas de IGV se generaron a mano con `09_igv/cargar_igv.batch` como punto de partida.

## Figuras → script → archivo

La numeración de los nombres de script (`fig20`…`fig30`) es la de versiones anteriores del informe y no coincide con la final
(Figuras 1–31). Solo se asigna número final a las capturas de IGV, cuyo nombre lo indica.

| Figura del informe | Script | Archivo de salida |
|---|---|---|
| Figuras 16–21, 26 y 27 | IGV (manual; `09_igv/cargar_igv.batch`) | `09_igv/capturas_finales/Figura_NN_*.png` |
| [VERIFICAR] largo vs cobertura de k-mers | `fig20_largo_vs_cobertura.py` | no versionada |
| [VERIFICAR] profundidad real vs k-mers | `fig23_profundidad_real.py` | no versionada |
| [VERIFICAR] GC y cobertura (mclust) | `analisis_contigs_gc_cobertura.R` | `figuras/FigX_gc_cobertura.png` |
| [VERIFICAR] mapa de contigs sobre MRSA252 | `fig24_mapa_contigs.py` | no versionada (insumo: `04_assembly_qc/dgenies_cov100/*.png`) |
| [VERIFICAR] cobertura a lo largo de MRSA252 | `fig25_cobertura_MRSA252.py` | `09_igv/fig25_cobertura.png` |
| [VERIFICAR] multicopia y región ebh (Prokka) | `fig26_prokka_multicopia_ebh.py` | `figuras/fig26_prokka_multicopia_ebh.png` |
| [VERIFICAR] BLAST de multicopia | `fig27_blast_multicopia.py` | `figuras/fig27_blast_multicopia.png` |
| [VERIFICAR] copias estimadas | `fig28_copias_estimadas.py` | `figuras/fig28_copias_estimadas.png` |
| [VERIFICAR] contexto genómico | `fig29_contexto_genomico.py` | `figuras/fig29A_mapa.png`, `figuras/fig29B_gc.png` |
| [VERIFICAR] profundidad vs ensamblado | `fig30_profundidad_vs_ensamblado.py` | `figuras/fig30.png` |
| [VERIFICAR] profundidad vs ensamblado (versión informe) | `fig23_informe.R` | `figuras/fig23_informe.png` |

Tablas 1–37 del informe: la correspondencia con los archivos de datos no pudo establecerse desde el repositorio [VERIFICAR];
las tablas fuente están en `04_assembly_qc/`, `08_genes_mge/` y `10_depth/`.

## Resultados principales

Cifras tomadas de los archivos indicados.

| Resultado | Valor | Fuente |
|---|---|---|
| Pares de lecturas / conservados tras recorte | 8 416 403 / 7 781 558 (92,46 %) | `logs/trimmomatic_S1.log` |
| Ensamblado completo (SPAdes 4.3.0, `--isolate`) | 17 258 contigs, 8 388 158 pb; 22 min 39 s, 4,6 GB | `04_assembly_qc/quast_full/report.tsv`, `logs/spades_full.time` |
| Ensamblado filtrado (≥500 pb y k-mers ≥100) | 74 contigs, 2 790 840 pb, N50 70 746, GC 32,76 % | `04_assembly_qc/quast_cov100/report.tsv` |
| Fracción de MRSA252 cubierta (filtrado) | 85,415 % | `04_assembly_qc/quast_cov100/report.tsv` |
| BUSCO (`bacillales_odb12`, n = 429) | completos 93,9 %, fragmentados 1,6 %, ausentes 4,4 % | `04_assembly_qc/busco_full/busco_short_summary.txt` |
| MLST | *saureus* ST338 | `07_typing/mlst_S1.tsv` |
| Alineamiento de lecturas: ensamblado / MRSA252 | 96,75 % / 83,68 % | `logs/bt2_asm.log`, `logs/bt2_ref.log` |
| Mediana de profundidad sobre MRSA252 | 702× | `09_igv/S1_ref.depth.tsv` (local, no versionado) |
| Regiones de MRSA252 sin cobertura | 50 (152 914 pb en total) | `09_igv/regiones_cov0.bed` |
| *mecA* | NODE_60 (100 % cobertura, 99,85 % identidad) | `08_genes_mge/abricate_card_S1.tsv` |
| *blaZ* | NODE_45 (posición 14 287–15 132) | `06_annotation/prokka/B378_prokka_nodenames.gff3` |
| *ebh* | anotado como dos CDS (`ebh_1`, `ebh_2`) en NODE_15 | `06_annotation/prokka/B378_prokka_nodenames.gff3` |
| Deleción de ≈38,6 kb | [VERIFICAR: no se reproduce con ningún archivo del repositorio] | `09_igv/regiones_cov0.bed` |

Tablas de detalle: [`04_assembly_qc/`](04_assembly_qc/README.md), [`08_genes_mge/`](08_genes_mge/README.md), [`10_depth/`](10_depth/README.md).

## Limitaciones

- Ensamblado a partir de lecturas cortas: repeticiones y elementos de múltiples copias (ARNr, IS, fagos) quedan colapsados o fragmentados.
- Solo el 85,4 % de MRSA252 tiene correspondencia en el ensamblado filtrado; el filtro por cobertura de k-mers descarta contigs cortos.
- Prokka, BUSCO, PHASTEST y D-Genies se ejecutaron en servicios web; sus parámetros y versiones dependen de los registros guardados.
- La comparación se hizo contra una única referencia (MRSA252).
- Parte de los archivos de entrada (lecturas, BAM) no está en el repositorio.

## Cómo citar

Rios, M. (2026). *Ensamblado de novo y caracterización genómica de Staphylococcus aureus B378 (ST338)*. Trabajo Práctico Final,
Bioinformática 3, Licenciatura en Bioinformática, FIUNER-UNER. https://github.com/MatiasRiosMR/TIF_Bioinfo3_Saureus_ST338

## Contacto

Matías Rios, matias.rios@ingenieria.uner.edu.ar, GitHub: MatiasRiosMR
