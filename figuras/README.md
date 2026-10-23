# figuras: figuras generadas con scripts

## Propósito
Figuras del análisis creadas con Python y R (las capturas de IGV están en `09_igv/capturas_finales/`; la figura de cobertura en `09_igv/fig25_cobertura.png`).

## Herramientas
Python 3.14.7 (matplotlib 3.11.1, numpy 2.5.2), R 4.4.3 del entorno `tif_bioinfo3` (paquetes de gráficos: ggplot2, patchwork, ragg; versión [VERIFICAR]).

## Archivos
| Archivo | Script | Dimensión (px) | Contenido |
|---|---|---|---|
| `fig23_informe.png` | `scripts/analisis/fig23_informe.R` | 1980×1560 | N50, NGA50, contigs y fracción del genoma por estrategia (6 ensamblados) |
| `fig30.png` | `scripts/analisis/fig30_profundidad_vs_ensamblado.py` | 1840×1880 | Seis métricas de QUAST por ensamblado |
| `fig26_prokka_multicopia_ebh.png` | `fig26_prokka_multicopia_ebh.py` | | Genes de Prokka en los 11 contigs de multicopia y la región *ebh* (NODE_15) |
| `fig27_blast_multicopia.png` | `fig27_blast_multicopia.py` | | BLAST de contigs de multicopia sin función asignada |
| `fig28_copias_estimadas.png` | `fig28_copias_estimadas.py` | | Copias estimadas de los 11 contigs de multicopia |
| `fig29A_mapa.png`, `fig29B_gc.png` | `fig29_contexto_genomico.py` | 1373×1361, 1920×1520 | Mapa circular de MRSA252 y GC de los tramos sin correspondencia |
| `FigX_gc_cobertura.png` | `analisis_contigs_gc_cobertura.R` | 1354×1889 | GC vs cobertura (mclust) y copias relativas |

Tamaño: 1,8 MB. Comandos exactos de cada script: sección "Reproducir las figuras" del `README.md` raíz.

## Excluido por .gitignore
Nada.

## Correspondencia con el informe
Los nombres `figNN` provienen de versiones anteriores del informe y no coinciden con la numeración final (Figuras 1–31)
[VERIFICAR: asignar el número final de cada archivo].
