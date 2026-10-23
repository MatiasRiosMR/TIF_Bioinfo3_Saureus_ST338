#!/usr/bin/env bash
# TP Final Bioinformática 3 - aislamiento B378 (ST338, SRR26803856)
# Se ejecuta desde cualquier carpeta; PROJ es la carpeta del proyecto.
set -euo pipefail
PROJ="${PROJ:-$HOME/tp_final}"
cd "$PROJ"
# Sección 2.3.2 - Ensamblado con la cobertura completa (7 781 558 pares, ~800x)
# ENTORNO: tif_bioinfo3 (SPAdes 4.3.0) | PLATAFORMA: computadora personal
# Resultado: 22 min 39 s, 4,6 GB, 17 258 contigs, 8 388 158 pb
/usr/bin/time -v spades.py --isolate \
  -1 02_trim/S1_R1.fq.gz -2 02_trim/S1_R2.fq.gz \
  -t 10 -m 12 -o 03_assembly/S1_full 2> logs/spades_full.time
grep -E "Elapsed|Maximum resident|Exit status" logs/spades_full.time

# Verificación de versión y modo (sin corrección de errores de lecturas)
spades.py --version
grep -E "Mode|error correction" 03_assembly/S1_full/params.txt
grep -i "k-mer" 03_assembly/S1_full/spades.log | head
