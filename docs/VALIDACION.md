# Contrato de validación 2.2

## Qué se admite

LuaLaTeX, clase memoir, una columna, 6 × 9 pulgadas, español o inglés, cuerpo de 10/11/12 pt, una o dos caras. Perfiles narrativo e ilustrado. Interior monocromático sin sangrado. Imágenes PDF/PNG/JPEG, bibliografía BibLaTeX/Biber y tablas largas correctamente dimensionadas.

## Qué se comprueba

`python3 scripts/build.py --tests` crea 41 casos limpios. `python3 scripts/qa.py` requiere que los 23 positivos compilen y superen el control, y que cada uno de los 18 negativos produzca la detección esperada. Un negativo que solo falle por otro motivo NO aprueba.

Pruebas positivas: ambas cajas de varias páginas; caja al final de página; listas, fórmulas y nota local; cuatro combinaciones de perfil/doble cara; salto antes de ancho extendido; flotantes aplazados; imágenes altas/anchas y pies largos; notas extensas; márgenes pares/impares; tabla de 240 filas; índice con numeración 998–1002; bibliografía e índice alfabético; español/inglés; títulos y caracteres; tamaños 10/12; cajas vacías y carga de 420 páginas más preliminares.

Pruebas negativas: bloque extendido y nota excesivamente altos; nota dentro de caja; anidación de ancho extendido; imagen más ancha que columna/margen; pie excesivo; imagen inexistente; idioma/perfil inválidos; referencia sin resolver; etiqueta duplicada; glifo ausente; línea desbordada; vector fuera del papel; color; título oscuro ilegible; saturación del margen.

El auditor revisa registros finales sin suprimir avisos tipográficos. Analiza límites de texto, vectores e imágenes; fuentes incrustadas; enlaces internos; dimensiones; igualdad RGB del render y contraste en candidatos de texto oscuro sobre fondos oscuros. La prueba de paridad mide reglas vectoriales, no solo cajas de texto.

## Qué NO se demuestra automáticamente

Una batería finita no demuestra ausencia universal de errores. No detecta todas las superposiciones entre objetos, la legibilidad de cada detalle dentro de una foto, exactitud técnica del manuscrito, enlaces web futuros, resolución adecuada para cualquier imprenta, PDF/X, separaciones de tinta, accesibilidad o EPUB. Revisa visualmente el PDF completo y una prueba física antes de una tirada.

Las notas laterales no tienen capacidad infinita. Si se acumulan y LaTeX las desplaza, la auditoría bloquea la publicación; reduce notas, usa pies o reorganiza el texto. Un `fullwidth` no debe compartir su zona exterior con una nota/figura marginal. No se implementa composición automática que resuelva cualquier colisión: esa combinación debe revisarse editorialmente.

## Entorno y confianza

`ci/toolchain.json` fija el contenedor TeX por digest y las acciones por SHA. El runner hospedado y el parche de Python siguen siendo suministrados por GitHub; no se afirma reproducción binaria bit a bit entre plataformas. `.build/environment.txt` registra el motor usado realmente. Cada caso tiene sus propios TEXMFVAR, TEXMFCONFIG y TEXMFCACHE: no comparte cachés escribibles con otras compilaciones paralelas.

El compilador de CI no tiene red y usa `-no-shell-escape`; no se le pasan secretos ni el socket de Docker. Esto reduce exposición, pero no convierte código TeX arbitrario de terceros en contenido confiable. Los scripts del repositorio también se ejecutan: revisa cambios de colaboradores antes de aprobarlos.

Solo `.build/approved/main.pdf` es el artefacto aprobado. Si falla un caso, el workflow conserva diagnósticos y no publica un libro aprobado. Los hashes del manifiesto impiden aprobar fuentes cambiadas desde la preparación. No se reutilizan los auxiliares ni el PDF de un build previo.
