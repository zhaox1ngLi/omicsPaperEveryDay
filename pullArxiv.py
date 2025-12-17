import arxiv
from datetime import datetime, timedelta

def fetch_arxiv_papers(keywords, days_back=1):
    query = " OR ".join(keywords)

    search = arxiv.Search(
        query=query,
        max_results=300,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    cutoff = datetime.now() - timedelta(days=days_back)
    results = []

    for paper in search.results():
        if paper.published.replace(tzinfo=None) >= cutoff:
            results.append({
                "title": paper.title,
                "summary": paper.summary,
                "url": paper.entry_id,
                "source": "arXiv"
            })

    return results
