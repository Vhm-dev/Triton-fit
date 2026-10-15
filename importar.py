import argparse, json, re, unicodedata, zipfile, io, shutil
from pathlib import Path
from PIL import Image

def slug(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return re.sub(r'-+','-',re.sub(r'[^a-z0-9]+','-',s)).strip('-')

def run():
    p=argparse.ArgumentParser(description='Importador de GIFs para Triton Fit')
    p.add_argument('arquivo_zip',type=Path)
    p.add_argument('--publicar-gifs',action='store_true',help='Use somente quando possuir direitos/autorizacao para republicar')
    p.add_argument('--saida',type=Path,default=Path('triton-fit-atualizado.zip'))
    a=p.parse_args()
    base=Path(__file__).parent/'base'/'biblioteca-exercicios'
    js=(base/'exercises.js').read_text(encoding='utf-8')
    entries=[]; seen=set(); logs=[]
    with zipfile.ZipFile(a.arquivo_zip) as z:
        for info in z.infolist():
            if info.is_dir() or not info.filename.lower().endswith('.gif'):continue
            if info.file_size>30_000_000:logs.append(f'IGNORADO (mais de 30MB): {info.filename}');continue
            filename=Path(info.filename).name
            # ZIP may encode unicode filenames as #Uxxxx
            filename=re.sub(r'#U([0-9a-fA-F]{4,6})',lambda m:chr(int(m.group(1),16)),filename)
            sid=slug(Path(filename).stem)
            if not sid or sid in seen:logs.append(f'IGNORADO (nome repetido/invalido): {filename}');continue
            raw=z.read(info)
            try:
                im=Image.open(io.BytesIO(raw)); frames=getattr(im,'n_frames',1)
                if im.format!='GIF' or frames<2:raise ValueError('Nao e GIF animado')
            except Exception as e:logs.append(f'IGNORADO ({e}): {filename}');continue
            seen.add(sid)
            name=Path(filename).stem
            group='Glúteos' if any(w in sid for w in ['quadril','glute','ponte','abducao']) else 'Outros'
            if 'aducao' in sid:group='Adutores'
            equip='Cabo' if 'cabo' in sid else ('Máquina' if 'alavanca' in sid else 'Peso corporal')
            path=f'assets/gifs/{sid}.gif'
            obj=dict(id=sid,name=name,group=group,equipment=equip,summary='Demonstração do movimento. Orientações técnicas em revisão.',steps=['Ajuste o equipamento e adote uma posição estável.','Execute o movimento com controle e amplitude individualizada.'],caution='Orientações genéricas provisórias: revisar antes de disponibilizar aos alunos.',gif=path if a.publicar_gifs else '')
            entries.append((obj,raw,path,frames))
            logs.append(f'VALIDADO: {name} — {frames} quadros'+(' — incluido no pacote' if a.publicar_gifs else ' — midia nao publicada'))
    # Generate safe add-on JS instead of rewriting the existing library
    # Load after exercises.js in index.html
    addon='// Gerado pelo importador Triton Fit. Revise as orientacoes antes de publicar.\nwindow.EXERCISES.push(...'+json.dumps([x[0] for x in entries],ensure_ascii=False,indent=2)+');\n'
    html=(base/'index.html').read_text(encoding='utf-8').replace('<script src="exercises.js"></script>','<script src="exercises.js"></script><script src="importados.js"></script>')
    with zipfile.ZipFile(a.saida,'w',zipfile.ZIP_DEFLATED) as out:
        out.writestr('index.html',html)
        out.writestr('exercises.js',js)
        out.writestr('importados.js',addon)
        out.writestr('RELATORIO-IMPORTACAO.txt','\n'.join(logs)+'\n')
        if a.publicar_gifs:
            for obj,raw,path,frames in entries:out.writestr(path,raw)
    print('\n'.join(logs));print(f'\nArquivo gerado: {a.saida.resolve()}')
if __name__=='__main__':run()
