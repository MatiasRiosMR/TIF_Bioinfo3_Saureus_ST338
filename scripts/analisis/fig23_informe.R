#!/usr/bin/env Rscript
# Figura 23 (versión informe) - Sección 2.9
# Uso: Rscript fig23_informe.R metricas_submuestreos.tsv fig23_informe.png
invisible(Sys.setlocale("LC_ALL","C.UTF-8"))
suppressPackageStartupMessages({library(ggplot2); library(patchwork)})
a <- commandArgs(trailingOnly=TRUE)
d <- read.delim(a[1], check.names=FALSE)
names(d) <- c("ens","N50","NGA50","nc","largo","gf","mis")
niv <- c("completo","filtrado","100x_iso","100x_car","30x_iso","30x_car")
d$ens <- factor(d$ens, niv, c("Completo","Filtrado","100×\niso","100×\ncar","30×\niso","30×\ncar"))
d$g <- ifelse(as.integer(d$ens) <= 2, "Sin submuestreo", "Submuestreo")
col <- c("Sin submuestreo"="#9AA0A6","Submuestreo"="#1F77B4")
fm <- function(x,k=1) formatC(x,format="f",digits=k,decimal.mark=",",big.mark=".")
th <- theme_minimal(base_size=9) + theme(panel.grid.major.x=element_blank(), panel.grid.minor=element_blank(),
  axis.title=element_blank(), axis.text.x=element_text(size=6.5), legend.position="none",
  plot.title=element_text(face="bold", size=9), plot.margin=margin(3,5,3,5))
bar <- function(v, tt, lab, scale) ggplot(d, aes(ens, .data[[v]], fill=g)) + geom_col(width=.7) +
  geom_text(aes(label=lab(.data[[v]])), vjust=-.4, size=2.6) + scale_fill_manual(values=col) + scale + labs(title=tt) + th
ex <- expansion(mult=c(0,.15))
A <- bar("N50","A. N50 (kb) ↑", function(x) fm(x/1000,1), scale_y_continuous(labels=function(x) fm(x/1000,0), expand=ex))
B <- bar("NGA50","B. NGA50 (kb) ↑", function(x) fm(x/1000,1), scale_y_continuous(labels=function(x) fm(x/1000,0), expand=ex))
C <- bar("nc","C. Nº de contigs (escala log) ↓", function(x) fm(x,0),
         scale_y_log10(breaks=c(10,100,1000,10000), labels=function(x) fm(x,0), expand=expansion(mult=c(0,.2)))) +
     coord_cartesian(ylim=c(10,NA))
D <- bar("gf","D. Fracción del genoma de MRSA252 (%) ↑", function(x) fm(x,1),
         scale_y_continuous(limits=c(0,100), expand=expansion(mult=c(0,.05))))
fig <- (A+B)/(C+D) + plot_annotation(caption="Gris: sin submuestreo · Azul: submuestreo (seqtk, semilla 42) · iso = --isolate, car = --careful",
  theme=theme(plot.caption=element_text(size=7.5, hjust=.5, colour="grey30")))
ragg::agg_png(a[2], width=6.6, height=5.2, units="in", res=300); print(fig); invisible(dev.off())
