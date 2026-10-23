# 09_igv/capturas_finales: capturas de IGV del informe

## Propósito
Capturas de pantalla de IGV incluidas en el informe (Figuras 16–21, 26 y 27).

## Herramientas
IGV 2.13.2 [VERIFICAR: versión usada para las capturas]. Pistas de las Figuras 16–21: `../cargar_igv.batch` (genoma `05_reference/MRSA252.fasta`;
pistas `S1_ref.bw`, `S1_ref.bam`, `regiones_cov0.bed`, `regiones_cov_alta.bed`, y para las Figuras 26 y 27 el ensamblado, su BAM y el GFF de Prokka).

## Archivos
| Archivo | Figura | Contenido |
|---|---|---|
| `Figura_16_IGV_sin_cobertura_44-72kb.png` | 16 | Tramo sin cobertura en MRSA252, 44–72 kb |
| `Figura_17_IGV_zoom_borde_47231.png` | 17 | Acercamiento al borde en 47 231 |
| `Figura_18_IGV_delecion_1598-1625kb.png` | 18 | Deleción, 1598–1625 kb |
| `Figura_19_IGV_zoom_borde_1602062.png` | 19 | Acercamiento al borde en 1 602 062 |
| `Figura_20_IGV_cobertura_alta_745-757kb.png` | 20 | Cobertura alta, 745–757 kb |
| `Figura_21_IGV_zoom_pico_752kb.png` | 21 | Acercamiento al pico en 752 kb |
| `Figura_26_IGV_ensamblado_mecA_NODE_60.png` | 26 | Lecturas sobre el ensamblado, *mecA* en NODE_60 |
| `Figura_27_IGV_ensamblado_ebh_NODE_15.png` | 27 | Lecturas sobre el ensamblado, *ebh* en NODE_15 |

Formato PNG; 34–170 kB cada una (≈630 kB en total). Las descripciones salen de los nombres de archivo.

## Origen
Capturas manuales en IGV; las Figuras 26 y 27 usan el ensamblado y su BAM (`../S1_asm.bam`) [VERIFICAR: pistas cargadas]. Las posiciones de las Figuras 16–21 corresponden a
`goto` de `../cargar_igv.batch` y a `../regiones_cov0.bed` / `../regiones_cov_alta.bed`. El comando de las Figuras 26 y 27 no está registrado [VERIFICAR].

## Excluido por .gitignore
Nada.
