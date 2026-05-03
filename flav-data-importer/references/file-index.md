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
│   │   ├── ...
│   │   ├── 2011/
│   │   │   ├── LHCb@2011.json       # 年度索引文件
│   │   │   ├── 06/                  # 月份子文件夹
│   │   │   │   └── LHCb:2011xxx.json
│   │   │   └── 12/
│   │   │       └── LHCb:2011yyy.json
│   │   ├── 2012/
│   │   ├── ...
│   │   └── 2026/
│   ├── PDG/
│   └── {group}/                     # 其他实验组
├── Theoretical/                     # 理论数据 
│   └── {group}/                     # 理论组
└── ...  
```

## 命名规则

### 数据文件
- **格式**: `{Collaboration}:{InspireTexKey}.json`
- **示例**: `LHCb:2015svh.json`, `CMS:2023abc.json`, `Belle:2020def.json`
- **路径**: `Experimental/{group}/{year}/{month}/{file_id}.json` 或 `Theoretical/{group}/{year}/{month}/{file_id}.json`
- **月份**: 必须零填充，`01` 到 `12`

### 年度索引文件
- **格式**: `{group}@{year}.json`
- **位置**: `Experimental/{group}/{year}/{group}@{year}.json` 或 `Theoretical/{group}/{year}/{group}@{year}.json`
- **内容**: 月份到 file_id 的映射

```json
{
    "06": ["LHCb:2015svh"],
    "12": ["LHCb:2015abc", "LHCb:2015def"]
}
```

- **键**: 零填充月份字符串 ("01" 到 "12")
- **值**: file_id 数组（不含 `.json` 后缀），按 Inspire 时间排序
- **排序**: 按月份键升序排列，每个月内的 file_id 按 arXiv v1 提交日期排序

### 支持的合作组
`ATLAS`, `BaBar`, `Belle`, `BESIII`, `CDF`, `CMS`, `HFLAV`, `LEP`, `LHCb`, `PDG`
`HPQCD`, `RBC/UKQCD`, `JLQCD`, `FNAL/MILC` 等

### 合作组联合论文
当论文来自多个合作组时 (如 LHCb + BESIII):
- 使用主要合作组作为目录名
- texkey 包含所有合作组信息
- 示例: `LHCb:2026npj.json` (LHCb + BESIII 联合测量)

## 索引查询方法

### 查找某年某月有哪些文件
```python
import json
index = json.load(open('Experimental/LHCb/2015/LHCb@2015.json'))
files_in_december = index.get("12", [])  # ["LHCb:2015svh"]
```

### 查找某篇论文是否已入库
```python
import json, os
base = 'Experimental/LHCb'
target = 'LHCb:2025xxx'
for year in sorted(os.listdir(base)):
    if year.isdigit():
        index_path = os.path.join(base, year, f'LHCb@{year}.json')
        if os.path.exists(index_path):
            with open(index_path) as f:
                index = json.load(f)
            for month, files in index.items():
                if target in files:
                    print(f"Found: {year}/{month}/{target}.json")
```

### 检查索引完整性
```python
import json, os
base = 'Experimental/LHCb/2015'
index = json.load(open(f'{base}/LHCb@2015.json'))

# 获取所有实际文件
actual_files = set()
for month in index:
    for f in index[month]:
        actual_files.add(f)

# 扫描磁盘
disk_files = set()
for month_dir in sorted(os.listdir(base)):
    if month_dir.isdigit() and len(month_dir) == 2:
        for fname in os.listdir(f'{base}/{month_dir}'):
            if fname.endswith('.json') and '@' not in fname:
                disk_files.add(fname.replace('.json', ''))

# 找出差异
missing_in_index = disk_files - actual_files
missing_on_disk = actual_files - disk_files
```

## 文件 ID 来源

file_id 来自 InspireHEP 的 `texkeys` 字段:
- `LHCb:2015svh` → 文件名为 `LHCb:2015svh.json`
- `Aaij:2015oid` (第二作者 texkey) 也可使用，但优先用第一 texkey

## 注意事项

1. **索引同步**: 每次添加/删除 JSON 文件后必须更新年度索引
2. **月份归属**: 按 arXiv v1 提交日期的月份归档
3. **文件大小**: 单个 JSON 文件不宜过大 (建议 < 10MB)，关联矩阵数据量大时可考虑拆分
4. **备份**: 修改前备份原文件
5. **验证**: 写入后运行 `python3 scripts/json-valid.py` 确认格式正确
