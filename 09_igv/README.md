# 09_igv: mapeo, cobertura e IGV

## Propósito
Alineamientos de las lecturas contra el ensamblado y contra MRSA252, perfiles de cobertura, regiones sin cobertura o de cobertura alta, y capturas de IGV.

## Herramientas
Bowtie2 2.5.5, SAMtools 1.24, deepTools (`bamCoverage`) [VERIFICAR: versión, no figura en los entornos], IGV 2.13.2 (según `logs/conda_list_tif_bioinfo3.txt`).

## Generado por
- `scripts/10_cobertura_real_bowtie2.sh` → `S1_asm.*` (lecturas contra `contigs.fasta`).
- `scripts/planificados/12_comparacion_referencia_igv.sh` → `S1_ref.bam`, `S1_ref.bw` (bin 50, RPGC).
- `samtools depth -a 09_igv/S1_ref.bam > 09_igv/S1_ref.depth.tsv` → `fig25_cobertura.png` (`fig25_cobertura_MRSA252.py`).

## Archivos
| Archivo | Contenido |
|---|---|
| `regiones_cov0.bed` | 50 regiones de MRSA252 con profundidad 0 (≥1 kb); BED3 sin encabezado |
| `regiones_cov_alta.bed` | 20 regiones de profundidad alta; BED4, la cuarta columna es el valor de profundidad [VERIFICAR: criterio exacto] |
| `contigs_B378_vs_MRSA252.bed` | 137 bloques de contigs sobre MRSA252; BED6 (columna 5 = MAPQ del alineamiento, 60 en los primeros bloques [VERIFICAR]) |
| `S1_ref.bw`, `S1_ref_cobertura_cruda.bw` | bigWig normalizado y crudo [VERIFICAR: origen del crudo] |
| `fig25_cobertura.png` | Profundidad relativa por ventana de 2 kb |
| `cargar_igv.batch` | Comandos de IGV para cargar pistas y tomar capturas (contiene rutas absolutas de la máquina de origen) |
| `capturas_finales/` | Capturas incluidas en el informe (ver su README) |

Tamaño versionado: <1 MB. En disco: 2,4 GB.

## Excluido por .gitignore
`*.bam`, `*.bai`, `*.bt2` (≈2,4 GB), `S1_ref.depth.tsv` (99 MB) y `pistas/` (enlaces simbólicos con rutas absolutas).
Regenerar: ejecutar `scripts/10_cobertura_real_bowtie2.sh` y `scripts/planificados/12_comparacion_referencia_igv.sh`; luego recrear `pistas/` con los nombres que usa `cargar_igv.batch`.

## Resultados clave
Mediana de profundidad sobre MRSA252: 702× (`S1_ref.depth.tsv`); 83,68 % de alineamiento (`logs/bt2_ref.log`).

## Correspondencia con el informe
Secciones 2.5 y 2.8; Figuras 16–21, 26 y 27 (capturas) y figura de cobertura [VERIFICAR: número de `fig25_cobertura.png`].
