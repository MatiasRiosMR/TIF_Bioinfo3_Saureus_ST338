#!/usr/bin/env bash
# TP Final Bioinformática 3 - aislamiento B378 (ST338, SRR26803856)
# Se ejecuta desde cualquier carpeta; PROJ es la carpeta del proyecto.
set -euo pipefail
PROJ="${PROJ:-$HOME/tp_final}"
cd "$PROJ"
# Sección 2.0.5 - Genoma de referencia MRSA252 (BX571856.1) desde ENA
# ENTORNO: tif_bioinfo3 (samtools) | PLATAFORMA: computadora personal
wget -O 05_reference/MRSA252.fasta \
  https://www.ebi.ac.uk/ena/browser/api/fasta/BX571856.1

# Verificación: encabezado, número de secuencias, longitud e índice
head -1 05_reference/MRSA252.fasta
grep -c '>' 05_reference/MRSA252.fasta                                   # esperado: 1
grep -v '>' 05_reference/MRSA252.fasta | tr -d '\n' | wc -c               # esperado: 2902619
samtools faidx 05_reference/MRSA252.fasta && cat 05_reference/MRSA252.fasta.fai
