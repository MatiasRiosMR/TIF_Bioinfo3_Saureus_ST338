# Prokka en Galaxy Australia (Sección 2.6)

- Servidor: Galaxy Australia (https://usegalaxy.org.au), historial `Proyecto-TPFinal-Bioinfo3`.
- Herramienta: Prokka, versión 1.14.6 (Galaxy 1.14.6+galaxy2).
- Fecha de la corrida: 20/10/2026. Duración: 0,97 minutos.
- Entrada: dataset 5 (`contigs_cov100.fasta`, 74 contigs, 2 790 840 pb), generado con `scripts/11_filtrar_cov100.sh`.

## Parámetros usados (el resto, por defecto)

| Parámetro de Galaxy | Valor | Opción de Prokka |
|---|---|---|
| Genus name | Staphylococcus | `--genus` |
| Species name | aureus | `--species` |
| Strain name | B378 | `--strain` |
| Kingdom | Bacteria | `--kingdom` |
| Force GenBank/ENA/DDJB compliance | Yes | `--compliant` |
| Genetic code | 11 (por defecto) | `--gcode` |
| E-value | 1e-06 (por defecto) | `--evalue` |
| Use genus-specific BLAST database | No | `--usegenus` no usado |
| Infernal + Rfam | No | `--rfam` no usado |
| Salidas | todas las opcionales (GFF3, GBK, FNA, FAA, FFN, SQN, FSA, TBL, TSV, ERR, TXT) | |

## Línea de comando registrada por Galaxy (dataset 17, log)

```
prokka --cpus 8 --quiet --outdir outdir --prefix prokka --increment 1 --gffver 3 --compliant \
  --genus Staphylococcus --species aureus --strain B378 --kingdom Bacteria --gcode 11 --evalue 1e-06 <entrada>
```

## Resultados (dataset 16, TXT, y dataset 14, TSV)

CDS 2576 · genes 2636 · ARNt 55 · ARNr 4 · ARNtm 1 · CRISPR 0.
En el TSV, 847 CDS (32,9 %) figuran como `hypothetical protein` (802 sin coincidencia según el log).

## Descarga

Guardar en `06_annotation/prokka/`: GFF3 (dataset 6), GBK (7), FAA (9), FFN (10) y TSV (14), además del TXT (16) y el log (17).
