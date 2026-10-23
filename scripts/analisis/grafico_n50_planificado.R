# ESTADO: PLANIFICADO (Sección 2.9). Gráfico del N50 de los ensamblados comparados con QUAST.
# Ejecutar desde la carpeta del proyecto: Rscript analisis/grafico_n50_planificado.R
library(ggplot2)
q <- read.delim("10_depth/quast_comp/transposed_report.tsv", check.names = FALSE)
ggplot(q, aes(Assembly, N50)) + geom_col() + theme_classic()
