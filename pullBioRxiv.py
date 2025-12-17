import requests
from datetime import date, timedelta


def fetch_biorxiv_papers(days_back=1, max_results=2000, timeout=20):
    end = date.today()
    start = end - timedelta(days=int(days_back))
    start_s = start.isoformat()
    end_s = end.isoformat()

    papers = []
    cursor = 0

    while len(papers) < max_results:
        url = f"https://api.biorxiv.org/details/biorxiv/{start_s}/{end_s}/{cursor}"
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        data = resp.json() or {}

        collection = data.get("collection") or []
        if not collection:
            break

        for item in collection:
            title = (item.get("title") or "").strip()
            abstract = (item.get("abstract") or "").strip()
            doi = (item.get("doi") or "").strip()

            if not title:
                continue

            papers.append(
                {
                    "title": title,
                    "summary": abstract,
                    "url": doi,         
                    "source": "bioRxiv",
                }
            )

            if len(papers) >= max_results:
                break

        cursor += len(collection)

    return papers