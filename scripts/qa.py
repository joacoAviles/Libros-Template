#!/usr/bin/env python3
"""Fail-closed LaTeX/PDF regression checks; requires PyMuPDF==1.26.7.
Only a fully passing run creates .build/approved/main.pdf.
"""
from __future__ import annotations
import argparse, hashlib, json, re, shutil
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1]
PATTERNS={
 'OVERFULL':r'Overfull \\[hv]box','UNDERFULL':r'Underfull \\[hv]box',
 'UNRESOLVED':r"(?:Reference|Citation) .+ undefined|undefined references|undefined citations|Please \(re\)run Biber",
 'DUPLICATE':r'multiply[- ]defined|multiply defined|destination with the same identifier|duplicate destination',
 'MISSING_GLYPH':r'Missing character:',
 'FONT_SUBSTITUTION':r'Font shape .* not available|font shapes were not available|Size substitutions',
 'MARGIN_COLLISION':r'Marginpar .*moved|Too many unprocessed floats',
 'MISSING_IMAGE':r"File .*does-not-exist.*not found",
 'RERUN':r'Rerun to get|Rerun LaTeX|Please rerun LaTeX'}

def log_errors(log):
    found=[name for name,pat in PATTERNS.items() if re.search(pat,log,re.I)]
    found+=sorted(set(re.findall(r'AVIA-E-[A-Z-]+',log)))
    if re.search(r'(?:LaTeX|Package \S+|Class \S+|LaTeX Font) Warning:',log):found.append('LOG_WARNING')
    if re.search(r'! (?:LaTeX|Package|Class)|Fatal error occurred|Emergency stop',log):found.append('TEX_ERROR')
    return sorted(set(found))

def inside(rect,page,tol=.6):
    return rect.x0>=page.x0-tol and rect.y0>=page.y0-tol and rect.x1<=page.x1+tol and rect.y1<=page.y1+tol

def audit_pdf(path,case):
    errors=[];detail=dict(pages=0,internal_links=0,external_links=0,fonts=0,non_mono_pages=[],outside=[],low_contrast=[],geometry=[])
    if not path.exists():return ['NO_PDF'],detail
    try:pdf=fitz.open(path)
    except Exception as exc:return ['INVALID_PDF'],dict(error=str(exc),pages=0)
    detail['pages']=len(pdf)
    if len(pdf)<case.get('min_pages',1):errors.append('TOO_FEW_PAGES')
    text=[];fonts={}
    for pn,page in enumerate(pdf,1):
        r=page.rect
        if abs(r.width-432)>.1 or abs(r.height-648)>.1:errors.append('PAGE_SIZE')
        text.append(page.get_text(sort=True))
        spans=[s for b in page.get_text('dict')['blocks'] if b.get('type')==0 for l in b['lines'] for s in l['spans'] if s['text'].strip()]
        for sp in spans:
            if not inside(fitz.Rect(sp['bbox']),r):
                errors.append('OUTSIDE_TEXT');detail['outside'].append(dict(page=pn,type='text',text=sp['text'][:80],rect=list(sp['bbox'])))
        drawings=page.get_drawings()
        for dr in drawings:
            if not inside(dr['rect'],r):
                errors.append('OUTSIDE_VECTOR');detail['outside'].append(dict(page=pn,type='vector',rect=list(dr['rect'])))
        # Candidate spans covered by a dark frame/background; the render resolves
        # white inner fills painted over that frame (rectangles alone are insufficient).
        contrast_candidates=[]
        for sp in spans:
            col=sp['color'];lum=((col>>16&255)+(col>>8&255)+(col&255))/(3*255)
            if lum<.25 and sp['size']>=7 and len(sp['text'].strip())>=4 and any(
                dr.get('fill') is not None and sum(dr['fill'])/len(dr['fill'])<.35
                and dr['rect'].contains((fitz.Rect(sp['bbox']).tl+fitz.Rect(sp['bbox']).br)/2) for dr in drawings):
                contrast_candidates.append(sp)
        for img in page.get_image_info():
            if not inside(fitz.Rect(img['bbox']),r):errors.append('OUTSIDE_IMAGE')
        for f in page.get_fonts(full=True):
            if f[0]:fonts[f[0]]=f
        for link in page.get_links():
            if link['kind'] in (fitz.LINK_GOTO,fitz.LINK_NAMED) and (link['kind']==fitz.LINK_GOTO or 'nameddest' in link):
                detail['internal_links']+=1
                if not 0<=link.get('page',-1)<len(pdf):errors.append('BROKEN_LINK')
            elif link['kind']==fitz.LINK_URI:detail['external_links']+=1
        pix=page.get_pixmap(matrix=fitz.Matrix(1,1),colorspace=fitz.csRGB,alpha=False)
        sample=pix.samples
        for sp in contrast_candidates:
            box=fitz.Rect(sp['bbox']) & r
            x0,x1=max(0,int(box.x0)),min(pix.width,int(box.x1)+1)
            y0,y1=max(0,int(box.y0+.18*box.height)),min(pix.height,int(box.y1-.12*box.height)+1)
            values=[]
            for y in range(y0,y1,2):
                values.extend(sample[y*pix.stride+3*x0:y*pix.stride+3*x1:6])
            if values and sum(v>190 for v in values)/len(values)<.15:
                errors.append('LOW_CONTRAST');detail['low_contrast'].append(dict(page=pn,text=sp['text'][:80]))
        if sample[::3]!=sample[1::3] or sample[1::3]!=sample[2::3]:
            errors.append('NON_MONO');detail['non_mono_pages'].append(pn)
        if case.get('geometry'):
            normal=[d['rect'] for d in drawings if 190<d['rect'].width and .3<(d['rect'].height or d.get('width',0))<.6]
            wide=[d['rect'] for d in drawings if 190<d['rect'].width and .8<(d['rect'].height or d.get('width',0))<1.2]
            if not normal or not wide:errors.append('GEOMETRY_MISSING');continue
            n,w=normal[0],wide[0];one='oneside' in case['name']
            alignment=abs(w.x0-n.x0) if one or pn%2 else abs(w.x1-n.x1)
            okay=(alignment<.8 and w.width>n.width+15 and w.x0>=18 and w.x1<=414)
            detail['geometry'].append(dict(page=pn,normal=list(n),extended=list(w),correct=okay))
            if not okay:errors.append('WRONG_OUTER_MARGIN')
    for xref in fonts:
        try:
            if not pdf.extract_font(xref)[3]:errors.append('UNEMBEDDED_FONT')
        except Exception:errors.append('UNEMBEDDED_FONT')
    detail['fonts']=len(fonts)
    alltext='\n'.join(text).replace('\u00ad','')
    missing=[m for m in case.get('markers',[]) if not re.search(re.escape(m),alltext)]
    if missing:errors.append('MISSING_CONTENT')
    detail['missing_markers']=missing
    detail['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    pdf.close()
    return sorted(set(errors)),detail

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,default=ROOT/'.build/manifest.json')
    args=parser.parse_args();manifest=json.loads(args.manifest.read_text(encoding='utf-8'))
    build=args.manifest.resolve().parent;approved=build/'approved'
    if approved.exists():shutil.rmtree(approved)
    results=[]
    changed=[name for name,digest in manifest['source_hashes'].items()
             if not (ROOT/name).is_file() or hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest]
    if changed:
        print('SOURCE_CHANGED: prepare and compile again: '+', '.join(changed))
        (build/'qa.json').write_text(json.dumps({'version':'2.2.0','passed':False,'error':'SOURCE_CHANGED','files':changed},indent=2))
        return 1
    for case in manifest['cases']:
        d=ROOT/case['directory']
        log=(d/'main.log').read_text(encoding='utf-8',errors='replace') if (d/'main.log').exists() else ''
        code=int((d/'exit-code.txt').read_text().strip()) if (d/'exit-code.txt').exists() else -1
        le=log_errors(log)
        if code!=0:le.append('COMPILER_EXIT')
        expected=case.get('expected')
        pe,detail=audit_pdf(d/'main.pdf',case) if code==0 else ([],dict(pages=None))
        errors=sorted(set(le+pe));passed=(expected in errors) if expected else not errors
        result=dict(name=case['name'],expected_rejection=expected,passed=passed,compiler_exit=code,detected=errors,**detail)
        results.append(result)
        print(('PASS ' if passed else 'FAIL ')+case['name']+(' ['+', '.join(errors)+']' if errors else ''),flush=True)
    report=dict(version=manifest['version'],cases=len(results),passed=sum(r['passed'] for r in results),
                positive_cases=sum(not r['expected_rejection'] for r in results),negative_cases=sum(bool(r['expected_rejection']) for r in results),
                results=results,source_hashes=manifest['source_hashes'],scope='Layout regression, not print/accessibility/content certification.')
    (build/'qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# Avia Editorial 2.2.0: resultados automáticos','',f"Casos aprobados: {report['passed']}/{report['cases']}.",'',
           '| Caso | Resultado | Páginas | Detecciones |','|---|---|---:|---|']
    for r in results:lines.append(f"| {r['name']} | {'OK' if r['passed'] else 'FALLO'} | {r['pages'] if r['pages'] is not None else '—'} | {', '.join(r['detected']) or 'Ninguna'} |")
    lines+=['','Los casos `reject-` solo aprueban cuando el defecto intencionado es detectado. Sus PDF no se publican como aprobados.',
            'Estos controles no prueban legibilidad de imágenes, exactitud del texto ni todas las posibles colisiones gráficas. Se requiere revisión visual y de imprenta.']
    (build/'qa.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    if report['passed']!=report['cases']:return 1
    approved.mkdir()
    for name in ['qa.md','qa.json','environment.txt']:
        if (build/name).exists():shutil.copy2(build/name,approved/name)
    demo=next((c for c in manifest['cases'] if c['name']=='demo'),None)
    if demo:shutil.copy2(ROOT/demo['directory']/'main.pdf',approved/'main.pdf')
    return 0
if __name__=='__main__':raise SystemExit(main())
