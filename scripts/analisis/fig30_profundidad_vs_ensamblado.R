#!/usr/bin/env Rscript
# Figura 23 - Comparación de estrategias de ensamblado (Sección 2.9)
# Uso: Rscript fig30_profundidad_vs_ensamblado.R metricas_submuestreos.tsv fig30_R.png
invisible(Sys.setlocale("LC_ALL","C.UTF-8"))
suppressPackageStartupMessages({library(ggplot2); library(patchwork); library(scales)})
a <- commandArgs(trailingOnly = TRUE)
d <- read.delim(a[1], check.names = FALSE, stringsAsFactors = FALSE)
names(d) <- c("ens","N50","NGA50","ncontigs","largo","gf","misas")
niv <- c("completo","filtrado","100x_iso","100x_car","30x_iso","30x_car")
et  <- c("Completo","Filtrado","100×\n--isolate","100×\n--careful","30×\n--isolate","30×\n--careful")
d$ens <- factor(d$ens, niv, et)
d$grupo <- factor(c("Sin submuestreo","Sin submuestreo","Submuestreo","Submuestreo","Submuestreo","Submuestreo"),
                  c("Sin submuestreo","Submuestreo"))
d$grupo <- factor(ifelse(grepl("^(Completo|Filtrado)", d$ens), "Sin submuestreo", "Submuestreo"),
                  c("Sin submuestreo","Submuestreo"))
col <- c("Sin submuestreo"="#9AA0A6", "Submuestreo"="#1F77B4")
fm <- function(x, k=1) formatC(x, format="f", digits=k, decimal.mark=",", big.mark=".")
base <- theme_minimal(base_size = 11) +
  theme(panel.grid.major.x = element_blank(), panel.grid.minor = element_blank(),
        plot.title = element_text(face="bold", size=11.5), plot.subtitle = element_text(colour="grey30", size=9),
        axis.title = element_blank(), axis.text.x = element_text(size=8), legend.position="none",
        plot.margin = margin(6,8,6,8))
panel <- function(v, titulo, sub, lab, ref=NULL, log=FALSE, kb=FALSE) {
  d$y <- d[[v]]; if (kb) d$y <- d$y/1000
  p <- ggplot(d, aes(ens, y, fill=grupo)) + geom_col(width=.68) +
    coord_cartesian(ylim=if (log) c(10, NA) else NULL) +
    geom_text(aes(label=lab(y)), vjust=-.4, size=3.1) +
    scale_fill_manual(values=col) + labs(title=titulo, subtitle=sub) + base
  if (!is.null(ref)) p <- p + geom_hline(yintercept=ref, linetype="dashed", colour="grey35", linewidth=.4)
  if (log) p <- p + scale_y_log10(breaks=c(10,100,1000,10000), labels=function(x) fm(x,0), expand=expansion(mult=c(0,.25)))
  else p <- p + scale_y_continuous(labels=function(x) fm(x,0), expand=expansion(mult=c(0,.18)))
  p
}
p1 <- panel("N50","N50 (kb)","↑ mejor · contigs más largos · línea punteada = ensamblado completo",
            function(x) paste0(fm(x,1)," kb"), ref=d$N50[1]/1000, kb=TRUE)
p2 <- panel("NGA50","NGA50 (kb)","↑ mejor · N50 solo de lo alineado a MRSA252 · línea = completo",
            function(x) paste0(fm(x,1)," kb"), ref=d$NGA50[1]/1000, kb=TRUE)
p3 <- panel("ncontigs","Nº de contigs (de cualquier largo)","↓ mejor · escala logarítmica",
            function(x) fm(x,0), log=TRUE)
p4 <- ggplot(d, aes(ens, gf, fill=grupo)) + geom_col(width=.68) +
  geom_text(aes(label=paste0(fm(gf,1)," %")), vjust=-.4, size=3.1) +
  scale_fill_manual(values=col) +
  scale_y_continuous(limits=c(0,100), expand=expansion(mult=c(0,.05)), labels=function(x) paste0(x," %")) +
  labs(title="Fracción del genoma de MRSA252 cubierta", subtitle="↑ mejor · ≈ 85 % en todos: ~300 kb de B378 no alinean con MRSA252") + base
p5 <- panel("misas","Misassemblies (QUAST)","↓ mejor · se mantienen en 47–51",
            function(x) fm(x,0))
# Panel de lectura
txt <- paste(
 "Cómo leer la figura",
 "",
 "• Gris: ensamblados sin submuestreo.",
 "  Azul: submuestreo de lecturas (seqtk,",
 "  semilla 42) y SPAdes 4.3.0.",
 "",
 "• El submuestreo más que duplica el N50",
 "  (43 → 98–103 kb) y baja el nº de contigs",
 "  de 17 258 a 959–2 794.",
 "",
 "• 30× da N50 similar y menos contigs que",
 "  100× (NGA50 algo menor: 37,4 vs 40,4 kb):",
 "  no hace falta más profundidad.",
 "",
 "• --careful no mejora a --isolate.",
 "",
 "• Fracción del genoma y misassemblies",
 "  no cambian: no dependen de la estrategia.", sep="\n")
p6 <- ggplot() + annotate("text", x=0, y=1, label=txt, hjust=0, vjust=1, size=3.3, lineheight=1.05) +
  xlim(0,1) + ylim(0,1) + theme_void() +
  theme(plot.background=element_rect(fill="#F3F6FA", colour=NA), plot.margin=margin(6,8,6,8))
fig <- (p1 + p2 + p3) / (p4 + p5 + p6) +
  plot_annotation(
    title = "Submuestrear las lecturas mejora el ensamblado de B378 sin perder genoma",
    subtitle = "Comparación QUAST (referencia MRSA252, BX571856.1) de seis estrategias · S. aureus B378, ST338, SRR26803856",
    theme = theme(plot.title=element_text(face="bold", size=15), plot.subtitle=element_text(colour="grey30", size=10)))
ragg::agg_png(a[2], width=15, height=8.4, units="in", res=200)
print(fig); invisible(dev.off())
