# arXiv API 使用方法

## 基本信息

- **端点**: `http://export.arxiv.org/api/query`
- **格式**: Atom XML
- **限制**: 每次最多 200 条结果

## 查询方式

### 按 arXiv ID 查询 (最常用)

```bash
curl -sL "http://export.arxiv.org/api/query?id_list=1512.04442"
```

### 搜索查询

```bash
# 按标题搜索
curl -sL "http://export.arxiv.org/api/query?search_query=ti:angular+analysis+cat:hep-ex&max_results=10"

# 按作者搜索
curl -sL "http://export.arxiv.org/api/query?search_query=au:Duan_Wen-Feng&max_results=20"
```

## 返回字段解析

```xml
<entry>
  <id>http://arxiv.org/abs/1512.04442v1</id>            <!-- 唯一标识 (含版本号) -->
  <updated>2016-01-26T14:32:53Z</updated>                <!-- 最后更新时间 -->
  <published>2015-12-14T16:00:00Z</published>            <!-- v1 首次提交时间 (关键!) -->
  <title>Angular analysis of the $B^{0}\to K^{*0}\mu^{+}\mu^{-}$ decay</title> <!-- 论文标题 -->
  <summary>An angular analysis of the $B^{0}\to K^{*0}(\to K^{+}\pi^{-})\mu^{+}\mu^{-}$ decay...</summary>  <!-- 摘要 -->

  <author>
    <name>Aaij, Roel</name>                              <!-- 作者 (可能多个) -->
  </author>

  <link href="http://arxiv.org/abs/1512.04442" />        <!-- abs 页面 -->
  <link href="http://arxiv.org/pdf/1512.04442" />        <!-- PDF 下载 -->

  <category term="hep-ph" />                            <!-- 主分类 -->
  <category term="hep-ex" />                            <!-- 交叉分类 -->

  <arxiv:comment>31 pages, 6 figures...</arxiv:comment> <!-- 备注 -->
  <arxiv:journal_ref>Chin.Phys.C 47 (2023) 3, 033102</arxiv:journal_ref> <!-- 期刊 (发表后) -->
  <arxiv:doi>10.1088/1674-1137/aca888</arxiv:doi>       <!-- DOI (发表后) -->
  <arxiv:primary_category term="hep-ph" />              <!-- 主分类 -->
</entry>
```

## Python 解析示例

```python
import urllib.request
import xml.etree.ElementTree as ET

def get_arxiv_info(arxiv_id):
    url = f'http://export.arxiv.org/api/query?id_list={arxiv_id}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req, timeout=15)
    xml_data = response.read().decode('utf-8')

    root = ET.fromstring(xml_data)
    ns = {'atom': 'http://www.w3.org/2005/Atom',
          'arxiv': 'http://arxiv.org/schemas/atom'}

    entry = root.find('atom:entry', ns)

    # v1 提交日期 → time 字段
    published = entry.find('atom:published', ns).text  # "2015-12-14T16:00:00Z"
    time_str = published[:10].replace('-', '.')         # "2015.12.14"

    # 标题
    title = entry.find('atom:title', ns).text.strip()

    # 摘要
    summary = entry.find('atom:summary', ns).text.strip()

    # 作者列表
    authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]
    if len(authors) > 1:
        author_str = f"{authors[0]} and others"
    else:
        author_str = authors[0]

    # PDF 链接
    pdf_link = entry.find('atom:link[@title="pdf"]', ns).get('href')

    # 分类
    categories = [c.get('term') for c in entry.findall('atom:category', ns)]

    # 期刊引用 (如果已发表)
    journal_ref = entry.find('arxiv:journal_ref', ns)
    journal_ref = journal_ref.text if journal_ref is not None else ''

    return {
        'arxiv_id': arxiv_id,
        'time': time_str,
        'title': title,
        'abstract': summary,
        'author': author_str,
        'authors': authors,
        'pdf_url': pdf_link,
        'categories': categories,
        'journal_ref': journal_ref,
    }
```

## 对 flav-data 的用途

| arXiv 字段 | flav-data 用途 |
|-----------|---------------|
| `published` | `time` 字段 (v1 提交日期) |
| `title` | `title` 字段 (可能需要 LaTeX 转义) |
| `summary` | `abstract` 字段 |
| `author[0]` | `author` 字段 (第一作者 + " and others") |
| `link[pdf]` | `pdf` 字段 |
| `category` | 辅助判断 (hep-ex 实验 vs hep-ph 理论) |

## 注意事项

1. **`published` 是 v1 时间**, `updated` 是最新版本时间 — 用 `published` 作为 `time`
2. **作者截断**: 超过 2 个作者时用 "FirstAuthor and others"
3. **标题可能需要 LaTeX 转义**: arXiv API 返回的标题用 `$...$` 格式
4. **网络限制**: 外部网络可能被阻断，需要本地终端访问
