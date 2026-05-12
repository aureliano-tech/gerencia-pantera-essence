import sys
import base64
import urllib.request
import urllib.parse
import json
from datetime import datetime

TOKEN = "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"
REPO = "aureliano-tech/gerencia-pantera-essence"
API = "https://api.github.com"

def get_file(path):
    url = f"{API}/repos/{REPO}/contents/{path}"
    req = urllib.request.Request(url, headers={"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"})
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
            return base64.b64decode(data["content"]).decode("utf-8"), data["sha"]
    except:
        return "", None

def update_file(path, content, sha, msg):
    url = f"{API}/repos/{REPO}/contents/{path}"
    body = {"message": msg, "content": base64.b64encode(content.encode("utf-8")).decode("utf-8")}
    if sha:
        body["sha"] = sha
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="PUT", headers={"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def append_to_file(path, new_entry, direccion):
    content, sha = get_file(path)
    updated = content + "\n" + new_entry
    msg = f"{direccion} · {datetime.now().strftime('%d/%m/%Y %H:%M')} · Cierre de sesion"
    update_file(path, updated, sha, msg)
    print(f"✅ {path} actualizado en GitHub")

if __name__ == "__main__":
    direccion = sys.argv[1]
    entrada = sys.argv[2]
    path_map = {
        "Gerencia": "SINCRONIZACION/CAMBIOS_GERENCIA.md",
        "P1": "SINCRONIZACION/CAMBIOS_P1.md",
        "P2": "SINCRONIZACION/CAMBIOS_P2.md",
        "P3": "SINCRONIZACION/CAMBIOS_P3.md",
        "P4": "SINCRONIZACION/CAMBIOS_P4.md"
    }
    path = path_map.get(direccion)
    if not path:
        print(f"❌ Dirección no reconocida: {direccion}")
        sys.exit(1)
    append_to_file(path, entrada, direccion)
