#!/usr/bin/env Rscript
# Análisis estadístico de los contigs de B378: GC, cobertura de k-mers y largo.
# Uso: Rscript analisis_contigs_gc_cobertura.R 03_assembly/S1_full/contigs.fasta salida/
# Los nombres de SPAdes son NODE_<n>_length_<L>_cov_<C>.
suppressPackageStartupMessages({library(ggplot2); library(mclust); library(patchwork); library(ggrepel)})
args <- commandArgs(trailingOnly = TRUE)
fa <- args[1]; out <- ifelse(length(args) > 1, args[2], "analisis_gc"); dir.create(out, showWarnings = FALSE)
set.seed(42)

# ---- 1. Leer el FASTA y calcular GC por contig (R base) ----
l <- readLines(fa); h <- grep("^>", l)
sec <- mapply(function(a, b) paste(l[(a + 1):b], collapse = ""), h, c(h[-1] - 1, length(l)))
nom <- sub("^>", "", l[h])
d <- data.frame(contig = nom, stringsAsFactors = FALSE)
d$largo <- as.numeric(sub(".*_length_([0-9]+)_cov_.*", "\\1", nom))
d$cov   <- as.numeric(sub(".*_cov_([0-9.]+).*", "\\1", nom))
d$gc    <- 100 * nchar(gsub("[^GCgc]", "", sec)) / nchar(sec)
d <- d[d$largo >= 500, ]                       # mismo corte que el informe
d$lcov <- log10(d$cov)

# ---- 2. Agrupamiento por mezcla de gaussianas (GC y log10 cobertura) ----
mc <- Mclust(d[, c("gc", "lcov")], G = 1:5, verbose = FALSE)
d$cluster <- factor(mc$classification)
cat("Modelo seleccionado por BIC:", mc$modelName, "con", mc$G, "grupos\n")

write.table(d, file.path(out, "contigs_cluster.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
# ---- 3. Comparación con el filtro del informe (k-mers >= 100) ----
d$filtro <- ifelse(d$cov >= 100, "cov ≥ 100", "cov < 100")
tab <- table(cluster = d$cluster, filtro = d$filtro)
print(tab); write.csv(as.data.frame.matrix(tab), file.path(out, "cluster_vs_filtro.csv"))
cat("Índice de Rand ajustado (cluster vs filtro):",
    round(adjustedRandIndex(d$cluster, d$filtro), 3), "\n")

# ---- 4. Contraste de GC entre los dos grupos del filtro ----
w <- wilcox.test(gc ~ filtro, data = d)
dif <- median(d$gc[d$filtro == "cov ≥ 100"]) - median(d$gc[d$filtro == "cov < 100"])
cat(sprintf("Wilcoxon GC (cov≥100 vs <100): W = %.0f, p = %.2e; diferencia de medianas = %.2f puntos\n",
            w$statistic, w$p.value, dif))
boot <- replicate(2000, { s <- d[sample(nrow(d), replace = TRUE), ]
  median(s$gc[s$filtro == "cov ≥ 100"]) - median(s$gc[s$filtro == "cov < 100"]) })
cat("IC95% bootstrap de la diferencia de medianas:", round(quantile(boot, c(.025, .975)), 2), "\n")

# ---- 5. Cromosoma: contigs atípicos por GC y cobertura (z robusto con MAD) ----
cr <- d[d$cov >= 100, ]
mw <- function(x, w) { o <- order(x); x <- x[o]; w <- w[o]; x[which(cumsum(w) >= sum(w)/2)[1]] }
cov_cromo <- mw(cr$cov, cr$largo); gc_cromo <- mw(cr$gc, cr$largo)
cr$copias <- cr$cov / cov_cromo                                  # número de copias relativo
cr$z_gc   <- (cr$gc - median(cr$gc)) / mad(cr$gc)
cr$atipico <- abs(cr$z_gc) > 3.5 | cr$copias > 1.5 | cr$copias < 0.5
cat("Cobertura mediana ponderada del cromosoma:", round(cov_cromo, 1), "\n")
write.table(cr[order(-abs(cr$z_gc)), c("contig","largo","cov","gc","copias","z_gc","atipico")],
            file.path(out, "contigs_filtrados_atipicos.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
print(head(cr[cr$atipico, c("contig","largo","gc","copias","z_gc")], 10))

# ---- 6. Figura ----
pal <- c("#0072B2", "#E69F00", "#009E73", "#CC79A7", "#999999")
pA <- ggplot(d, aes(gc, cov, colour = cluster, size = largo)) + geom_point(alpha = .6) +
  scale_y_log10() + scale_size_continuous(range = c(.6, 4), guide = "none") +
  scale_colour_manual(values = pal, name = "Grupo (mclust)") +
  labs(title = "A", x = "GC (%)", y = "Cobertura de k-mers (log)") + theme_classic(base_size = 8) + theme(legend.position = "bottom")
pB <- ggplot(cr, aes(gc, copias)) +
  geom_hline(yintercept = 1, linetype = 2, colour = "grey50") +
  geom_point(aes(size = largo, colour = atipico), alpha = .7) +
  geom_text_repel(data = cr[cr$atipico, ], aes(label = sub("_length.*", "", contig)),
                  size = 2.4, max.overlaps = 20) +
  scale_colour_manual(values = c("FALSE" = "#0072B2", "TRUE" = "#D55E00"), guide = "none") +
  scale_size_continuous(range = c(.8, 4), guide = "none") +
  labs(title = "B", x = "GC (%)", y = "Copias relativas al cromosoma") + theme_classic(base_size = 8)
ggsave(file.path(out, "FigX_gc_cobertura.png"), pA / pB, width = 8.6, height = 12, units = "cm",
       dpi = 400, device = ragg::agg_png)
sink(file.path(out, "sessionInfo.txt")); print(sessionInfo()); sink()
