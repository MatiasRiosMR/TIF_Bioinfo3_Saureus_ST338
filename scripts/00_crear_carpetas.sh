#!/usr/bin/env bash
# TP Final Bioinformática 3 - aislamiento B378 (ST338, SRR26803856)
# Se ejecuta desde cualquier carpeta; PROJ es la carpeta del proyecto.
set -euo pipefail
PROJ="${PROJ:-$HOME/tp_final}"
cd "$PROJ"
# Sección 2.0.2 - Estructura de carpetas del proyecto (ver Sección 3.1)
# ENTORNO: ninguno especial | PLATAFORMA: computadora personal
mkdir -p "$PROJ" && cd "$PROJ"
mkdir -p 00_raw 01_qc 02_trim 03_assembly 04_assembly_qc 05_reference \
         06_annotation 07_typing 08_genes_mge 09_igv 10_depth \
         scripts envs logs
