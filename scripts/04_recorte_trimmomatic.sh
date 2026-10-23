#!/usr/bin/env bash
# TP Final Bioinformática 3 - aislamiento B378 (ST338, SRR26803856)
# Se ejecuta desde cualquier carpeta; PROJ es la carpeta del proyecto.
set -euo pipefail
PROJ="${PROJ:-$HOME/tp_final}"
cd "$PROJ"
# Sección 2.2.1 - Recorte de adaptadores y de bases de baja calidad
# ENTORNO: tif_bioinfo3 (Trimmomatic) | PLATAFORMA: computadora personal
# Archivo de adaptadores incluido en el entorno
AD=$CONDA_PREFIX/share/trimmomatic/adapters/TruSeq3-PE-2.fa

# Recorte en modo paired-end (se conservan ambas lecturas del par: keepBothReads = True)
trimmomatic PE -threads 4 \
  00_raw/SRR26803856_1.fastq.gz 00_raw/SRR26803856_2.fastq.gz \
  02_trim/S1_R1.fq.gz 02_trim/S1_R1_U.fq.gz \
  02_trim/S1_R2.fq.gz 02_trim/S1_R2_U.fq.gz \
  ILLUMINACLIP:$AD:2:30:10:2:True LEADING:3 TRAILING:3 \
  SLIDINGWINDOW:4:20 MINLEN:50 2> logs/trimmomatic_S1.log

# Resumen del recorte y archivos generados
tail -5 logs/trimmomatic_S1.log
head -5 logs/trimmomatic_S1.log
ls -lh 02_trim/

# Lecturas, bases totales y longitud media de los archivos pareados
for f in 02_trim/S1_R1.fq.gz 02_trim/S1_R2.fq.gz; do
  zcat "$f" | awk -v f="$f" 'NR%4==2{n++; s+=length($0)} END{print f, n, s, s/n}'
done
