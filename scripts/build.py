#!/usr/bin/env python3
"""Stage clean builds, prepare reproducible tests, and invoke LuaLaTeX.
Run from the repository root: python3 scripts/build.py [--tests] [--prepare-only].
Does not approve PDFs. Run scripts/qa.py after compilation.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, shutil, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BUILD=ROOT/'.build'

def shape_pdf(path: Path,w: int,h: int)->None:
    """A font-free monochrome vector fixture, independent of external assets."""
    stream=f'0 G 0.7 w 1 1 {w-2} {h-2} re S 0.7 g {w/4:g} {h/4:g} {w/2:g} {h/2:g} re f 0 G 0 0 m {w} {h} l S\n'.encode()
    objects=[b'<< /Type /Catalog /Pages 2 0 R >>',b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
             f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {w} {h}] /Resources << >> /Contents 4 0 R >>'.encode(),
             b'<< /Length '+str(len(stream)).encode()+b' >>\nstream\n'+stream+b'endstream']
    data=b'%PDF-1.4\n'; offsets=[0]
    for i,obj in enumerate(objects,1):
        offsets.append(len(data));data+=f'{i} 0 obj\n'.encode()+obj+b'\nendobj\n'
    start=len(data);data+=f'xref\n0 {len(objects)+1}\n0000000000 65535 f \n'.encode()
    for off in offsets[1:]:data+=f'{off:010d} 00000 n \n'.encode()
    data+=f'trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{start}\n%%EOF\n'.encode()
    path.write_bytes(data)

def copy_project(dest: Path)->None:
    dest.mkdir(parents=True)
    # Source-only staging: no old .aux/.log/main.pdf can masquerade as a new build.
    for src in ROOT.rglob('*'):
        rel=src.relative_to(ROOT)
        if any(p.startswith('.') or p in {'tests','scripts','docs','evidence','__pycache__'} for p in rel.parts):continue
        if src.is_symlink():raise RuntimeError(f'Symlink not allowed in build input: {rel}')
        if src.is_file() and (src.suffix in {'.tex','.sty','.bib','.cls','.png','.jpg','.jpeg'} or
                             src.suffix=='.pdf' and rel.parts[0]=='assets'):
            target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,target)

def prepare(with_tests:bool,stress_pages:int)->dict:
    if BUILD.is_symlink():raise RuntimeError('Refusing symlink .build')
    if BUILD.exists():shutil.rmtree(BUILD)
    BUILD.mkdir()
    entries=[dict(name='demo',expected=None,markers=[],min_pages=8,geometry=False)]
    if with_tests:
        spec=importlib.util.spec_from_file_location('cases',ROOT/'tests/cases.py')
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        entries+=mod.cases(stress_pages)
    for item in entries:
        stage=BUILD/'cases'/item['name'];copy_project(stage)
        assets=stage/'assets';assets.mkdir(exist_ok=True)
        for name,w,h in [('tall',80,640),('wide',640,80),('square',220,220)]:shape_pdf(assets/(name+'.pdf'),w,h)
        tex=item.pop('tex',None)
        if tex is not None:(stage/'main.tex').write_text(tex,encoding='utf-8')
        item['directory']=str(stage.relative_to(ROOT))
    manifest={'version':'2.2.0','root':'.','cases':entries,'source_hashes':{
        str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(ROOT.rglob('*')) if p.is_file() and not any(
            q.startswith('.') or q in {'__pycache__','evidence'} for q in p.relative_to(ROOT).parts)
        and p.suffix in {'.tex','.sty','.bib','.cls','.py','.sh','.pdf','.png','.jpg','.jpeg'}
        and (p.suffix!='.pdf' or p.relative_to(ROOT).parts[0]=='assets')}}
    (BUILD/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (BUILD/'plan.tsv').write_text(''.join(c['name']+'\t'+c['directory']+'\n' for c in entries),encoding='utf-8')
    return manifest

def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tests',action='store_true');parser.add_argument('--prepare-only',action='store_true')
    parser.add_argument('--stress-pages',type=int,default=420)
    args=parser.parse_args()
    if not 10<=args.stress_pages<=2000:parser.error('--stress-pages must be in [10, 2000]')
    manifest=prepare(args.tests,args.stress_pages)
    print(f"Staged {len(manifest['cases'])} clean cases.",flush=True)
    if not args.prepare_only:
        return subprocess.call(['bash','scripts/compile.sh'],cwd=ROOT)
    return 0
if __name__=='__main__':raise SystemExit(main())
