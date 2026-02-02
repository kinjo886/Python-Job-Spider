# 导入自动化模块
from DrissionPage import ChromiumPage
# 导入格式化输出模块
from pprint import pprint
# 导入csv模块s
import csv

# 导入数据处理模块
import pandas as pd
# 导入配置项
from pyecharts import options as opts
# 导入饼图
from pyecharts.charts import Pie,Bar,Line
# 导入数据
from pyecharts.faker import Faker

'''爬取网页信息'''

# 创建文件对象
f = open('data.csv',mode='w',encoding='utf-8',newline='')
# 字典写入方法
csv_writer = csv.DictWriter(f,fieldnames=[
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
# 循环翻页
for page in range(1,11):
    print(f'正在采集第{page}页的数据内容')
    # 下滑网页页面到底部
    dp.scroll.to_bottom()
    # 等待数据包加载
    resp = dp.listen.wait()
    # 获取响应数据
    json_data = resp.response.body
    """解析数据"""
    # 提取职位信息所在列表
    jobList =json_data['zpData']['jobList']
    # for循环遍历，提取列表里面的元素（30个岗位信息）
    for index in jobList:
        # 提取相关数据，保存字典
        dit ={
            '职位': index['jobName'],
            '城市': index['cityName'],
            '区域': index['areaDistrict'],
            '街道': index['businessDistrict'],
            '公司': index['brandName'],
            '薪资': index['salaryDesc'],
            '经验': index['jobExperience'],
            '学历': index['jobDegree'],
            '领域': index['brandIndustry'],
            '融资': index['brandStageName'],
            '规模': index['brandStageName'],
            '技能要求': ''.join(index['skills']),
            '基本福利': ''.join(index['welfareList']),
        }
        # join 列表合并字符串
        # 写入数据
        csv_writer.writerow(dit)
        print(dit)

    # 点击下一页（元素定位） -dp.ele()通过元素定位 -click()点击操作
    dp.ele('css:.ui-icon-arrow-right').click()

'''数据可视化'''

# 读出csv文件
df = pd.read_csv('data.csv')
# print(df.head())
#获取x轴数据内容
x_city =df['城市'].value_counts().index.to_list()
#获取y轴数据内容
y_city =df['城市'].value_counts().to_list()
# 饼图
c =(
    Pie()
    .add(
        "",
        [
            list(z)
            for z in zip(
                x_city,#x轴数据
                y_city,#y轴数据
            )
        ],
        center=["40%", "50%"],
    )
    .set_global_opts(
        #设置可视化标题
        title_opts=opts.TitleOpts(title="Python招聘城市分布情况"),
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    #导出可视化效果：保存html文件
    .render("pie_Python招聘城市分布情况.html")
)

#获取x轴数据内容
x_edu =df['学历'].value_counts().index.to_list()
#获取y轴数据内容
y_edu =df['学历'].value_counts().to_list()
# 柱状图
c_bar = (
    Bar()
    .add_xaxis(x_edu)
    .add_yaxis("学历", y_edu, stack="stack1")
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="Bar-Python招聘学历要求分布情况"))
    .render("bar_Python招聘学历要求分布情况.html")
)

#获取x轴数据内容
x_exp =df['经验'].value_counts().index.to_list()
#获取y轴数据内容
y_exp =df['经验'].value_counts().to_list()
# 折线图
c_Line = (
    Line()
    .add_xaxis(x_exp)
    .add_yaxis("经验", y_exp, is_connect_nones=True)
    .set_global_opts(title_opts=opts.TitleOpts(title="Line-Python招聘经验要求分布情况"))
    .render("line_Python招聘经验要求分布情况.html")
)
