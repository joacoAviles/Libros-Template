# Avia Editorial

**Sistema editorial en LaTeX para libros extensos, documentación técnica y publicaciones en español.**

[![Versión editorial](https://img.shields.io/badge/versi%C3%B3n-2.2.0-242424?style=flat-square)](./VERSION)
[![Motor](https://img.shields.io/badge/motor-LuaLaTeX-242424?style=flat-square)](https://www.luatex.org/)
[![Formato](https://img.shields.io/badge/formato-6%C3%979%20pulgadas-242424?style=flat-square)](https://ctan.org/pkg/memoir)
[![Compilación](https://github.com/joacoAviles/Libros-Template/actions/workflows/build.yml/badge.svg)](https://github.com/joacoAviles/Libros-Template/actions/workflows/build.yml)

Avia Editorial es una base reutilizable para componer libros con una identidad visual consistente: tipografía sobria, interior monocromático, márgenes pensados para lectura, figuras, referencias, notas y componentes editoriales. Se apoya en la clase [`memoir`](https://ctan.org/pkg/memoir) y utiliza **LuaLaTeX**, **Latexmk** y **Biber**.

La plantilla es el **sistema de composición**, no el manuscrito de una obra particular. Cada libro debe mantener sus capítulos, referencias, recursos y automatizaciones en su propio repositorio.

> **Versión de la base:** `2.2.0`. El tag Git `v3.0.0` creado en este repositorio no representa una versión 3.0 del motor editorial; el archivo `VERSION` sigue indicando 2.2.0.

## Ejemplos publicados

Aquí puedes revisar dos ejemplos de libros creados con Avia Editorial: **[Manual 1](https://joacoaviles.github.io/Libros-Template/r22/manual-r22.pdf)** y **[Manual 2](https://joacoaviles.github.io/Libros-Template/r22-claude/manual-r22.pdf)**. Ambos muestran cómo integrar textos extensos, gráficos, tablas, imágenes, notas, referencias y distintos recursos de maquetación en un documento editorial.

## Características

| Área | Funcionalidad |
| --- | --- |
| **Composición** | Tamaño de página 6 × 9 pulgadas, tipografía y jerarquía editorial, impresión a una o dos caras |
| **Perfiles** | `narrative` para lectura en columna; `illustrated` para notas y elementos marginales |
| **Contenido** | Capítulos modulares, secciones, tablas, figuras con pies, citas y bibliografía |
| **Recursos visuales** | Figuras normales, extendidas y marginales, con límites de composición |
| **Componentes** | Recuadros técnicos y de información divisibles entre páginas |
| **Idiomas** | Español como idioma predeterminado; inglés configurable |
| **Automatización** | Compilación mediante GitHub Actions y archivo PDF como artefacto |
| **Control de calidad** | Herramientas de regresión, diagnósticos y auditoría editorial en la línea 2.2 |

La compilación y una auditoría editorial completa **no son equivalentes**. Un PDF generado correctamente puede seguir necesitando ajustes de tipografía, referencias, tablas o imágenes.

## Comenzar un libro

1. Revisa la [base editorial 2.2](https://github.com/joacoAviles/Libros-Template/tree/release/2.2). Es la referencia apropiada para iniciar proyectos sin tomar como punto de partida los archivos particulares de los manuales R22 que llegaron a `main`.
2. Crea un repositorio nuevo para tu libro. Puedes usar **Use this template** cuando la rama predeterminada esté depurada, o copiar la base desde `release/2.2` mientras tanto.
3. Personaliza el título, autor, estructura y ajustes en `main.tex`, `config.tex` y los archivos específicos de tu obra.
4. Escribe un archivo `.tex` por capítulo dentro de `chapters/` e inclúyelo desde `main.tex`.
5. Compila, revisa los diagnósticos y publica el PDF desde **el repositorio del libro**.

> **Estado de este repositorio:** su rama `main` aún conserva archivos incorporados desde un manuscrito R22 durante una integración anterior. Este README describe el sistema editorial y enlaza la rama `release/2.2` para recuperar una base independiente. La limpieza del código de `main` es una tarea distinta y no se resuelve cambiando la documentación.

## Estructura del proyecto editorial

```text
.github/workflows/     Automatización de GitHub
assets/                Figuras y recursos de cada proyecto
chapters/              Capítulos independientes en LaTeX
ci/                    Casos y configuración de pruebas
docs/                  Documentación y migración
scripts/               Compilación y auditoría
tests/                 Regresiones editoriales
avia-editorial.sty     Estilos y componentes editoriales
config.tex             Formato, idioma y perfil
main.tex               Documento principal
references.bib         Bibliografía del libro
VERSION                Versión del motor editorial
README.md              Documentación
```

Al crear una obra, el contenido de `assets/`, `chapters/`, `main.tex` y `references.bib` corresponde a **ese libro**. El sistema reutilizable reside principalmente en el estilo, la configuración y las herramientas editoriales.

## Recursos LaTeX

```latex
% Componentes disponibles en Avia Editorial
\sidenote{Una nota de lectura.}
\sidecite[detalle]{Fuente consultada}
\chapterquote{Una cita de apertura}{Autor}

\begin{insightbox}[Concepto]
  Un recuadro informativo que puede dividirse entre páginas.
\end{insightbox}

\begin{technicalbox}[Detalle técnico]
  Información importante, sin depender de franjas de color.
\end{technicalbox}

\widefigure{assets/figura.pdf}{Pie de figura}
\fullwidthfigure{assets/figura.pdf}{Figura extendida}
\aviamarginfigure{assets/figura.pdf}{Figura marginal}
```

Los comandos deben utilizarse en contextos compatibles con sus límites de ancho, altura y página. Algunas figuras extendidas no pueden dividirse libremente; las tablas y bloques complejos requieren diseño apropiado para documentos extensos.

### Perfiles de composición

Define el perfil antes de cargar la configuración:

```latex
\documentclass[11pt,twoside,openright]{memoir}
\def\AviaProfile{narrative} % o illustrated
\def\AviaLanguage{spanish}  % o english
\input{config.tex}
\usepackage{avia-editorial}
```

## Compilación y validación

La línea editorial **2.2** proporciona herramientas de compilación reproducible y controles de calidad. En una copia de la base 2.2 con las dependencias instaladas:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-qa.txt
python3 scripts/build.py --tests
.venv/bin/python scripts/qa.py
```

La compilación local requiere TeX Live con LuaLaTeX, Latexmk, Biber y los paquetes utilizados por el estilo. El flujo de regresión puede producir diagnósticos en `.build/` y guardar un PDF aprobado en `.build/approved/main.pdf` **solo si supera las verificaciones exigidas**.

La rama `main` de este repositorio mantiene actualmente un workflow básico `Compilar libro` que genera `main.pdf` y lo sube como artefacto `avia-editorial-pdf`; no debe confundirse con la cadena estricta de auditoría de `release/2.2`.

- [Historial de compilaciones](https://github.com/joacoAviles/Libros-Template/actions)
- [Guía de validación](https://github.com/joacoAviles/Libros-Template/blob/release/2.2/docs/VALIDACION.md)
- [Guía de migración](https://github.com/joacoAviles/Libros-Template/blob/release/2.2/docs/MIGRACION.md)
- [Registro de cambios](https://github.com/joacoAviles/Libros-Template/blob/release/2.2/CHANGELOG.md)

## Relación entre plantilla y libros

```text
                 AVIA EDITORIAL
            Plantilla y herramientas
                       |
            +----------+----------+
            |                     |
         R22-GPT              R22-Claude
      Manuscrito propio     Manuscrito propio
            |                     |
       PDF de lectura       PDF de lectura
            |                     |
            +----------+----------+
                       |
             Libros-Template
             gh-pages / PDF
            (solo ejemplos)
```

Los PDF de demostración se publican en rutas separadas. No se deben sincronizar capítulos, macros específicas, bibliografías ni archivos `README.md` de los libros hacia la plantilla.

## Alcance y créditos

Avia Editorial utiliza [memoir](https://ctan.org/pkg/memoir) como base de composición. Su enfoque visual toma referencias de [DGrady/book-template](https://github.com/DGrady/book-template) y [Tufte-LaTeX](https://github.com/Tufte-LaTeX/tufte-latex), sin implicar afiliación o aprobación de estos proyectos.

La plantilla **no certifica** exactitud técnica, conformidad aeronáutica, accesibilidad, PDF/X, condiciones de imprenta ni derechos de publicación de materiales de terceros. Cada obra es responsable de validar su contenido, sus fuentes y sus permisos de distribución.

---

**Avia Editorial** · Un sistema de composición reutilizable. Cada libro, un proyecto independiente.
