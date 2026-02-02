# 导入自动化模块
from DrissionPage import ChromiumPage
# 导入格式化输出模块
from pprint import pprint
# 导入csv模块s
import csv
# 导入时间模块 (新增，用于滚动等待)
import time
import random

# 导入数据处理模块
import pandas as pd
# 导入配置项
from pyecharts import options as opts
# 导入饼图
from pyecharts.charts import Pie, Bar, Line
# 导入数据
from pyecharts.faker import Faker

'''爬取网页信息'''

# 创建文件对象
f = open('data.csv', mode='w', encoding='utf-8', newline='')
# 字典写入方法
csv_writer = csv.DictWriter(f, fieldnames=[
    '职位',
    '城市',
    '区域',
    '街道',
    '公司',
    '薪资',
    '经验',
    '学历',
    '领域',
    '融资',
    '规模',
    '技能要求',
    '基本福利'
])
# 写入表头
csv_writer.writeheader()
# 实例化浏览器对象（自动打开浏览器）
dp = ChromiumPage()
# 监听数据包
dp.listen.start('wapi/zpgeek/search/joblist.json')
# 访问网站
dp.get('https://www.zhipin.com/web/geek/job?query=python&city=100010000')

print("开始采集数据...")

# 循环翻页
# 注意：如果是无限滚动，这里的 range(1, 20) 代表尝试滚动加载 19 次
for page in range(1, 20):
    print(f'正在采集第 {page} 页数据...')

    # 等待数据包加载 (第一次是打开网页自动加载，后续是滚动触发加载)
    # 如果长时间没有数据包，wait() 可能会报错，建议放在 try-except 块中更稳健，这里保持原逻辑简便性
    res = dp.listen.wait()

    # 获取响应数据
    json_data = res.response.body
    # pprint(json_data) # 调试用，平时可以注释掉

    # 解析数据
    job_list = json_data['zpData']['jobList']
    for job in job_list:
        dit = {
            '职位': job['jobName'],
            '城市': job['cityName'],
            '区域': job['areaDistrict'],
            '街道': job['businessDistrict'],
            '公司': job['brandName'],
            '薪资': job['salaryDesc'],
            '经验': job['jobExperience'],
            '学历': job['jobDegree'],
            '领域': job['brandIndustry'],
            '融资': job['brandStageName'],
            '规模': job['brandScaleName'],
            '技能要求': ','.join(job['skills']),
            '基本福利': ','.join(job['welfareList']),
        }
        # 写入数据
        csv_writer.writerow(dit)
        # print(dit)

    # === 核心修改部分：2026年无限滚动模式 ===
    print(f"第 {page} 页采集完毕，正在向下滚动加载新内容...")

    # 滚动到页面底部，触发新数据的加载
    dp.scroll.to_bottom()

    # 随机等待 1.5 到 3 秒，给网页加载新内容的时间，同时也模拟真人操作
    time.sleep(random.uniform(1.5, 3))
    # ====================================

# 关闭文件
f.close()
print("数据采集完成，开始生成图表...")

'''数据可视化'''

# 读出csv文件
try:
    df = pd.read_csv('data.csv')
    # print(df.head())

    # --- 饼图：城市分布 ---
    # 获取x轴数据内容
    x_city = df['城市'].value_counts().index.to_list()
    # 获取y轴数据内容
    y_city = df['城市'].value_counts().to_list()

    c = (
        Pie()
        .add(
            "",
            [
                list(z)
                for z in zip(
                x_city,  # x轴数据
                y_city,  # y轴数据
            )
            ],
            center=["40%", "50%"],
        )
        .set_global_opts(
            # 设置可视化标题
            title_opts=opts.TitleOpts(title="Python招聘城市分布情况"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        # 导出可视化效果：保存html文件
        .render("pie_Python招聘城市分布情况.html")
    )

    # --- 柱状图：学历要求 ---
    # 获取x轴数据内容
    x_edu = df['学历'].value_counts().index.to_list()
    # 获取y轴数据内容
    y_edu = df['学历'].value_counts().to_list()

    c_bar = (
        Bar()
        .add_xaxis(x_edu)
        .add_yaxis("学历", y_edu)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Bar-Python招聘学历要求分布情况"),
            toolbox_opts=opts.ToolboxOpts(),
            legend_opts=opts.LegendOpts(is_show=False),
        )
        .render("bar_Python招聘学历要求分布情况.html")
    )

    # --- 折线图：经验要求 ---
    # 获取x轴数据内容
    x_exp = df['经验'].value_counts().index.to_list()
    # 获取y轴数据内容
    y_exp = df['经验'].value_counts().to_list()

    c_line = (
        Line()
        .add_xaxis(x_exp)
        .add_yaxis("经验", y_exp)
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-Python招聘经验要求分布情况"))
        .render("line_Python招聘经验要求分布情况.html")
    )
    print("图表生成完毕！")

except Exception as e:
    print(f"可视化生成失败，可能是数据为空或格式错误: {e}")