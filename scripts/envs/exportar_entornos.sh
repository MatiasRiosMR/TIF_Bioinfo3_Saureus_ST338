#!/usr/bin/env bash
# Sección 3.2 - Registro del entorno de software (trazabilidad)
# Ejecutar con el entorno tif_bioinfo3 ya creado. Las versiones de los paquetes instalados con pip
# (por ejemplo QUAST y cutadapt) no quedan fijadas con la misma seguridad en el YAML; por eso también se
# guarda la lista completa.
set -euo pipefail
PROJ="${PROJ:-$HOME/tp_final}"
cd "$PROJ"
conda env export -n tif_bioinfo3 > envs/tif_bioinfo3.yml
conda list -n tif_bioinfo3 > logs/conda_list_tif_bioinfo3.txt
# Entorno propio de QUAST
conda env export -n quast_env > envs/quast_env.yml
conda list -n quast_env > logs/conda_list_quast_env.txt
