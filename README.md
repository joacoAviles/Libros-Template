# Avia Editorial 2.2

**Libros en español · Blanco y negro · memoir · 6 × 9 pulgadas**

Una plantilla para escribir no ficción, relatos y divulgación con una composición sobria. El texto ocupa el centro del diseño; las notas, diagramas y recuadros deben ayudar a leer, no competir con el libro.

La versión 2.2 corrige los recuadros largos recortados y el ancho extendido que invadía el margen interior en páginas pares. Añade pruebas reproducibles y una barrera de validación: un PDF que termina de compilar no se publica como aprobado si falla los controles.

## Empieza tu libro

Usa **Use this template → Create a new repository**, si está activada esa opción en GitHub. También puedes clonar este proyecto. Cambia título, subtítulo y autor en `main.tex`; escribe en `chapters/` y organiza capítulos con `include`. Tu libro debe tener su propio repositorio.

En cada push y pull request, Actions prepara un entorno limpio, compila el manuscrito y los casos de prueba, y audita los PDF. El resultado aprobado aparece en **Artifacts → avia-editorial-2.2-aprobado**. Los diagnósticos se conservan por separado. La compilación no es una vista previa en vivo.

## Dos perfiles, una base

El predeterminado es `narrative`: columna amplia y notas a pie. Para márgenes ilustrados, antes de cargar `config.tex`:

```latex
\def\AviaProfile{illustrated}
\input{config.tex}
\usepackage{avia-editorial}
```

Español es el idioma inicial. Para inglés define `AviaLanguage` como `english` antes de cargar la configuración. Se prueban 10, 11 y 12 pt, una y dos caras. El motor soportado de esta versión es **LuaLaTeX**.

| Recurso | Uso |
|---|---|
| Nota | `\sidenote{Texto}` |
| Nota de fuente | `\sidecite[detalle]{Fuente}` |
| Figura en columna | `\widefigure{archivo.pdf}{Pie}[fig:clave]` |
| Figura extendida | `\fullwidthfigure{archivo.pdf}{Pie}[fig:clave]` |
| Figura marginal | `\aviamarginfigure{archivo.pdf}{Pie}` |
| Epígrafe | `\chapterquote{Cita}{Autor}` |
| Recuadro divisible | `\begin{insightbox}[Título] ... \end{insightbox}` |
| Recuadro técnico | `\begin{technicalbox}[Título] ... \end{technicalbox}` |

Los pies y etiquetas de figuras son reales y enlazables. Las imágenes conservan su proporción y se limitan a la altura disponible. Los bloques extendidos demasiado altos y otros usos no admitidos se detienen con un error explícito: no se ocultan ni se recortan silenciosamente.

## Compilar y comprobar

Instala TeX Live con LuaLaTeX, Latexmk, Biber, memoir, Babel, fontspec, tcolorbox, TikZ y las demás dependencias del estilo. Python 3.10 o posterior.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-qa.txt
python3 scripts/build.py --tests
.venv/bin/python scripts/qa.py
```

Para compilar solamente tu manuscrito, omite `--tests`. El PDF aprobado se copia a `.build/approved/main.pdf`; el registro y los resultados están en `.build/`. Las 420 páginas de carga son datos sintéticos de prueba, no contenido de ejemplo para rellenar libros.

No uses `main.pdf` antiguo de la raíz como resultado de esta cadena. La preparación elimina `.build` y crea fuentes limpias. Si cambias archivos después de preparar, el auditor exige volver a compilar.

## Qué cambia frente a 2.1

Recuadros multipágina, paridad exterior corregida, portadas sin anclas duplicadas, guardas de figuras y márgenes, índice para páginas de cuatro cifras, fondos blancos explícitos y notas alineadas por arriba. El CI deja de depender de `assets/wing.tex`; el ejemplo conserva ese recurso monocromático por compatibilidad.

Consulta [cambios](CHANGELOG.md), [migración](docs/MIGRACION.md), [alcance de pruebas](docs/VALIDACION.md) y [entorno fijado](ci/toolchain.json).

## Fuentes e inspiración

La clase [memoir](https://ctan.org/pkg/memoir) proporciona la base de composición. [DGrady/book-template](https://github.com/DGrady/book-template) inspiró el enfoque de libro comercial; [Tufte-LaTeX/tufte-latex](https://github.com/Tufte-LaTeX/tufte-latex) inspiró las anotaciones y figuras marginales. No se incluyen las clases originales de Tufte ni se afirma afiliación con esos proyectos.

Las cajas divisibles utilizan [tcolorbox](https://ctan.org/pkg/tcolorbox). El entorno de CI proviene de [latex-docker](https://github.com/xu-cheng/latex-docker), fijado por digest. Las dependencias mantienen sus propias licencias. No se incluyen archivos de fuentes tipográficas.

## Antes de publicar

Esta versión incorpora una batería finita de regresión, no una garantía para cualquier combinación de paquetes y contenido. Revisa el PDF y los requisitos de la imprenta: encuadernación, sangrado, resolución y especificaciones del archivo. Las páginas de respeto de `openright` son intencionales. El margen no tiene capacidad infinita; los casos saturados se rechazan para corregir el manuscrito.

No se certifica PDF/X, accesibilidad ni EPUB. La revisión de contenido y los permisos de materiales de terceros corresponden a cada libro, no a la plantilla. No se concede aquí una nueva licencia sobre aportes previos o materiales ajenos; define la licencia del proyecto con su titular antes de una redistribución comercial.
