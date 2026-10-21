# Avia Editorial

**Plantilla abierta de libros en LaTeX · Español por defecto · `memoir` · Formato 6 × 9 pulgadas**

Un punto de partida para libros de no ficción, relatos, divulgación y manuales didácticos. Busca el equilibrio entre la legibilidad de un libro comercial y algunos recursos de las ediciones ilustradas: márgenes con notas, epígrafes, figuras y recuadros discretos.

**Filosofía:** más carácter editorial que una plantilla mínima; menos ornamentación y menos interrupciones que un libro de estilo Tufte estricto. Las páginas deben seguir siendo fáciles de leer.

## Crea tu libro

1. En este repositorio, elige **Use this template → Create a new repository** (una vez activado **Template repository** en **Settings → General**).
2. Elige el nombre de tu libro y crea el nuevo repositorio.
3. Edita `main.tex`: título, subtítulo, autor y capítulos.
4. Escribe en `chapters/` y registra cada capítulo con `\include{chapters/nombre}`.
5. Haz commit. GitHub Actions compila automáticamente y deja `main.pdf` descargable en **Actions → Compilar libro → Artifacts**.

También puedes editar directamente archivos `.tex` desde la interfaz web de GitHub. GitHub no ofrece vista previa LaTeX en vivo.

## Lo que viene incluido

| Recurso | Sintaxis |
| --- | --- |
| Nota marginal | `\sidenote{Una observación}` |
| Texto lateral | `\margintext{Texto adicional}` |
| Fuente comentada | `\sidecite[detalle]{Fuente}` |
| Figura al margen | `\aviamarginfigure{archivo.pdf}{Pie}` |
| Figura tradicional | `\widefigure{archivo.pdf}{Pie}` |
| Figura extendida | `\fullwidthfigure{archivo.pdf}{Pie}` |
| Epígrafe | `\chapterquote{Cita}{Autor}` |
| Frase de apertura | `\opening{Texto}` |
| Recuadro de concepto | `\begin{insightbox}[Título] ... \end{insightbox}` |
| Recuadro técnico | `\begin{technicalbox}[Título] ... \end{technicalbox}` |
| Referencia bibliográfica | `\textcite{clave}` |

- **Idioma:** español (`babel`) por defecto; inglés disponible como segundo idioma.
- **Formato:** 6 × 9 pulgadas, apropiado como base para libros comerciales.
- **Motor:** LuaLaTeX; bibliografía con Biber.
- **Perfiles:** `\AviaIllustratedtrue` (márgenes amplios) o `\AviaIllustratedfalse` (texto más ancho) en `config.tex`.
- **Capítulos:** independientes para facilitar la escritura de obras largas.

## Estructura

```text
Libros-Template/
├── .github/workflows/build.yml  # PDF automático en GitHub
├── chapters/                    # Un archivo .tex por capítulo
├── assets/                      # Imágenes e ilustraciones
├── main.tex                     # Portada, autor y orden de capítulos
├── config.tex                   # Idioma, formato y perfiles
├── avia-editorial.sty           # Sistema editorial reutilizable
├── references.bib               # Fuentes bibliográficas
└── README.md
```

## Compilar en tu computador

Instala TeX Live (incluyendo LuaLaTeX, Biber y Latexmk). Desde la raíz del repositorio:

```bash
cd assets && lualatex -interaction=nonstopmode -halt-on-error wing.tex && cd ..
latexmk -lualatex -interaction=nonstopmode -halt-on-error main.tex
```

La compilación local y la de GitHub son equivalentes en su objetivo, aunque el entorno de paquetes puede variar. Para archivos `.bib`, `latexmk` invoca Biber cuando corresponde.

## Inspiración y créditos

Esta plantilla usa la clase [`memoir`](https://ctan.org/pkg/memoir). El diseño se desarrolló específicamente para **Avia Editorial**; no se incluye ninguna clase o macro original del repositorio Tufte.

- **[DGrady/book-template](https://github.com/DGrady/book-template)**: referencia principal para la tipografía de libro, tamaño comercial de 6 × 9 pulgadas, márgenes orientados a encuadernación y la clase `memoir`.
- **[Tufte-LaTeX/tufte-latex](https://github.com/Tufte-LaTeX/tufte-latex)**: inspiración visual para anotaciones marginales, figuras fuera de la columna principal y una segunda capa de lectura.
- **[CTAN memoir](https://ctan.org/pkg/memoir)**: documentación técnica de la clase de composición.

Estas referencias son atribuciones de inspiración, no una afiliación o aprobación por sus autores. Sus licencias respectivas aplican a su código original.

## Publicación y límites

Esta edición es una **base para escritura y pruebas**, no un PDF certificado para imprenta. Antes de imprimir revisa sangrado, márgenes interiores, fuentes, calidad de ilustraciones, grosor del volumen y el perfil requerido por la imprenta. El prototipo utiliza `oneside`; para producción a doble cara hay que revisar los márgenes par/impar y las notas laterales. Las notas pueden solaparse si se concentran en un mismo tramo.

EPUB requiere un flujo de exportación separado. En contenidos aeronáuticos, un manual no oficial no reemplaza los documentos aprobados aplicables a la aeronave.
