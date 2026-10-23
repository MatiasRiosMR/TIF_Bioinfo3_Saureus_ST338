#!/usr/bin/env bash
# TP Final Bioinformática 3 - aislamiento B378 (ST338, SRR26803856)
# Se ejecuta desde cualquier carpeta; PROJ es la carpeta del proyecto.
set -euo pipefail
PROJ="${PROJ:-$HOME/tp_final}"
cd "$PROJ"
# Sección 2.2.2 - Control de calidad posterior al recorte
# ENTORNO: tif_bioinfo3 (FastQC, MultiQC) | PLATAFORMA: computadora personal
mkdir -p 01_qc/trim
fastqc -t 4 -o 01_qc/trim 02_trim/S1_R1.fq.gz 02_trim/S1_R2.fq.gz
multiqc 01_qc/trim 01_qc/raw logs/trimmomatic_S1.log -o 01_qc/trim -n multiqc_antes_despues
