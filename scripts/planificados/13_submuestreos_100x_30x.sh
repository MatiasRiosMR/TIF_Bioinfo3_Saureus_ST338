#!/usr/bin/env bash
# TP Final Bioinformática 3 - aislamiento B378 (ST338, SRR26803856)
# ESTADO: PLANIFICADO, todavía no se ejecutó. Revisar y ajustar antes de correr.
set -euo pipefail
PROJ="${PROJ:-$HOME/tp_final}"
cd "$PROJ"
# Sección 2.9 - Submuestreos de ≈100x y ≈30x, ensamblados con SPAdes --isolate y con --careful, y comparados con QUAST
# ENTORNO: tif_bioinfo3 (seqtk, SPAdes) y quast_env | PLATAFORMA: computadora personal
# Sugerencia de los docentes (21/10/2026): probar --careful. SPAdes no permite combinar --isolate y --careful,
# por lo que cada submuestreo se ensambla dos veces (sufijos _iso y _car) con las mismas lecturas.
# Fracciones = cobertura objetivo / profundidad real medida en la Sección 2.4.1 (762,5x):
#   100 / 762,5 = 0,1311   y   30 / 762,5 = 0,0393   (con 0,11 y 0,033 se obtendrían ≈84x y ≈25x)
# Misma semilla en R1 y R2 para conservar los pares.
mkdir -p 10_depth logs
seqtk sample -s 42 02_trim/S1_R1.fq.gz 0.1311 | gzip > 10_depth/S1_100x_R1.fq.gz
seqtk sample -s 42 02_trim/S1_R2.fq.gz 0.1311 | gzip > 10_depth/S1_100x_R2.fq.gz
seqtk sample -s 42 02_trim/S1_R1.fq.gz 0.0393 | gzip > 10_depth/S1_30x_R1.fq.gz
seqtk sample -s 42 02_trim/S1_R2.fq.gz 0.0393 | gzip > 10_depth/S1_30x_R2.fq.gz
for f in 10_depth/S1_*x_R?.fq.gz; do echo "$f $(( $(zcat "$f" | wc -l) / 4 ))"; done

# Comprobación de que los pares siguen sincronizados (esperado: 0; repetir con 30x)
paste <(zcat 10_depth/S1_100x_R1.fq.gz | awk 'NR%4==1{print $1}') \
      <(zcat 10_depth/S1_100x_R2.fq.gz | awk 'NR%4==1{print $1}') \
  | awk '$1!=$2' | wc -l

# Ensamblados: --isolate (_iso) y --careful (_car) para cada cobertura
for X in 100x 30x; do
  /usr/bin/time -v spades.py --isolate \
    -1 10_depth/S1_${X}_R1.fq.gz -2 10_depth/S1_${X}_R2.fq.gz \
    -t 10 -m 12 -o 10_depth/S1_${X}_iso 2> logs/spades_${X}_iso.time
  /usr/bin/time -v spades.py --careful \
    -1 10_depth/S1_${X}_R1.fq.gz -2 10_depth/S1_${X}_R2.fq.gz \
    -t 10 -m 12 -o 10_depth/S1_${X}_car 2> logs/spades_${X}_car.time
done

# Opcional, al final y en segundo plano: --careful con la cobertura completa (≈800x)
# /usr/bin/time -v spades.py --careful -1 02_trim/S1_R1.fq.gz -2 02_trim/S1_R2.fq.gz \
#   -t 10 -m 12 -o 03_assembly/S1_full_careful 2> logs/spades_full_careful.time

# Comparación con QUAST contra MRSA252
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate quast_env
quast.py 03_assembly/S1_full/contigs.fasta \
  03_assembly/S1_full/contigs_cov100.fasta \
  10_depth/S1_100x_iso/contigs.fasta 10_depth/S1_100x_car/contigs.fasta \
  10_depth/S1_30x_iso/contigs.fasta 10_depth/S1_30x_car/contigs.fasta \
  -r 05_reference/MRSA252.fasta \
  -l completo,filtrado,100x_iso,100x_car,30x_iso,30x_car \
  -o 10_depth/quast_comp -t 4
