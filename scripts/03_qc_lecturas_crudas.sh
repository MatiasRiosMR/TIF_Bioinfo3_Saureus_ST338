#!/usr/bin/env bash
# TP Final Bioinformática 3 - aislamiento B378 (ST338, SRR26803856)
# Se ejecuta desde cualquier carpeta; PROJ es la carpeta del proyecto.
set -euo pipefail
PROJ="${PROJ:-$HOME/tp_final}"
cd "$PROJ"
# Sección 2.1 - Control de calidad de las lecturas crudas
# ENTORNO: tif_bioinfo3 (FastQC, MultiQC) | PLATAFORMA: computadora personal
# NOTA: este comando se reconstruyó a partir del de la Sección 2.2.2 (mismo programa y opciones);
#       confirmar que coincide con el que se ejecutó, ya que el informe no lo detalla.
mkdir -p 01_qc/raw
fastqc -t 4 -o 01_qc/raw 00_raw/SRR26803856_1.fastq.gz 00_raw/SRR26803856_2.fastq.gz
multiqc 01_qc/raw -o 01_qc/raw -n multiqc_raw
