# 🐍 Python 招聘数据采集与分析爬虫 (Job Recruitment Spider)

> 一个基于新一代自动化工具 **DrissionPage** 开发的招聘网站数据采集工具。
> 实现了从数据抓取、清洗 (Pandas) 到可视化分析 (Pyecharts) 的全流程闭环。

![Python](https://img.shields.io/badge/Language-Python3-blue?style=flat-square&logo=python)
![DrissionPage](https://img.shields.io/badge/Tool-DrissionPage-green?style=flat-square)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458?style=flat-square&logo=pandas)
![Pyecharts](https://img.shields.io/badge/Viz-Pyecharts-red?style=flat-square)

## 📖 项目简介

本项目旨在自动化抓取主流招聘网站（如 Boss直聘）的 Python 岗位信息，帮助求职者快速分析市场行情。

与传统的 Selenium/Requests 爬虫不同，本项目采用了 **DrissionPage** 框架，能够有效绕过部分网站的自动化检测机制，实现了高效、稳定的数据采集。采集到的数据会自动进行清洗，并生成直观的 **HTML 交互式图表**。

## 📊 成果展示 (Visualization)

*(本项目已包含爬取到的示例数据 `data.csv` 及生成的 HTML 图表，下载即可查看)*

| 经验要求分布 (Pie/Line) | 学历要求分布 (Bar) |
| :---: | :---: |
|<img width="962" height="535" alt="image" src="https://github.com/user-attachments/assets/475f8c13-ad1e-473c-8a62-de2cd2e0bd24" />|<img width="959" height="533" alt="image" src="https://github.com/user-attachments/assets/f8556e29-e659-45d7-a375-cd8e86931a99" />|


## ✨ 核心功能

* **抗干扰采集**: 使用 `ChromiumPage` 监听数据包模式，通过 `listen.start` 直接捕获 JSON 数据接口，比传统 DOM 解析更稳定、更快速。
* **自动化翻页**: 模拟人工操作逻辑，自动处理分页请求。
* **数据持久化**: 使用 `csv` 模块将结构化数据（职位、薪资、公司、技能要求等）实时写入文件。
* **数据分析与可视化**:
    * 使用 **Pandas** 读取并处理 CSV 数据。
    * 使用 **Pyecharts** 生成饼图、柱状图和折线图，直观展示“城市分布”、“学历要求”及“经验要求”。

## 🛠️ 技术栈

* **核心框架**: Python 3.x
* **爬虫工具**: `DrissionPage` (监听数据包/自动化控制)
* **数据处理**: `Pandas`
* **可视化**: `Pyecharts` (生成 Echarts 风格的 HTML 报表)

## 📂 文件说明

```text
Python-Job-Spider/
├── 📄 pa.py           # 主程序：包含爬虫逻辑与可视化绘图代码
├── 📄 test.py         # 浏览器路径配置测试脚本
├── 📄 data.csv        # 采集到的原始数据样本
├── 📄 *.html          # 生成的可视化图表结果
└── 📄 README.md       # 项目说明文档
```

## 🚀 如何运行 (How to Run)
1. 安装依赖库:

```Bash
pip install DrissionPage pandas pyecharts
```
2. 配置浏览器路径: 请在 test.py 或 pa.py 中根据您的电脑环境，修改浏览器（Edge/Chrome）的可执行文件路径。

3. 运行爬虫:

```Bash
python pa.py
```
*程序将自动打开浏览器开始采集，结束后会在当前目录生成 data.csv 和 HTML 图表文件。*

👨‍💻 作者信息
吴俊 (Wu Jun)

- Email: 23jwu2@stu.edu.cn

- Portfolio: [访问我的简历主页](https://github.com/kinjo886/JIANLI_CV)

*声明：本项目仅用于编程学习与数据分析练习，请勿用于商业用途或对目标网站造成压力。*
