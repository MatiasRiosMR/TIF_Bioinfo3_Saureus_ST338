# 01_qc: control de calidad de las lecturas

## Propósito
Evaluar la calidad de las lecturas crudas (`raw/`) y de las recortadas (`trim/`). Sección 2.1 y 2.2.2 del informe.

## Herramientas
FastQC 0.12.1 y MultiQC 1.35 (entorno `tif_bioinfo3`).

## Generado por
- `scripts/03_qc_lecturas_crudas.sh` → `raw/` (comando reconstruido, ver nota en el script).
- `scripts/05_qc_posterior_recorte.sh` → `trim/` (MultiQC integra `raw/`, `trim/` y `logs/trimmomatic_S1.log`).

## Archivos
| Ruta | Contenido |
|---|---|
| `raw/SRR26803856_{1,2}_fastqc.html/.zip` | Informes FastQC de R1 y R2 crudas |
| `raw/multiqc_report.html`, `raw/multiqc_data/` | Resumen MultiQC de las lecturas crudas |
| `trim/S1_R{1,2}_fastqc.html/.zip` | Informes FastQC de las lecturas recortadas |
| `trim/multiqc_antes_despues.html` | MultiQC comparativo antes/después, incluye estadísticas de Trimmomatic |
| `*/multiqc_data/*.txt` | Tablas tabuladas de cada módulo (`multiqc_general_stats.txt`, `multiqc_fastqc.txt`, `multiqc_trimmomatic.txt`, etc.) y `multiqc_data.json` |

Tamaño: ≈9 MB en total. Las tablas `multiqc_data/*.txt` tienen una fila por muestra (R1/R2) y una columna por métrica.

## Excluido por .gitignore
Las lecturas (`00_raw/`, `02_trim/`). Para regenerar: ver `scripts/01_descarga_lecturas_ncbi.sh` y `scripts/04_recorte_trimmomatic.sh`.

## Correspondencia con el informe
Figuras de calidad de lecturas antes y después del recorte.
