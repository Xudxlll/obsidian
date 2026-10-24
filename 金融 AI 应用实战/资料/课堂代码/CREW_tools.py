"""
金融投研 Mutil-Agent
数据获取, 估值计算
"""
from crewai.tools import tool
import re
import requests
from datetime import datetime

@tool
def get_stock_basic(symbol="sh600519"):
    """获取股票最新实时行情数据"""
    try:
        r = requests.get(f"http://qt.gtimg.cn/q={symbol}", timeout=10)
        parts = r.text.split("~")
        price = float(parts[3])
        pct = float(parts[32])
        high = float(parts[33])
        low = float(parts[34])
        vol = int(float(parts[6]))
        return f"""股票 {symbol}最新行情:
        - 最新价格: {price} 元
        - 当日涨跌幅: {pct} %
        - 当日最高价: {high} 元
        - 当日最低价: {low} 元
        - 成交量: {vol} 手
        """
    except Exception as e:
        print(f"获取股票行情失败{e}")

def clean(text):
    text = re.sub(r"<!--.*?-->", "", text, re.S)
    text = re.sub(r"<.*?>", "", text, re.S)
    return text.strip()

@tool
def get_stock_news(symbol):
    """
    查询股票相关的最新市场新闻
    输入股票代码,返回最多5条新闻,包含标题,时间,来源
    """
    keyword = f"{symbol.upper()} 美股"
    url = f"http://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&wd={keyword}"
    response = requests.get(
        url,
        headers={
            "Cookie": """PSTM=1782311186; BIDUPSID=D98BFC1565E2033D470E5F2860618121; BD_UPN=12314753;""",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }
    )
    response.encoding = "utf-8"

    html = response.text

    # 把html切分得到结果块
    blocks = re.split(r'(?=<h3 class="news-title_)', html)
    results = []
    for b in blocks[1:]:
        title_m = re.search(r'aria-label="标题：([^"]+)"', b)
        time_m = re.search(r'aria-label="发布于：([^"]+)"', b)
        source_m = re.search(r'aria-label="新闻来源：([^"]+)"', b)

        title = title_m.group(1).strip() if title_m else ""
        time = time_m.group(1).strip()
        source = source_m.group(1).strip()

        cut = re.split(r'<div class="(news-source_|result-op)', b)[0]
        b2 = re.sub(r'<h3 class="news-title_.*?</h3>', '', cut, flags=re.S)
        content = clean(b2)
        for drop in (time, source):
            if drop and drop in content:
                content = content.replace(drop, "", 1)
            content = content.strip()

        if title:
            results.append({
                "title": title,
                "time": time,
                "source": source,
                "content": content
            })

    # 组装信息
    lines = []
    for i, r in enumerate(results[:5], 1):
        lines.append(
            f"[{i}] {r['title']}\n"
            f"来源: {r['source']}\n"
            f"时间: {r['time']}\n"
            f"内容: {r['content']}\n"
        )

    return "\n".join(lines)

@tool
def calc(pe, industry_avg_re, profit_growth):
    """
    简单估值分析,计算PEG, 当前动态的PE 行业平均PE 利润增速
    """
    pe = float(pe)
    industry_avg_re = float(industry_avg_re)
    profit_growth = float(profit_growth)

    if profit_growth <= 0:
        return f"利润增速为: {profit_growth}, PEG不适用"

    peg = pe / (profit_growth * 100)
    pe_vs_industry = (pe - industry_avg_re) / industry_avg_re
    judgment = "可能低估" if peg < 1 else ("估值合理" if peg < 1.5 else "可能高估")

    return (
        f"PEG :{judgment}"
        f"PE 相对行业 {'溢价' if pe_vs_industry > 0 else '折价'} {abs(pe_vs_industry):.1}%"
    )

FINANCE_TOOLS = [get_stock_basic, get_stock_news, calc]
