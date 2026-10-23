# 05_reference: genoma de referencia

## Propósito
Genoma de *S. aureus* MRSA252 (BX571856.1) para QUAST, D-Genies, mapeo de lecturas e IGV.

## Generado por
`scripts/02_descarga_referencia.sh` (ENA, `wget`; indexado con `samtools faidx`). Índices Bowtie2 con
`scripts/planificados/12_comparacion_referencia_igv.sh` (`bowtie2-build`, Bowtie2 2.5.5).

## Archivos
| Archivo | Contenido |
|---|---|
| `MRSA252.fasta` | 1 secuencia, 2 902 619 pb; encabezado `ENA\|BX571856\|BX571856.1` |
| `MRSA252.fasta.fai` | Índice de SAMtools (`nombre largo offset bases_por_línea bytes_por_línea`) |
| `MRSA252.{1..4}.bt2`, `MRSA252.rev.{1,2}.bt2` | Índice Bowtie2 (no versionado) |

Tamaño: 15 MB (los `.bt2` son la mayor parte).

## Excluido por .gitignore
`*.bt2`. Se regenera con `bowtie2-build 05_reference/MRSA252.fasta 05_reference/MRSA252`.

## Correspondencia con el informe
Sección de datos de entrada (2.0.5) [VERIFICAR: número exacto].
