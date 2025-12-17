from datetime import datetime
import yaml

from pullArxiv import fetch_arxiv_papers
from pullBioRxiv import fetch_biorxiv_papers
from filterAndTag import filter_and_tag
from exportMarkdown import export_markdown, export_html
from sendEmail import send_html_email


def dedup_by_url(papers):
    seen = set()
    out = []
    for p in papers:
        url = p.get("url")
        if not url or url in seen:
            continue
        seen.add(url)
        out.append(p)
    return out


def load_config(path="config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main():
    cfg = load_config("config.yaml")
    days_back = int(cfg.get("days_back", 1))
    keyword_dict = cfg.get("keywords", {}) or {}

    omics_keywords = keyword_dict.get("omics", []) or []
    arxiv_raw = fetch_arxiv_papers(keywords=omics_keywords, days_back=days_back)
    biorxiv_raw = fetch_biorxiv_papers(days_back=days_back)

    arxiv = filter_and_tag(dedup_by_url(arxiv_raw), keyword_dict)[:10]
    biorxiv = filter_and_tag(dedup_by_url(biorxiv_raw), keyword_dict)[:10]

    papers = arxiv + biorxiv

    out_md = "daily_papers.md"
    out_html = "daily_papers.html"
    export_markdown(papers, out_md)
    export_html(papers, out_html)

    subject = f"论文日报 - {datetime.now().strftime('%Y-%m-%d')}"
    send_html_email(subject, html_path=out_html, text_path=out_md)


if __name__ == "__main__":
    main()