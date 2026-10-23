#!/usr/bin/env bash
# TP Final Bioinformática 3 - aislamiento B378 (ST338, SRR26803856)
# Se ejecuta desde cualquier carpeta; PROJ es la carpeta del proyecto.
set -euo pipefail
PROJ="${PROJ:-$HOME/tp_final}"
cd "$PROJ"
# Sección 2.4.1 - Evaluación del ensamblado completo con QUAST 5.3.0 contra MRSA252
# ENTORNO: quast_env (entorno conda propio) | PLATAFORMA: computadora personal
# 'conda activate' dentro de un script requiere cargar antes el perfil de conda:
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate quast_env
quast.py 03_assembly/S1_full/contigs.fasta \
  -r 05_reference/MRSA252.fasta -o 04_assembly_qc/quast_full -t 4
