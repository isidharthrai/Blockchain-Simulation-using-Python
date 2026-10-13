"""Web visualizer for Blockchain-Simulation-using-Python.
Put this file and index.html in the SAME folder as block.py, then run:  python server.py
It uses the project's real Block class (block.py) and jupiter_block.py. No extra packages needed.
"""
import json, os, webbrowser, datetime as date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from block import Block              # the project's real block + SHA-256 hashing
import jupiter_block as jb           # the project's genesis block

HERE = os.path.dirname(os.path.abspath(__file__))
chain = []


def reset():
    chain.clear()
    chain.append(jb.create_jupiter_block())


def add_block(data):
    last = chain[-1]
    chain.append(Block(last.index + 1, date.datetime.now(), data, last.hash))


def fix_chain():
    """Redo every block (what a cheater would have to do)."""
    for i, b in enumerate(chain):
        b.previous_hash = chain[i - 1].hash if i else "0"
        b.hash = b.hash_block()


def snapshot():
    out, broken = [], False
    for i, b in enumerate(chain):
        live = b.hash_block()                      # recomputed by block.py
        if live != b.hash:
            broken = True                          # block's contents changed
        if i and b.previous_hash != chain[i - 1].hash_block():
            broken = True                          # link to previous block no longer matches
        out.append({"index": b.index, "data": str(b.data), "hash": live,
                    "previous_hash": b.previous_hash, "broken": broken})
    return out


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, code, body, ctype="application/json"):
        raw = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path == "/api/chain":
            return self.send(200, json.dumps(snapshot()))
        if self.path in ("/", "/index.html"):
            with open(os.path.join(HERE, "index.html"), "rb") as f:
                return self.send(200, f.read(), "text/html")
        self.send(404, "{}")

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
        except ValueError:
            body = {}
        if self.path == "/api/add":
            add_block(str(body.get("data", "?"))[:30])
        elif self.path == "/api/tamper":
            i = int(body.get("index", -1))
            if 0 <= i < len(chain):
                chain[i].data = str(body.get("data", ""))[:30]   # hash is NOT updated
        elif self.path == "/api/fix":
            fix_chain()
        elif self.path == "/api/reset":
            reset()
        else:
            return self.send(404, "{}")
        self.send(200, json.dumps(snapshot()))


if __name__ == "__main__":
    reset()
    for port in range(8000, 8010):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
            break
        except OSError:
            continue
    url = "http://localhost:%d" % port
    print("Blockchain visualizer running at", url)
    print("Press Ctrl+C to stop.")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
