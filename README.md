# Polymarket World Cup Data Fetcher

GitHub Actions 自动抓取 Polymarket 世界杯投注数据。

## 工作原理

1. GitHub Actions 在美国服务器定时运行（可访问 Polymarket）
2. 抓取世界杯相关市场的成交量、赔率、选项数据
3. 存为 JSON 写入仓库
4. 本地直接 `git pull` 即可读取——不用翻墙

## 部署

1. Push 到你的 GitHub 仓库
2. Actions 自动触发（每6小时一次）
3. `data/` 目录出现数据文件

## 本地读取

```python
import json
with open("data/polymarket_latest.json") as f:
    data = json.load(f)
for m in data["markets"]:
    print(m["question"], m["volume"])
```
