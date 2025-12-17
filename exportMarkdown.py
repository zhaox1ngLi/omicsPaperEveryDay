import html
from datetime import datetime


def _today_tag() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _normalize_url(url: str) -> str:
    if not url:
        return ""
    u = str(url).strip()
    if u.startswith("10."):
        return "https://doi.org/" + u
    return u


def export_markdown(papers, filename="daily_papers.md"):
    title = f"Papers-{_today_tag()}"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        for p in papers:
            f.write(f"## {p.get('title', '')}\n")
            f.write(f"- Source: {p.get('source', '')}\n")
            f.write(f"- L: {', '.join(p.get('tags', []))}\n")
            f.write(f"- Link: {_normalize_url(p.get('url', ''))}\n")

            abstract = (p.get("abstract") or p.get("summary") or "").strip()
            if abstract:
                abstract = " ".join(abstract.split())
                f.write(f"\n**Abstract:** {abstract}\n")

            f.write("\n")


def export_html(papers, filename="daily_papers.html"):
    title = f"Papers-{_today_tag()}"

    parts = []
    parts.append("<!doctype html>")
    parts.append('<html lang="en">')
    parts.append("<head>")
    parts.append('<meta charset="utf-8" />')
    parts.append('<meta name="viewport" content="width=device-width, initial-scale=1" />')
    parts.append(f"<title>{html.escape(title)}</title>")
    parts.append(
        "<style>"
        "body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;max-width:980px;margin:24px auto;padding:0 16px;}"
        "h1{margin-bottom:16px;}"
        "article{padding:14px 0;border-top:1px solid #eee;}"
        "h2{font-size:18px;margin:0 0 8px 0;}"
        ".meta{color:#444;font-size:14px;margin:0 0 8px 0;}"
        ".meta b{color:#111;}"
        ".abstract{margin:8px 0 0 0;line-height:1.55;}"
        "a{color:#0b57d0;text-decoration:none;} a:hover{text-decoration:underline;}"
        "</style>"
    )
    parts.append("</head>")
    parts.append("<body>")
    parts.append(f"<h1>{html.escape(title)}</h1>")

    for p in papers:
        paper_title = html.escape(str(p.get("title", "")).strip())
        source = html.escape(str(p.get("source", "")).strip())
        tags = p.get("tags", []) or []
        tags_txt = html.escape(", ".join([str(t) for t in tags]))
        url = _normalize_url(p.get("url", ""))
        url_esc = html.escape(url)

        abstract = (p.get("abstract") or p.get("summary") or "").strip()
        abstract = " ".join(abstract.split())
        abstract_esc = html.escape(abstract)

        parts.append("<article>")
        parts.append(f"<h2>{paper_title}</h2>")
        parts.append(
            f'<p class="meta"><b>Source:</b> {source} &nbsp; '
            f'<b>Tags:</b> {tags_txt} &nbsp; '
            f'<b>Link:</b> <a href="{url_esc}" target="_blank" rel="noreferrer noopener">{url_esc}</a></p>'
        )
        if abstract_esc:
            parts.append(f'<p class="abstract"><b>Abstract:</b> {abstract_esc}</p>')
        parts.append("</article>")

    parts.append("</body>")
    parts.append("</html>")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))