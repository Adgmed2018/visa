"""Web UI mínima da Visa — visualizador de _visa_sdd/.

Filosofia: ZERO dependencias externas. Usa apenas http.server stdlib.
Single-file. Renderiza markdown como HTML simples (sem deps de markdown lib).

Introducido em v1.6.0 (P6).
"""
from __future__ import annotations

import html
import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


def _md_to_html(md_text: str) -> str:
    """Mini-renderer markdown -> HTML. Sem deps externas.

    Suporta: headers (# ## ###), bold (**), italic (*), code inline (`),
    code blocks (```), listas, links, paragrafos.
    """
    out: list[str] = []
    in_code = False
    in_list = False
    for line in md_text.splitlines():
        if line.startswith("```"):
            if in_code:
                out.append("</code></pre>")
                in_code = False
            else:
                lang = line[3:].strip()
                out.append(f'<pre><code class="lang-{html.escape(lang)}">')
                in_code = True
            continue
        if in_code:
            out.append(html.escape(line))
            continue
        if not line.strip():
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append("")
            continue
        # headers
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            if in_list:
                out.append("</ul>")
                in_list = False
            level = len(m.group(1))
            out.append(f"<h{level}>{html.escape(m.group(2))}</h{level}>")
            continue
        # listas
        m = re.match(r"^[\*\-]\s+(.*)$", line)
        if m:
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{_inline(m.group(1))}</li>")
            continue
        if in_list:
            out.append("</ul>")
            in_list = False
        out.append(f"<p>{_inline(line)}</p>")
    if in_list:
        out.append("</ul>")
    if in_code:
        out.append("</code></pre>")
    return "\n".join(out)


def _inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                  r'<a href="\2">\1</a>', text)
    return text


def _list_artifacts(project_root: Path) -> list[dict[str, Any]]:
    sdd = project_root / "_visa_sdd"
    if not sdd.exists():
        return []
    items = []
    for f in sorted(sdd.rglob("*")):
        if f.is_file() and f.suffix in (".md", ".yaml", ".yml", ".json", ".feature"):
            items.append({
                "rel": str(f.relative_to(project_root)),
                "size": f.stat().st_size,
            })
    return items


def _br_future_index(project_root: Path) -> list[str]:
    """Extrai todos os IDs BR-FUTURE-NNN dos artefatos."""
    sdd = project_root / "_visa_sdd"
    if not sdd.exists():
        return []
    ids: set[str] = set()
    for f in sdd.rglob("*.md"):
        try:
            text = f.read_text(encoding="utf-8")
        except OSError:
            continue
        for m in re.finditer(r"BR-FUTURE-[A-Z0-9-]+", text):
            ids.add(m.group(0))
    return sorted(ids)


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><title>Visa Web UI</title>
<style>
body{{font-family:-apple-system,Segoe UI,Roboto,sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;color:#222;line-height:1.6}}
h1,h2,h3{{color:#9126f5}}
nav{{background:#f6f3fb;padding:1rem;border-radius:8px;margin-bottom:2rem}}
nav a{{margin-right:1rem;color:#4300d4;text-decoration:none}}
nav a:hover{{text-decoration:underline}}
table{{border-collapse:collapse;width:100%}}
th,td{{padding:.5rem;border-bottom:1px solid #eee;text-align:left}}
pre{{background:#f0f0f0;padding:1rem;overflow-x:auto;border-radius:4px}}
code{{background:#f0f0f0;padding:.1rem .3rem;border-radius:3px;font-size:.9em}}
.badge{{display:inline-block;padding:.1rem .5rem;border-radius:3px;font-size:.8em;margin-right:.3rem}}
.br{{background:#9126f5;color:white}}
.amb{{background:#ff9800;color:white}}
.lac{{background:#f44336;color:white}}
footer{{margin-top:3rem;padding-top:1rem;border-top:1px solid #eee;color:#888;font-size:.9em}}
</style></head><body>
<nav>
<a href="/">Home</a>
<a href="/artifacts">Artefatos</a>
<a href="/br-future">BR-FUTURE</a>
<a href="/state">State</a>
</nav>
{body}
<footer>Visa Web UI · v{version} · gerado por <code>visa serve</code> (NOVO v1.6.0)</footer>
</body></html>
"""


def _render_home(project_root: Path, version: str) -> str:
    artifacts = _list_artifacts(project_root)
    br_ids = _br_future_index(project_root)
    state_path = project_root / ".visa" / "state.json"
    state_summary = "ausente"
    if state_path.exists():
        try:
            s = json.loads(state_path.read_text(encoding="utf-8"))
            state_summary = f"phase={s.get('phase')}, version={s.get('version')}"
        except (OSError, json.JSONDecodeError):
            state_summary = "corrompido"
    body = f"""
<h1>Visa Web UI</h1>
<p><strong>Projeto:</strong> <code>{html.escape(str(project_root))}</code></p>
<table>
<tr><th>Artefatos em <code>_visa_sdd/</code></th><td>{len(artifacts)}</td></tr>
<tr><th>IDs <span class="badge br">BR-FUTURE</span></th><td>{len(br_ids)}</td></tr>
<tr><th>State</th><td>{html.escape(state_summary)}</td></tr>
</table>
<p>Use os links acima para navegar.</p>
"""
    return PAGE_TEMPLATE.format(body=body, version=version)


def _render_artifacts(project_root: Path, version: str) -> str:
    items = _list_artifacts(project_root)
    if not items:
        body = "<h1>Sem artefatos</h1><p>Rode <code>/visa</code> no seu agente primeiro.</p>"
    else:
        rows = "".join(
            f'<tr><td><a href="/file?path={html.escape(i["rel"])}">{html.escape(i["rel"])}</a></td>'
            f'<td>{i["size"]} bytes</td></tr>'
            for i in items
        )
        body = f"<h1>Artefatos ({len(items)})</h1><table><tr><th>Path</th><th>Tamanho</th></tr>{rows}</table>"
    return PAGE_TEMPLATE.format(body=body, version=version)


def _render_file(project_root: Path, rel: str, version: str) -> str:
    f = (project_root / rel).resolve()
    # Sandboxing — proibido sair de project_root
    try:
        f.relative_to(project_root.resolve())
    except ValueError:
        return PAGE_TEMPLATE.format(body="<h1>403</h1><p>Acesso negado.</p>", version=version)
    if not f.exists() or not f.is_file():
        return PAGE_TEMPLATE.format(body="<h1>404</h1>", version=version)
    text = f.read_text(encoding="utf-8", errors="replace")
    if f.suffix == ".md":
        rendered = _md_to_html(text)
    else:
        rendered = f"<pre>{html.escape(text)}</pre>"
    body = f'<h1><code>{html.escape(rel)}</code></h1>{rendered}'
    return PAGE_TEMPLATE.format(body=body, version=version)


def _render_br_future(project_root: Path, version: str) -> str:
    ids = _br_future_index(project_root)
    rows = "".join(f'<tr><td><span class="badge br">{i}</span></td></tr>' for i in ids)
    body = f"<h1>BR-FUTURE-NNN ({len(ids)})</h1><table>{rows}</table>"
    return PAGE_TEMPLATE.format(body=body, version=version)


def _render_state(project_root: Path, version: str) -> str:
    p = project_root / ".visa" / "state.json"
    if not p.exists():
        return PAGE_TEMPLATE.format(body="<h1>State</h1><p>Ausente — rode <code>/visa</code></p>", version=version)
    try:
        s = json.loads(p.read_text(encoding="utf-8"))
        body = f"<h1>State</h1><pre>{html.escape(json.dumps(s, indent=2, ensure_ascii=False))}</pre>"
    except (OSError, json.JSONDecodeError) as e:
        body = f"<h1>State corrompido</h1><pre>{html.escape(str(e))}</pre>"
    return PAGE_TEMPLATE.format(body=body, version=version)


def make_handler(project_root: Path, version: str) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: Any) -> None:
            return  # silencioso

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            path = parsed.path
            if path == "/":
                page = _render_home(project_root, version)
            elif path == "/artifacts":
                page = _render_artifacts(project_root, version)
            elif path == "/br-future":
                page = _render_br_future(project_root, version)
            elif path == "/state":
                page = _render_state(project_root, version)
            elif path == "/file":
                qs = dict(p.split("=", 1) for p in parsed.query.split("&") if "=" in p)
                rel = unquote(qs.get("path", ""))
                page = _render_file(project_root, rel, version)
            else:
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"<h1>404</h1>")
                return
            data = page.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    return Handler


def serve(project_root: Path, port: int, version: str) -> None:
    handler = make_handler(project_root, version)
    server = HTTPServer(("127.0.0.1", port), handler)
    print(f"Visa Web UI em http://127.0.0.1:{port}/  (Ctrl+C para parar)")
    print(f"Projeto: {project_root}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nWeb UI encerrada.")
        server.server_close()
