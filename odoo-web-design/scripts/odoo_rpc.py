"""Conexión JSON-RPC a Odoo para el skill odoo-web-design.

Credenciales por variables de entorno (nunca en archivos que se entreguen):
  ODOO_URL   https://cliente.odoo.com
  ODOO_DB    nombre de la base
  ODOO_USER  usuario (correo)
  ODOO_KEY   API key        (o ODOO_KEY_FILE con la ruta a un archivo chmod 600)

Uso:
  from odoo_rpc import x, rpc, UID, langs, backup
  x('website', 'read', [1], fields=['name'])
"""
import json, os, time, urllib.request, urllib.error

URL = os.environ['ODOO_URL'].rstrip('/')
DB = os.environ['ODOO_DB']
USER = os.environ['ODOO_USER']
KEY = os.environ.get('ODOO_KEY') or open(os.environ['ODOO_KEY_FILE']).read().strip()


def rpc(service, method, *args, retries=3):
    body = json.dumps({"jsonrpc": "2.0", "method": "call",
                       "params": {"service": service, "method": method, "args": args}, "id": 1}).encode()
    for attempt in range(retries):
        try:
            req = urllib.request.Request(URL + '/jsonrpc', body, {'Content-Type': 'application/json'})
            r = json.load(urllib.request.urlopen(req, timeout=120))
            break
        except urllib.error.HTTPError as e:  # 502/503 temporales de Odoo Online
            if e.code in (502, 503, 504) and attempt < retries - 1:
                time.sleep(4 * (attempt + 1)); continue
            raise
    if 'error' in r:
        raise Exception(r['error']['data']['message'])
    return r['result']


UID = rpc('common', 'authenticate', DB, USER, KEY, {})
if not UID:
    raise SystemExit('No se pudo autenticar: revisa ODOO_URL, ODOO_DB, ODOO_USER y la API key.')


def x(model, method, *args, **kw):
    return rpc('object', 'execute_kw', DB, UID, KEY, model, method, list(args), kw)


def langs(website_id=1):
    """Idiomas activos del sitio (códigos). Los campos traducibles se escriben en todos."""
    w = x('website', 'read', [website_id], fields=['language_ids'])[0]
    codes = [l['code'] for l in x('res.lang', 'read', w['language_ids'], fields=['code'])]
    return sorted(set(codes) | {'en_US'})


def backup(name, data, folder='respaldo'):
    """Guarda un respaldo JSON con fecha y hora en respaldo/."""
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, time.strftime('%Y%m%d-%H%M%S') + '_' + name + '.json')
    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=1, default=str)
    return path
