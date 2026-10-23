# scripts/envs: registro del entorno de software

## Propósito
Exportar los entornos conda para dejar constancia de versiones (Sección 3.2 del informe).

## Contenido
| Archivo | Descripción |
|---|---|
| `exportar_entornos.sh` | Ejecuta `conda env export -n tif_bioinfo3 > envs/tif_bioinfo3.yml`, `conda list -n tif_bioinfo3 > logs/conda_list_tif_bioinfo3.txt` y lo mismo para `quast_env` |

Uso: `PROJ=<raíz> bash scripts/envs/exportar_entornos.sh` (con los entornos ya creados).

## Dónde quedan las salidas
Los YAML no están en esta carpeta sino en `envs/` (raíz del repositorio):
- `envs/tif_bioinfo3.yml`: Python 3.14.7, FastQC 0.12.1, MultiQC 1.35, Trimmomatic 0.41, SPAdes 4.3.0, seqtk 1.5, Bowtie2 2.5.5, SAMtools 1.24,
  minimap2 2.31, sra-tools 3.4.1, pigz 2.8, R 4.4.3, matplotlib 3.11.1, numpy 2.5.2; QUAST 5.3.0 por `pip`.
- `envs/quast_env.yml`: Python 3.9.23, QUAST 5.3.0, BLAST 2.16.0, bedtools 2.31.1, minimap2 2.31, numpy 2.0.2.
- `logs/conda_list_tif_bioinfo3.txt`: lista completa de paquetes.

Recrear: `conda env create -f envs/tif_bioinfo3.yml` y `conda env create -f envs/quast_env.yml`.

## Discrepancias
- El script también guardaría `logs/conda_list_quast_env.txt`, que no existe en el repositorio.
- deepTools, ABRicate, mlst y los paquetes de R (mclust, ggrepel, scales) no figuran en `envs/tif_bioinfo3.yml`.
