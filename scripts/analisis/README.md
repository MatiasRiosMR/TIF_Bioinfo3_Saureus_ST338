# scripts/analisis: gráficos y tablas derivadas

## Propósito
Scripts de Python y R que generan las figuras y las tablas de análisis del informe. Se ejecutan desde la raíz del repositorio,
con el entorno `tif_bioinfo3` (Python 3.14.7, R 4.4.3). Los paquetes de R (ggplot2, patchwork, ragg, scales, mclust, ggrepel) no figuran en el YAML del entorno [VERIFICAR].

## Scripts
| Script | Uso (argumentos) | Salida |
|---|---|---|
| `fig20_largo_vs_cobertura.py` | `contigs.fasta salida.png` | Largo vs cobertura de k-mers |
| `fig23_profundidad_real.py` | `contigs.fasta S1_coverage.tsv salida.png` | Profundidad real vs largo y vs k-mers |
| `analisis_contigs_gc_cobertura.R` | `contigs.fasta [directorio]` | `contigs_cluster.tsv`, `cluster_vs_filtro.csv`, `contigs_filtrados_atipicos.tsv`, `FigX_gc_cobertura.png`, `sessionInfo.txt` |
| `regiones_sin_correspondencia_MRSA252.py` | `mapeo.paf contigs.fasta salida.tsv [largo_min=3000] [cov_min=100] [largo_contig_min=500]` | `04_assembly_qc/regiones_sin_correspondencia_MRSA252.tsv` |
| `fig24_mapa_contigs.py` | `mapeo.paf salida.png [--min-bloque --min-hueco --multicopia --largo-ref]` | Mapa de contigs sobre MRSA252 |
| `fig25_cobertura_MRSA252.py` | `S1_ref.depth.tsv salida.png [--ventana --min-sin-cobertura --ymax --pico]` | `09_igv/fig25_cobertura.png` |
| `fig26_prokka_multicopia_ebh.py` | `prokka.gff3 contigs.fasta salida.png` | Genes en contigs de multicopia y *ebh* |
| `fig27_blast_multicopia.py` | `salida.png hits1.csv [hits2.csv ...]` | BLAST de multicopia |
| `fig28_copias_estimadas.py` | `S1_coverage.tsv salida.png copias.tsv` | Gráfico y `08_genes_mge/copias_estimadas_S1.tsv` |
| `fig29_contexto_genomico.py` | `mapeo.paf contigs.fasta tramos.tsv A.png B.png tabla_gc.tsv` | Mapa, GC y `04_assembly_qc/gc_tramos_B378.tsv` |
| `fig30_profundidad_vs_ensamblado.py` | `quast_comp/report.tsv figura.png tabla.tsv` | `figuras/fig30.png`, `10_depth/metricas_submuestreos.tsv` |
| `fig30_profundidad_vs_ensamblado.R` | `metricas_submuestreos.tsv salida.png` | Versión en R de la misma figura |
| `fig23_informe.R` | `metricas_submuestreos.tsv salida.png` | `figuras/fig23_informe.png` |
| `blast_resumen_tramos.py` | `hits.csv resumen.tsv` | Resumen por tramo de hits BLAST |
| `esquema_avance.py` | sin argumentos | `esquema_avance.png` (diagrama de avance del TP; no es una figura del informe) |
| `grafico_n50_planificado.R` | sin argumentos | Estado "PLANIFICADO"; lee `10_depth/quast_comp/transposed_report.tsv` |

Comandos con rutas reales: `README.md` raíz.

## Notas [VERIFICAR]
- Las docstrings numeran las figuras con versiones anteriores del informe (20, 21, 22, 23, 24, 25); no coinciden con la numeración final.
- `fig26`, `fig27`, `fig29` y `fig30` documentan una invocación sin prefijo de carpeta (`python3 fig26_...`): se ejecutan desde la raíz con la ruta `scripts/analisis/`.
- El encabezado que escribe `blast_resumen_tramos.py` no coincide con el de `08_genes_mge/blast_ncbi/blast_multicopia_S1_resumen.tsv`.
- `fig24_mapa_contigs.py` y `fig25` mencionan la ruta `analisis/...` (carpeta del paquete original), hoy `scripts/analisis/`.
