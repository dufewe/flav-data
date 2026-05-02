# InspireHEP API 使用方法

## 基本信息

- **端点**: `https://inspirehep.net/api/literature`
- **格式**: JSON
- **请求头**: 必须包含 `Accept: application/json`
- **限制**: 每页默认 10 条，最多 1000 条

## 查询方式

### 按 arXiv ID 查询 (最常用)

```bash
curl -s -H 'Accept: application/json' \
  'https://inspirehep.net/api/literature?q=eprint:1512.04442'
```

### 按 InspireHEP 控制号直接查询

```bash
curl -s -H 'Accept: application/json' \
  'https://inspirehep.net/api/literature/1409497'
```

### 按合作组和年份搜索

```bash
curl -s -H 'Accept: application/json' \
  'https://inspirehep.net/api/literature?q=collaboration:LHCb%20and%20earliest_date:2025'
```

## 返回字段解析

### 顶层结构

```json
{
  "hits": {
    "hits": [{
      "id": "1409497",                     // control_number (字符串)
      "metadata": { ... }                  // 详细元数据
    }],
    "total": 1
  }
}
```

### metadata 核心字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `control_number` | int | InspireHEP 数据库主键 | `1409497` |
| `texkeys` | string[] | BibTeX 标识符 (Inspire ID) | `["LHCb:2015svh"]` |
| `preprint_date` | string | 预印本提交日期 | `"2021-11-09"` |
| `earliest_date` | string | 最早日期 | `"2021-11-09"` |
| `document_type` | string[] | 文档类型 | `["article"]` |
| `citation_count` | int | 被引用次数 | `9` |
| `author_count` | int | 作者数量 | `4` |

### 标题 (titles 数组)

```json
"titles": [
  {"source": "arXiv", "title": "Linking the $R_{K^{(*)}}$ anomalies..."},
  {"source": "IOP", "title": "Linking anomalies to Hubble tension..."}
]
```

- 优先用 arXiv 来源的标题 (保留完整 LaTeX)

### 作者 (authors 数组)

```json
"authors": [
  {
    "full_name": "Duan, Wen-Feng",
    "first_name": "Wen-Feng",
    "last_name": "Duan",
    "affiliations": [{"value": "CCNU, Wuhan, Inst. Part. Phys."}],
    "raw_affiliations": [{"value": "Institute of Particle Physics..."}]
  }
]
```

`first_author` 对象还包含邮箱信息。

### 发表信息 (publication_info)

```json
"publication_info": [{
  "journal_title": "Chin.Phys.C",
  "journal_volume": "47",
  "journal_issue": "3",
  "artid": "033102",
  "year": 2023
}]
```

### DOI

```json
"dois": [
  {"source": "IOP", "value": "10.1088/1674-1137/aca888"}
]
```

### arXiv 信息

```json
"arxiv_eprints": [{
  "value": "1512.04442",
  "categories": ["hep-ex"]
}]
```

### 摘要 (abstracts 数组)

```json
"abstracts": [
  {"source": "arXiv", "value": "The updated measurements..."},
  {"source": "IOP", "value": "Updated measurements from..."}
]
```

- 优先用 arXiv 来源的摘要 (保留 LaTeX 格式)

### 关键词

```json
"keywords": [
  {"source": "author", "value": "rare B-meson decays"},
  {"schema": "INSPIRE", "value": "new physics"}
]
```

## Python 提取示例

```python
import urllib.request
import json

def get_inspire_info(arxiv_id):
    url = f'https://inspirehep.net/api/literature?q=eprint:{arxiv_id}'
    req = urllib.request.Request(url, headers={'Accept': 'application/json'})
    response = urllib.request.urlopen(req, timeout=15)
    data = json.loads(response.read().decode('utf-8'))

    hit = data['hits']['hits'][0]
    meta = hit['metadata']
    recid = hit['id']  # control_number as string

    # texkey (Inspire ID)
    texkey = meta.get('texkeys', [''])[0]

    # 标题
    for t in meta.get('titles', []):
        if t.get('source') == 'arXiv':
            title = t['title']
            break
    else:
        title = meta.get('titles', [{}])[0].get('title', '')

    # 摘要
    for a in meta.get('abstracts', []):
        if a.get('source') == 'arXiv':
            abstract = a['value']
            break
    else:
        abstract = meta.get('abstracts', [{}])[0].get('value', '')

    # 作者
    authors = meta.get('authors', [])
    if len(authors) > 1:
        author_str = f"{authors[0]['full_name']} and others"
    elif authors:
        author_str = authors[0]['full_name']
    else:
        author_str = ''

    # 合作组
    collaborations = meta.get('collaborations', [])
    collaboration = collaborations[0]['value'] if collaborations else ''

    # 日期
    preprint_date = meta.get('preprint_date', '')
    time_str = preprint_date.replace('-', '.') if preprint_date else ''

    # 期刊信息
    pub_info = meta.get('publication_info', [{}])[0]
    journal = pub_info.get('journal_title', '')
    year = pub_info.get('year', '')
    volume = pub_info.get('journal_volume', '')
    artid = pub_info.get('artid', '')

    # DOI
    dois = meta.get('dois', [])
    doi = dois[0]['value'] if dois else ''

    return {
        'texkey': texkey,
        'recid': recid,
        'title': title,
        'abstract': abstract,
        'author': author_str,
        'collaboration': collaboration,
        'time': time_str,
        'journal': journal,
        'year': year,
        'volume': volume,
        'artid': artid,
        'doi': doi,
    }
```

## 构建 Markdown 链接

```python
# inspire-hep 字段
inspire_link = f"[{texkey}](https://inspirehep.net/literature/{recid})"
# 示例: "[LHCb:2015svh](https://inspirehep.net/literature/1409497)"

# arxiv 字段
arxiv_link = f"[{arxiv_id}](https://arxiv.org/pdf/{arxiv_id})"
# 示例: "[1512.04442](https://arxiv.org/pdf/1512.04442)"

## 两种 ID 的区别

| 名称 | 示例 | 类型 | 说明 |
|------|------|------|------|
| **control_number (recid)** | `1409497` | 整数 | 数据库自增主键，用于 URL |
| **texkey** | `LHCb:2015svh` | 字符串 | `合作组:年份+hash` 格式，用于 BibTeX 和显示 |

- URL 用 control_number: `https://inspirehep.net/literature/1409497`
- 显示文本用 texkey: `[LHCb:2015svh]`
