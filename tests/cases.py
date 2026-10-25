"""Deterministic editorial regression cases. Synthetic text is test data, not a book."""
from pathlib import Path

PARA = ('La prueba verifica la continuidad de la explicación y la composición del texto. '
        'Cada párrafo tiene una marca independiente para detectar pérdidas, recortes o duplicaciones. '
        'La extensión del caso es una carga sintética, no una medida de calidad editorial. ')

def paragraph(n, prefix='T'):
    return f'\\noindent {prefix}{n:04d}. '+PARA+'\n\n'

def doc(body, profile='narrative', options='11pt,twoside,openany', extra='', language='spanish'):
    return (rf'\documentclass[{options}]{{memoir}}'+'\n'+
            rf'\def\AviaProfile{{{profile}}}\def\AviaLanguage{{{language}}}'+'\n'+
            '\\input{config.tex}\n\\usepackage{avia-editorial}\n'
            '\\usepackage{amsmath,amssymb,longtable,booktabs,array}\n'+extra+
            '\n\\begin{document}\n'+body+'\n\\end{document}\n')

def cases(stress_pages=420):
    out=[]
    def add(name, body, *, expected=None, marks=(), min_pages=1, geometry=False, **kw):
        out.append(dict(name=name,tex=doc(body,**kw),expected=expected,
                        markers=list(marks),min_pages=min_pages,geometry=geometry))
    for kind,num in [('technicalbox',17),('insightbox',90)]:
        text=''.join(paragraph(i,'B') for i in range(1,num+1))
        add('box-'+kind, '\\begin{'+kind+'}[Explicación extensa y título legible]\n'+text+
            '\\end{'+kind+'}\nFINALCAJA', marks=[f'B{i:04d}' for i in range(1,num+1)]+['FINALCAJA'], min_pages=2)
    add('box-near-bottom', paragraph(1)+r'\vspace{.55\textheight}'+
        r'\begin{technicalbox}[Continuación sin pérdida]'+
        ''.join(paragraph(i,'C') for i in range(1,32))+r'\end{technicalbox}',
        marks=[f'C{i:04d}' for i in range(1,32)], min_pages=3)
    add('boxes-list-math-footnote',r'''
\begin{insightbox}[Una explicación con una nota]
Texto con una nota local.\footnote{NOTACAJA: permanece dentro del recuadro.}
\begin{enumerate}\item Primera condición.\item Segunda condición.\end{enumerate}
\[E=\frac{1}{2}mv^2\]
\begin{technicalbox}[Caja breve anidada]Una aclaración acotada.\end{technicalbox}
\end{insightbox}
FINMIXTO''', marks=['NOTACAJA','FINMIXTO'])
    rules=r'''\noindent Columna de lectura.\par\noindent\rule{\linewidth}{.4pt}
\begin{fullwidth}\noindent Bloque extendido.\par\noindent\rule{\linewidth}{1pt}\end{fullwidth}
'''
    for p in ['narrative','illustrated']:
        for side in ['oneside','twoside']:
            add('wide-'+p+'-'+side, rules+r'\newpage'+rules+r'\newpage'+rules,
                profile=p,options=f'11pt,{side},openany',min_pages=3,geometry=True)
    add('wide-after-pagebreak',paragraph(1)+r'\vspace{.75\textheight}'+
        r'\begin{fullwidth}\noindent BLOQUEFINAL\par\rule{\linewidth}{1pt}\par '+PARA*2+r'\end{fullwidth}',
        profile='illustrated',marks=['BLOQUEFINAL'],min_pages=2)
    add('wide-deferred-floats',r'''
\noindent Comienzo del ensayo de flotantes aplazados.
\vspace{.70\textheight}
\fullwidthfigure{assets/tall.pdf}{Figura aplazada con pie numerado.}[fig:late]
'''+''.join(paragraph(i,'D') for i in range(1,18))+r'''
\clearpage
\fullwidthfigure{assets/wide.pdf}{Segunda figura aplazada.}[fig:lateb]
Véanse las figuras~\ref{fig:late} y~\ref{fig:lateb}. FINFLOTANTES
''', profile='illustrated',marks=['FINFLOTANTES']+[f'D{i:04d}' for i in range(1,18)],min_pages=4)
    add('figures-aspect-and-caption',r'''
\widefigure{assets/tall.pdf}{Una imagen muy alta no invade el pie.}[fig:tall]
\widefigure{assets/wide.pdf}{Una imagen muy ancha conserva sus proporciones.}[fig:wide]
\aviamarginfigure{assets/square.pdf}{En el perfil narrativo esta imagen ocupa la columna.}
'''+r'\fullwidthfigure{assets/square.pdf}{'+PARA*3+r'}[fig:caption]'+r'''
\clearpage
Las figuras~\ref{fig:tall}, \ref{fig:wide} y~\ref{fig:caption} tienen destinos distintos. FINFIGURAS
''',marks=['FINFIGURAS'],min_pages=3)
    add('footnotes-long',r'Una nota extensa.\sidenote{NOTALARGA '+PARA*14+' FINNOTA}'+
        ''.join(paragraph(i,'N') for i in range(1,18)),marks=['NOTALARGA','FINNOTA']+[f'N{i:04d}' for i in range(1,18)],min_pages=3)
    margin=[]
    for i in range(1,5):
        margin.append(r'\noindent Texto de la página '+str(i)+r'.\sidenote{MN'+str(i)+' Breve definición.}\n'.replace('\\n','\n'))
        margin.append(PARA*3+r'\par\vspace{22mm}')
        margin.append(r'\aviamarginfigure{assets/square.pdf}{MI'+str(i)+' Forma geométrica.}\n'.replace('\\n','\n')+PARA*2)
        if i<4:margin.append(r'\newpage')
    add('margin-notes-both-sides','\n'.join(margin),profile='illustrated',
        marks=['MN'+str(i) for i in range(1,5)]+['MI'+str(i) for i in range(1,5)],min_pages=4)
    table=r'''\small\begin{longtable}{@{}p{.17\linewidth}p{.74\linewidth}@{}}
\caption{Tabla multipágina.}\label{tab:long}\\
\toprule Código & Descripción\\\midrule\endfirsthead
\toprule Código & Descripción (continuación)\\\midrule\endhead
\bottomrule\endfoot
'''
    for i in range(1,241):
        table+=f'R{i:04d} & Se verifica la continuidad de esta fila y su separación respecto de las filas contiguas.\\\\\n'
    table+=r'\end{longtable}\normalsize Referencia a la tabla~\ref{tab:long}. FINTABLA'
    add('table-240-rows',table,marks=[f'R{i:04d}' for i in range(1,241)]+['FINTABLA'],min_pages=8)
    add('toc-four-digits',r'''
\frontmatter\tableofcontents*\mainmatter\setcounter{page}{998}
\chapter{Una apertura de capítulo con un título largo pero compuesto dentro de la página}
\section{Una sección cuya numeración debe dejar sitio al título y a la página de cuatro cifras}
Contenido de prueba.\newpage\noindent Página adicional.\newpage
\chapter{Continuidad del índice} \section{Última sección} FININDICE
''',marks=['FININDICE'],min_pages=4)
    add('bibliography-index-links',r'''
\frontmatter\tableofcontents*\mainmatter
\chapter{Citas e índice alfabético}\label{ch:citas}
Una referencia a \textcite{lamport1994}.\index{Composición}
La sección~\ref{ch:citas} enlaza con este capítulo.\index{Referencias}
\sidecite[Ejemplo de atribución]{Fuente comentada}
\backmatter\printbibliography[heading=bibintoc]\printindex
''',extra=r'''
\usepackage[backend=biber,style=authoryear]{biblatex}
\addbibresource{references.bib}\AtBeginBibliography{\raggedright}
\makeindex
''',marks=['Lamport'],min_pages=3)
    add('language-english',r'''
\title{A restrained book design}\booksubtitle{English language test}\author{Avia Editorial}
\frontmatter\aviatitlepage\tableofcontents*\mainmatter\chapter{Reading and checking}
English text with an inline note.\sidenote{Footnote in English.}
\begin{technicalbox}[A white heading]Black text remains readable.\end{technicalbox}
ENDENGLISH
''',language='english',marks=['ENDENGLISH','Contents'])
    add('spanish-characters-and-title',r'''
\title{Un libro de lectura, explicaciones técnicas y decisiones editoriales para lectores curiosos}
\booksubtitle{Prueba de títulos largos y caracteres del español}
\author{María José Muñoz}
\frontmatter\aviatitlepage\mainmatter
\chapter{Acentuación, signos y ecuaciones}
¿Árbol, pingüino, acción y niño? Sí: á é í ó ú ü ñ Á É Í Ó Ú Ü Ñ. Euros: 25 €.
\chapterquote{Una explicación que permanece junto a su contexto y no divide palabras.}{Autor de prueba}
\[\alpha+\beta=\gamma,\quad x\in\mathbb{R},\quad\sum_{i=1}^{n}i=\frac{n(n+1)}{2}\]
FINESPANOL
''',marks=['FINESPANOL','pingüino','Muñoz'])
    for size in [10,12]:
        add('font-size-'+str(size),r'\chapter{Prueba de cuerpo tipográfico}'+PARA*6+
            r'\begin{insightbox}[Un recuadro]'+PARA+r'\end{insightbox}', options=f'{size}pt,twoside,openright')
    add('empty-boxes',r'\chapter{Recursos vacíos}' + r'\begin{technicalbox}\end{technicalbox}' +
        r'\begin{insightbox}[Título sin contenido]\end{insightbox}'+r'\noindent FINVACIO',marks=['FINVACIO'])
    # A large document is explicitly synthetic. Every page has a unique marker.
    stress=[r'\frontmatter\tableofcontents*\mainmatter']
    for i in range(1,stress_pages+1):
        if (i-1)%35==0:stress.append(r'\chapter{Carga sintética '+str((i-1)//35+1)+'}')
        else:stress.append(r'\newpage')
        stress.append(f'\\noindent S{i:04d}. Página de carga de maquetación.\n\n'+PARA*2)
        mode=i%5
        if mode==0:stress.append(r'\begin{technicalbox}[Bloque de control]'+PARA+r'\end{technicalbox}')
        elif mode==1:stress.append(r'\section{Lectura y continuidad}'+PARA)
        elif mode==2:stress.append(r'Una nota adicional.\sidenote{Nota de la página de prueba '+str(i)+'.}'+PARA)
        elif mode==3:stress.append(r'\[P=\frac{E}{t},\qquad a^2+b^2=c^2\]'+PARA)
        else:stress.append(r'\begin{center}\begin{tabular}{ll}\toprule Clave & Valor\\\midrule A & 120\\ B & 240\\\bottomrule\end{tabular}\end{center}'+PARA)
    stress.append(r'\par FINESTRES')
    add('stress-'+str(stress_pages),'\n'.join(stress),marks=[f'S{i:04d}' for i in range(1,stress_pages+1)]+['FINESTRES'],min_pages=stress_pages)
    # Deliberately invalid uses: each must fail for the specified reason.
    add('reject-wide-block-too-high',r'\begin{fullwidth}\rule{20pt}{2\textheight}\end{fullwidth}',expected='AVIA-E-WIDE-HEIGHT')
    add('reject-margin-too-high',r'\sidenote{'+PARA*10+'}',profile='illustrated',expected='AVIA-E-MARGIN-HEIGHT')
    add('reject-margin-in-box',r'\begin{insightbox}Texto.\sidenote{Nota incompatible.}\end{insightbox}',profile='illustrated',expected='AVIA-E-MARGIN-CONTEXT')
    add('reject-nested-wide',r'\begin{fullwidth}\begin{fullwidth}Texto\end{fullwidth}\end{fullwidth}',expected='AVIA-E-NESTED-WIDE')
    add('reject-image-width',r'\widefigure[2\linewidth]{assets/square.pdf}{Pie}',expected='AVIA-E-IMAGE-WIDTH')
    add('reject-margin-image-width',r'\aviamarginfigure[2\marginparwidth]{assets/square.pdf}{Pie}',profile='illustrated',expected='AVIA-E-IMAGE-WIDTH')
    add('reject-caption-too-high',r'\widefigure{assets/square.pdf}{'+PARA*30+'}',expected='AVIA-E-CAPTION-HEIGHT')
    add('reject-missing-image',r'\widefigure{assets/does-not-exist.pdf}{Pie}',expected='MISSING_IMAGE')
    add('reject-language',r'Texto.',language='unknown',expected='AVIA-E-LANGUAGE')
    add('reject-profile',r'Texto.',profile='unknown',expected='AVIA-E-PROFILE')
    add('reject-reference',r'La referencia~\ref{no-existe} no tiene destino.',expected='UNRESOLVED')
    add('reject-duplicate-label',r'\chapter{Uno}\label{dup}\chapter{Dos}\label{dup}',expected='DUPLICATE')
    add('reject-missing-glyph',r'Glifo sin soporte: '+chr(0x1F984),expected='MISSING_GLYPH')
    add('reject-unbreakable-line',r'\noindent\mbox{'+('TextoMuyLargo'*40)+'}',expected='OVERFULL')
    add('reject-outside-vector',r'\noindent\makebox[0pt][l]{\hspace{\paperwidth}\rule{20pt}{20pt}}Texto.',expected='OUTSIDE_VECTOR')
    add('reject-color',r'\textcolor{red}{Texto de color en interior monocromático.}',expected='NON_MONO')
    add('reject-dark-heading',r'\begin{tcolorbox}[colback=white,colbacktitle=black,coltitle=black,title=Ilegible]Texto.\end{tcolorbox}',expected='LOW_CONTRAST')
    crowded='\n'.join(r'Nota '+str(i)+r'.\sidenote{'+PARA+'}' for i in range(20))
    add('reject-crowded-margin',crowded,profile='illustrated',expected='MARGIN_COLLISION')
    return out
