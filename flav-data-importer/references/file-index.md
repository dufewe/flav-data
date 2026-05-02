# 文件索引与目录结构

## 数据库根目录

```
flav-data/
├── Experimental/                    # 实验数据
│   ├── ATLAS/
│   ├── BaBar/
│   ├── Belle/
│   ├── CDF/
│   ├── CMS/
│   ├── HFLAV/
│   ├── LEP/
│   ├── LHCb/
│   │   ├── LHCb.py                  # LHCb 数据自动加载脚本
│   │   ├── 2011/
│   │   │   ├── LHCb@2011.json       # 年度索引文件
│   │   │   ├── 06/                  # 月份子文件夹
│   │   │   │   └── LHCb:2011xxx.json
│   │   │   └── 12/
│   │   │       └── LHCb:2011yyy.json
│   │   ├── 2012/
│   │   ├── ...
│   │   └── 2025/
│   ├── PDG/
│   └── {group}/                     # 其他实验组
└── Theoretical/                     # 理论数据 (可扩展)
```

## 命名规则

### 数据文件
- **格式**: `{Collaboration}:{InspireTexKey}.json`
- **示例**: `LHCb:2015svh.json`, `CMS:2023abc.json`, `Belle:2020def.json`
- **路径**: `Experimental/{group}/{year}/{month}/{file_id}.json`

### 年度索引文件
- **格式**: `{group}@{year}.json`
- **位置**: `Experimental/{group}/{year}/{group}@{year}.json`
- **内容**: 月份到 file_id 的映射

```json
{
    "06": ["LHCb:2015svh"],
    "12": ["LHCb:2015svh"]
}
```

- **键**: 零填充月份字符串 ("01" 到 "12")
- **值**: file_id 数组（不含 `.json` 后缀）
- **排序**: 按月份键升序排列

### 支持的合作组
`ATLAS`, `BaBar`, `Belle`, `CDF`, `CMS`, `HFLAV`, `LEP`, `LHCb`, `PDG`

## 索引查询方法

### 查找某年某月有哪些文件
```python
import json
index = json.load(open('Experimental/LHCb/2025/LHCb@2025.json'))
files_in_april = index.get("04", [])  # ["LHCb:2015svh"]
```

### 查找某篇论文是否已入库
```python
import json, os
base = 'Experimental/LHCb'
for year in sorted(os.listdir(base)):
    if year.isdigit():
        index_path = os.path.join(base, year, f'LHCb@{year}.json')
        if os.path.exists(index_path):
            with open(index_path) as f:
                index = json.load(f)
            for month, files in index.items():
                if 'LHCb:2025xxx' in files:
                    print(f"Found: {year}/{month}/LHCb:2025xxx.json")
```

## 文件 ID 来源

file_id 来自 InspireHEP 的 `texkeys` 字段:
- `LHCb:2015svh` → 文件名为 `LHCb:2015svh.json`
- `Aaij:2015oid` (第二作者 texkey) 也可使用，但优先用第一 texkey
