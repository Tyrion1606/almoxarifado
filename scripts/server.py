"""Servidor local opcional para registrar compras, uso e descartes pela página.

Uso: python3 scripts/server.py            (abre http://127.0.0.1:8765 no navegador)
     python3 scripts/server.py --port 9000 --no-browser

Aberto por file://, o catálogo continua funcionando só para consulta. Por este
servidor, a aba Histórico ganha um formulário: cada registro é gravado no SQLite
e os snapshots (catalog.js e inventory.sql) são regenerados na hora. Escuta
apenas em 127.0.0.1 e usa só a biblioteca padrão do Python.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import threading
import webbrowser
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import db  # noqa: E402

MAX_BODY = 16 * 1024
DELETE_ROUTE = re.compile(r'/api/movements/(\d+)/delete')


class Handler(SimpleHTTPRequestHandler):
    database: Path = db.DATABASE
    data_dir: Path = db.DATA
    write_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(db.ROOT), **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, format, *args):  # noqa: A002 - assinatura herdada
        if self.path.startswith('/api/'):
            super().log_message(format, *args)

    def do_GET(self):
        if self.path == '/api/status':
            return self.send_json({'writable': True})
        if self.path.startswith('/api/'):
            return self.send_json({'error': 'Rota desconhecida.'}, HTTPStatus.NOT_FOUND)
        if any(part.startswith('.') for part in self.path.split('?')[0].split('/')):
            return self.send_error(HTTPStatus.NOT_FOUND)  # .git e outros arquivos ocultos
        return super().do_GET()

    def do_POST(self):
        problem = self.untrusted_request()
        if problem:
            return self.send_json({'error': problem}, HTTPStatus.FORBIDDEN)
        try:
            body = self.read_json()
            match = DELETE_ROUTE.fullmatch(self.path)
            with self.write_lock:
                con = db.connect(self.database)
                try:
                    if self.path == '/api/movements':
                        db.add_movement(con, body.get('component_id'), body.get('type_id'), body.get('quantity'),
                                        body.get('date'), body.get('note', ''))
                    elif match:
                        db.delete_movement(con, int(match.group(1)))
                    else:
                        return self.send_json({'error': 'Rota desconhecida.'}, HTTPStatus.NOT_FOUND)
                    db.write_snapshots(con, self.data_dir)
                    catalog = db.build_catalog(con)
                finally:
                    con.close()
        except db.InventoryError as error:
            return self.send_json({'error': str(error)}, HTTPStatus.UNPROCESSABLE_ENTITY)
        return self.send_json({'catalog': catalog})

    def untrusted_request(self) -> str | None:
        """Bloqueia outros sites (CSRF/DNS rebinding): só aceita JSON vindo desta mesma origem local."""
        port = self.server.server_address[1]
        hosts = {f'127.0.0.1:{port}', f'localhost:{port}'}
        if self.headers.get('Host') not in hosts:
            return 'Host não permitido.'
        origin = self.headers.get('Origin')
        if origin and origin not in {f'http://{host}' for host in hosts}:
            return 'Origem não permitida.'
        if not self.headers.get('Content-Type', '').startswith('application/json'):
            return 'Envie JSON.'
        return None

    def read_json(self) -> dict:
        length = int(self.headers.get('Content-Length') or 0)
        if length > MAX_BODY:
            raise db.InventoryError('Requisição grande demais.')
        try:
            body = json.loads(self.rfile.read(length) or b'{}')
        except ValueError:
            raise db.InventoryError('JSON inválido.') from None
        if not isinstance(body, dict):
            raise db.InventoryError('JSON inválido.')
        return body

    def send_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        blob = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(blob)))
        self.end_headers()
        self.wfile.write(blob)


def main() -> None:
    parser = argparse.ArgumentParser(description='Abre o almoxarifado com registro de movimentações.')
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--no-browser', action='store_true', help='não abrir o navegador automaticamente')
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    url = f'http://127.0.0.1:{args.port}/'
    print(f'Almoxarifado em {url} — registros vão para data/inventory.sqlite. Ctrl+C encerra.')
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServidor encerrado. Lembre de comitar data/ para guardar os registros no Git.')
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
