# Avia Editorial — memoir + recursos inspirados en Tufte

**Idioma predeterminado: español**, incluido el contenido de ejemplo, guionado, índice, fechas y referencias bibliográficas (Biber).

Plantilla propia para libros de no ficción comercial, divulgación y manuales ilustrados. Se usa la clase `memoir` (no se copia código de Tufte-LaTeX).

## Idioma

La plantilla utiliza `babel` con **español predeterminado** y soporte adicional de inglés. En `config.tex`, `\def\AviaLanguage{spanish}` define el idioma base. Para publicar un libro en inglés cambia ese valor a `english` (y ajusta `pdflang` en `avia-editorial.sty` a `en-US`). Para un párrafo puntual en inglés utiliza `\foreignlanguage{english}{Text in English}`. Las comillas localizadas se manejan con `\enquote{texto}`. Los títulos automáticos como «Índice general», «Capítulo», «Figura» y «Referencias» usan configuración española.

## Empezar

1. Abre `main.tex` y cambia el título, subtítulo y autor.
2. Crea capítulos en `chapters/` con `\\chapter{...}` y añádelos mediante `\\include`.
3. Cambia texto y figuras de demostración. Añade fuentes a `references.bib`.
4. Compila con LuaLaTeX + Biber. Comandos locales:

```bash
cd assets && lualatex -interaction=nonstopmode wing.tex && cd ..
lualatex -interaction=nonstopmode main.tex
biber main
lualatex -interaction=nonstopmode main.tex
lualatex -interaction=nonstopmode main.tex
```

En GitHub, Actions ejecuta la compilación y guarda el PDF en **Actions → Compilar libro → Artifacts**. Editar `.tex` en GitHub funciona, pero GitHub no tiene previsualización WYSIWYG de LaTeX.

## Funciones disponibles

- `\\sidenote{...}`: nota al margen.
- `\\sidecite[detalle]{fuente}`: referencia marginal redactada.
- `\\margintext{...}`: texto lateral.
- `\\aviamarginfigure{archivo}{pie}`: figura al margen.
- `\\widefigure[ancho]{archivo}{pie}`: figura flotante en columna principal.
- `\\fullwidthfigure{archivo}{pie}`: figura usando el margen lateral.
- `\\begin{fullwidth} ... \\end{fullwidth}`: contenido extendido.
- `\\chapterquote{texto}{autor}`: epígrafe.
- `\\opening{texto}`: bajada de apertura.
- `insightbox`: recuadro narrativo.
- `technicalbox`: recuadro técnico.
- `\\textcite{clave}`: cita bibliográfica BibLaTeX.

## Edición e impresión

Dimensiones iniciales: 6 x 9 pulgadas y diseño de una cara (`oneside`); adecuado para prototipos y pruebas. **No es un PDF final certificado para imprenta**: antes de distribuir revisa dimensiones exactas, sangrado, marcas, medianil, lomo, PDF/X, fuentes y especificaciones de la imprenta. En la edición dúplex (`twoside`) debe adaptarse la anchura extendida a cada página par/impar, y probar que notas e ilustraciones se mantengan legibles.

Las notas marginales pueden colisionar si son demasiadas; para libros extensos es importante revisar cada capítulo visualmente. Compilar libros largos es viable; dividir los capítulos reduce el costo de edición y depuración. `\\includeonly{...}` permite compilar solo capítulos seleccionados.

## Límites importantes

- En `config.tex` cambia `\AviaIllustratedtrue` a `\AviaIllustratedfalse` para un bloque de lectura narrativa más ancho. Ambos perfiles necesitan corrección editorial previa a imprenta.
- EPUB no se genera con este pipeline: requiere conversión y validación independientes.
- No se han replicado las macros originales de Tufte-LaTeX ni se garantiza compatibilidad con ese paquete.
- Los manuales no oficiales de aviación deben incluir advertencias y referencias a documentación aprobada por modelo y matrícula.
