# Cambios

## 2.2.0 — 21 de octubre de 2026

Base: commit 1539db5c05a48bd5b4f980ee3cc65b18224fb4cf (2.1).

- Recuadros divisibles entre páginas, fondos y títulos explícitamente blancos.
- Ancho extendido hacia el exterior en páginas pares/impares y flotantes aplazados. Los bloques extendidos indivisibles demasiado altos se rechazan antes de recortarse.
- Imágenes con conservación de proporción y altura disponible calculada después de reservar el pie. Etiquetas opcionales en figuras normales/extendidas.
- Guardas de ancho, altura, contexto, perfil, idioma, clase y motor. Los caracteres ausentes son errores.
- Índice preparado para numeración de cuatro cifras, estilos de páginas de capítulo y páginas de respeto unificados, notas marginales alineadas por arriba.
- Portada sin destinos PDF duplicados; español por defecto e inglés probado; versalitas reales para la fuente principal.
- Demo independiente de un gráfico precompilado, con prosa, ecuaciones, tabla multipágina, referencias y diagramas monocromáticos.
- Cachés de Luaotfload/TeX aisladas por caso para que las compilaciones paralelas no modifiquen dependencias compartidas. Los fallos inesperados muestran su diagnóstico en CI.
- Compilación limpia en directorios temporales: ningún auxiliar o PDF anterior puede sustituir el nuevo resultado.
- Batería de 41 casos: 23 positivos y 18 negativos. Las pruebas sintéticas no se presentan como contenido de un libro.
- Auditoría de logs, marcadores de contenido, fuentes incrustadas, enlaces internos (incluidos destinos nombrados), texto/vectores/imágenes fuera del papel, color y una prueba de contraste de texto oscuro sobre fondos oscuros.
- Publicación bloqueada si falla un caso o cambian las fuentes después de preparar la compilación.
- CI con imagen TeX por digest, acciones por SHA, sin red en el compilador, sin shell escape y artefacto aprobado separado de diagnósticos.

## Migración

Ver `docs/MIGRACION.md`. No se genera EPUB ni se certifica PDF/X, accesibilidad o impresión física.
