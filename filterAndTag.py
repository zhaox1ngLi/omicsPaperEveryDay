def filter_and_tag(papers, keyword_dict):
    omics_kws = keyword_dict.get("omics", []) or []
    methods_kws = keyword_dict.get("methods", []) or []
    tasks_kws = keyword_dict.get("tasks", []) or []

    filtered = []

    for p in papers:
        title = str(p.get("title", ""))
        summary = str(p.get("summary", ""))
        text = (title + " " + summary).lower()

        omics_hits = [kw for kw in omics_kws if str(kw).lower() in text]
        if not omics_hits:
            continue

        method_hits = [kw for kw in methods_kws if str(kw).lower() in text]
        task_hits = [kw for kw in tasks_kws if str(kw).lower() in text]

        tags = list(set([*omics_hits, *method_hits, *task_hits]))
        p["tags"] = tags

        p["_method_score"] = len(method_hits)
        p["_omics_hits"] = omics_hits
        p["_method_hits"] = method_hits

        filtered.append(p)

    filtered.sort(key=lambda x: (x.get("_method_score", 0), len(x.get("_omics_hits", []))), reverse=True)
    return filtered