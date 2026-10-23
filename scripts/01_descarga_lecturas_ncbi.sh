#!/usr/bin/env bash
# TP Final Bioinformática 3 - aislamiento B378 (ST338, SRR26803856)
# Se ejecuta desde cualquier carpeta; PROJ es la carpeta del proyecto.
set -euo pipefail
PROJ="${PROJ:-$HOME/tp_final}"
cd "$PROJ"
# Sección 2.0.4 - Descarga del run SRR26803856 desde el SRA de NCBI
# ENTORNO: bioinfo3 / tif_bioinfo3 (sra-tools) | PLATAFORMA: computadora personal
# Los archivos de ENA (calidades simplificadas) se descartaron: ver Sección 4, registro de decisiones.
RUN=SRR26803856
mkdir -p 00_raw_ncbi && cd 00_raw_ncbi

# 1) Descarga en segundo plano y seguimiento (el 17/10/2026 tardó unos 15 min)
nohup prefetch "$RUN" -O . > ../logs/prefetch_${RUN}.log 2>&1 &
PID=$!
while kill -0 "$PID" 2>/dev/null; do du -sh . ; sleep 5; done   # equivale a 'watch -n 5 du -sh'
wait "$PID"

# 2) Verificación de integridad y conversión a FASTQ
vdb-validate "$RUN/$RUN.sra" 2>&1 | tee ../logs/vdb-validate.log
fasterq-dump --split-files --threads 4 "$RUN/$RUN.sra" 2>&1 | tee ../logs/fasterq-dump.log

# 3) Compresión en paralelo (requiere pigz: sudo apt install -y pigz)
pigz -p 8 ${RUN}_1.fastq ${RUN}_2.fastq

# 4) Comprobaciones: lecturas por archivo, calidades de las primeras 100 000 lecturas, MD5 y tamaños
for f in ${RUN}_?.fastq.gz; do echo "$f $(( $(zcat "$f" | wc -l) / 4 ))"; done
zcat ${RUN}_1.fastq.gz | head -400000 | awk 'NR%4==0' | fold -w1 | sort | uniq -c | sort -k2
md5sum ${RUN}_?.fastq.gz; ls -lh

# 5) Ubicación: los archivos de NCBI van a 00_raw; los de ENA (si existen) a 00_raw_ena
cd "$PROJ"
if ls 00_raw/${RUN}_?.fastq.gz >/dev/null 2>&1; then
  mkdir -p 00_raw_ena && mv 00_raw/${RUN}_?.fastq.gz 00_raw_ena/
fi
mv 00_raw_ncbi/${RUN}_?.fastq.gz 00_raw/
ls -lh 00_raw/ 00_raw_ena/ 2>/dev/null || true
