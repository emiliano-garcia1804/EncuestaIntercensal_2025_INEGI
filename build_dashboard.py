"""Build one versioned browser bundle from the local dashboard sources."""
from pathlib import Path
import hashlib,re

def build():
    root=Path(__file__).resolve().parent
    files=['map.js','reference.js','data.js','explorer.js','app.js']
    content='\n'.join((root/name).read_text(encoding='utf-8') for name in files)
    bundle="(()=>{\n'use strict';\ntry {\n"+content+"\n} catch(error) { console.error(error); const notice=document.getElementById('load-status'); notice.hidden=false; notice.textContent='No se pudo cargar el tablero. Recarga la página; si continúa, comprueba que dashboard.bundle.js corresponde a esta versión.'; }\n})();\n"
    (root/'dashboard.bundle.js').write_text(bundle,encoding='utf-8')
    version=hashlib.sha256(bundle.encode()).hexdigest()[:12]
    html=(root/'index.html').read_text(encoding='utf-8-sig')
    html=re.sub(r'<script\b[^>]*src="(?:map|reference|data|explorer|app|dashboard\.bundle)\.js[^\"]*"[^>]*></script>','',html)
    html=html.replace('</head>',f'<script defer src="dashboard.bundle.js?v={version}" onerror="document.getElementById(\'load-status\').hidden=false"></script></head>')
    for name in ['styles.css','explorer.css']:
        digest=hashlib.sha256((root/name).read_bytes()).hexdigest()[:12]
        html=re.sub(r'href="'+re.escape(name)+r'(?:\?[^\"]*)?"',f'href="{name}?v={digest}"',html)
    (root/'index.html').write_text(html,encoding='utf-8')
    print('Built dashboard version '+version)

if __name__=='__main__': build()
