# Migrar desde 2.1

Conserva una copia o commit de tu libro. Reemplaza `avia-editorial.sty` y `config.tex` juntos; no mezcles versiones. Mantén tus capítulos, imágenes y bibliografía. Compara el PDF anterior y el nuevo: corregir composición puede cambiar la paginación.

```latex
\documentclass[11pt,twoside,openright]{memoir}
% Opcional, ANTES de input:
% \def\AviaProfile{illustrated}
% \def\AviaLanguage{english}
\input{config.tex}
\usepackage{avia-editorial}
```

El perfil por defecto es `narrative`: las notas pasan al pie. El perfil `illustrated` habilita el margen. No cambies `AviaIllustratedtrue` después de calcular los márgenes; selecciona `AviaProfile` antes de cargar config.

Retira de los ajustes del libro únicamente los parches genéricos que ahora incorpora 2.2: `tcbset{breakable}`, alias de páginas de capítulo, anchos del índice y redefiniciones de `fullwidth`. Conserva los metadatos, macros de contenido, bibliografía, tablas y diagramas propios. Si cargabas Babel previamente, declara ambos idiomas: `[english,spanish,es-tabla]`.

Los comandos 2.1 se conservan, salvo comportamientos inseguros ahora rechazados. `fullwidth` es un bloque indivisible de una sola página; para texto extenso usa un recuadro normal divisible. No coloques notas marginales dentro de cajas ni bloques extendidos. Las figuras extendidas tienen ahora numeración y pie real; revisa referencias manuales que dependieran del antiguo pie sin número.

```latex
\widefigure{assets/foto.pdf}{Pie explicativo.}[fig:foto]
\fullwidthfigure{assets/diagrama.pdf}{Diagrama a ancho exterior.}[fig:diagrama]
```

No coloques `footnote` dentro de un pie: escribe la nota en el cuerpo. Evita líneas literales indivisibles; usa `url`/`path` para direcciones. Tablas anchas necesitan columnas con anchos adecuados y, si continúan, `longtable`. No se reduce automáticamente texto hasta hacerlo ilegible.

La prueba privada del R22 usa los mismos capítulos, no un libro reescrito para pasar. Ese manuscrito y las imágenes de terceros no forman parte del repositorio público.
