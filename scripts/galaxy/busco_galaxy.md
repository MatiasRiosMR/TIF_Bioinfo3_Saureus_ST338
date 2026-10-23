# BUSCO en Galaxy Australia (Sección 2.4.2)

- Servidor: Galaxy Australia (https://usegalaxy.org.au), historial `Proyecto-TPFinal-Bioinfo3`.
- Herramienta: BUSCO 6.1.0.
- Entrada: dataset 1 (`contigs.fasta` completo, 17 258 contigs, sin filtrar por largo).

| Parámetro de Galaxy | Valor |
|---|---|
| Sequences to analyze | Dataset 1 (contigs.fasta) |
| Mode | Genome assemblies (DNA); el resumen indica que se usó `prok_genome_min` con Prodigal |
| Lineage | Bacillales; base `bacillales_odb12` (la planificación preveía odb10) |
| Resto | valores por defecto |

Resultado: C 403 (93,9 %) de 429 BUSCOs, de los cuales 42 con codones de parada internos.
Guardar los archivos (resumen corto y tabla completa) en `04_assembly_qc/busco_full/`.
