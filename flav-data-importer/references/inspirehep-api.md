# InspireHEP API Reference

This document describes how to use the InspireHEP API to extract paper metadata — the authoritative source for TexKeys, collaboration names, and citation information.

## Endpoints

| Query Type | URL | Example |
|------------|-----|---------|
| By arXiv ID | `https://inspirehep.net/api/literature?q=eprint:{id}` | `...?q=eprint:1512.04442` |
| By control number (recid) | `https://inspirehep.net/api/literature/{recid}` | `.../literature/1409497` |
| By TexKey | `https://inspirehep.net/api/literature?q={texkey}` | `...?q=LHCb:2015svh` |
| By DOI | `https://inspirehep.net/api/literature?q={doi}` | `...?q=10.1007/JHEP02(2016)104` |
| By collaboration + year | `https://inspirehep.net/api/literature?q=collaboration:LHCb%20and%20earliest_date:2025` | Search results |

**Required header**: `Accept: application/json`

```bash
curl -s -H 'Accept: application/json' \
  'https://inspirehep.net/api/literature?q=eprint:1512.04442'
```

## Response Structure

### Search Response (by arXiv ID, TexKey, DOI)

```json
{
  "hits": {
    "hits": [{
      "id": 1409497,           // control_number
      "metadata": { ... }      // Full paper metadata
    }],
    "total": 1
  }
}
```

### Direct Response (by recid)

```json
{
  "id": 1409497,
  "metadata": { ... }          // Full paper metadata (no hits wrapper)
}
```

## Key Metadata Fields

| Field | Path | Type | Use |
|-------|------|------|-----|
| **control_number** | `id` (search) or `metadata.control_number` (direct) | int | `recid` for InspireHEP URLs |
| **texkeys** | `metadata.texkeys[]` | string[] | BibTeX citation keys. Use the first (collaboration-level) one for filenames. |
| **titles** | `metadata.titles[]` | object[] | Paper titles in various formats. Prefer entries with `source: "arXiv"` (preserves LaTeX). |
| **abstracts** | `metadata.abstracts[]` | object[] | Abstracts in various formats. Prefer `source: "arXiv"`. |
| **authors** | `metadata.authors[].full_name` | string[] | Full author list. Use first author + " and others" for the `author` field. |
| **first_author** | `metadata.first_author` | object | First author with email and affiliation info. |
| **collaborations** | `metadata.collaborations[].value` | string[] | Collaboration name(s). |
| **preprint_date** | `metadata.preprint_date` | string | arXiv v1 submission date (YYYY-MM-DD). |
| **arxiv_eprints** | `metadata.arxiv_eprints[].value` | string | arXiv ID (without version number). |
| **dois** | `metadata.dois[].value` | string[] | DOI(s). |
| **publication_info** | `metadata.publication_info[]` | object[] | Journal title, volume, issue, article ID, year. |
| **keywords** | `metadata.keywords[].value` | string[] | Author and INSPIRE keywords. |
| **citation_count** | `metadata.citation_count` | int | Total citation count. |
| **citation_count_without_self_citations** | `metadata.citation_count_without_self_citations` | int | Citations excluding self-citations. |

## Python Extraction

```python
import urllib.request
import json

def get_inspire_info(arxiv_id):
    """Fetch paper metadata from InspireHEP by arXiv ID.

    Returns a dict with fields mapped to flav-data JSON requirements.
    """
    url = f'https://inspirehep.net/api/literature?q=eprint:{arxiv_id}'
    req = urllib.request.Request(url, headers={'Accept': 'application/json'})
    data = json.loads(urllib.request.urlopen(req, timeout=15).read())

    hit = data['hits']['hits'][0]
    meta = hit['metadata']
    recid = hit['id']

    # TexKey (prefer collaboration-level, usually first)
    texkey = meta.get('texkeys', [''])[0]

    # Title — prefer arXiv source (preserves LaTeX)
    title = next(
        (t['title'] for t in meta.get('titles', [])
         if t.get('source') == 'arXiv'),
        meta.get('titles', [{}])[0].get('title', '')
    )

    # Abstract — prefer arXiv source (preserves LaTeX)
    abstract = next(
        (a['value'] for a in meta.get('abstracts', [])
         if a.get('source') == 'arXiv'),
        meta.get('abstracts', [{}])[0].get('value', '')
    )

    # Author
    authors = meta.get('authors', [])
    if len(authors) > 1:
        author_str = f"{authors[0]['full_name']} and others"
    elif authors:
        author_str = authors[0]['full_name']
    else:
        # Fallback: use collaboration name
        collabs = meta.get('collaborations', [])
        author_str = f"{collabs[0]['value']} collaboration" if collabs else ''

    # Collaboration
    collabs = meta.get('collaborations', [])
    collaboration = collabs[0]['value'] if collabs else ''

    # Date
    preprint_date = meta.get('preprint_date', '')
    time_str = preprint_date.replace('-', '.') if preprint_date else ''

    return {
        'texkey': texkey,
        'recid': str(recid),
        'title': title,
        'abstract': abstract,
        'author_str': author_str,
        'collaboration': collaboration,
        'time': time_str,
        'inspire_hep_link': f'[{texkey}](https://inspirehep.net/literature/{recid})',
    }
```

## Direct Query by recid

```python
def get_inspire_by_recid(recid):
    """Fetch paper metadata directly by InspireHEP control number."""
    url = f'https://inspirehep.net/api/literature/{recid}'
    req = urllib.request.Request(url, headers={'Accept': 'application/json'})
    return json.loads(urllib.request.urlopen(req, timeout=15).read())
```

## Two ID Types

| Name | Example | Type | Purpose |
|------|---------|------|---------|
| **control_number (recid)** | `1409497` | Integer | Database primary key. Used in InspireHEP URLs. |
| **TexKey** | `LHCb:2015svh` | String | BibTeX citation key. Format: `collaboration:year+hash`. Used for display and filenames. |

The URL uses recid: `https://inspirehep.net/literature/1409497`
The display text uses TexKey: `[LHCb:2015svh](https://inspirehep.net/literature/1409497)`

## Notes

1. **Always prefer arXiv-sourced titles and abstracts** — they preserve LaTeX formatting. Journal-sourced versions often strip LaTeX.
2. **Author fallback**: If the `authors` array is empty or missing, construct the author field as `"{group} collaboration"`.
3. **Multiple TexKeys**: A paper may have both a collaboration-level TexKey (e.g., `LHCb:2015svh`) and an author-level one (e.g., `Aaij:2015oid`). Always use the collaboration-level one for filenames and indices.
4. **Annual indices**: Always verify the latest TexKey on InspireHEP before writing or updating annual indices. TexKeys can change when papers are updated.
5. **API reliability**: The InspireHEP API can intermittently return empty responses or timeout, especially for very large records (e.g., PDG reviews). If you get a `JSONDecodeError` or empty hits array, retry after a 2-second delay, or use the bibtex endpoint as fallback: `https://inspirehep.net/api/literature/{recid}?format=bibtex`.
6. **`arxiv_eprints.value` does not include the version number** — use the arXiv API to get the version.
