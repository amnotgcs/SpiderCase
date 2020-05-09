from requests import get
from re import search
from re import compile
from os import getcwd
from bs4 import BeautifulSoup


def get_page(pageurl):
    """
    获取页面
    """
    #try:
    response = get(pageurl, headers = header)
    page_soup = BeautifulSoup(response.text, 'html.parser')
    file_tags = page_soup.find_all('a', class_ = "item-title")

    # 每页有10个文件，解析HTML以获取文件ID
    # 然后拼接URL之后获取文件类型并下载文件
    for tag in file_tags:
        fileName = (tag.string).strip()
        #fileID = tag['href'][-4:]
        pat = compile(r"\d+")
        fileID = search(pat, tag['href']).group()
        furl = fileurl + fileID

        ftype = get_file_type(furl)
        if ftype:
            file_down(fileName, fileID, ftype)
        else:
            print("文件类型获取失败，%s 文件将不被下载。"%fileName)


def get_page_num(item):
    """
    用于解析该类别的最大页数
    """
    url = fileurl + kindsDict[item]
    response = get(url, headers = header)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 获取网页导航中>>标签对应的页数作为最大页数返回
    tag = soup.find(string ='»')
    maxNum = search(r'\d+$', tag.parent['href']).group()
    return maxNum


def get_file_type(url):
    """
    用于获取文件的类型，也就是后缀名
    """
    try:
        file_response = get(url, headers = header)
        file_soup = BeautifulSoup(file_response.text, 'html.parser')
        ftype = file_soup.find(string = "资源类型：").next_element.string
    except:
        return None
    return ftype


def file_down(fileName, fileID, ftype):
    """
    用于将文件保存到本地
    """
    global count
    down_url = downurl + fileID
    print("%d:正在下载：%s,id=%s"%(count, fileName, fileID))
    try:
        fileContent = get(down_url, headers = header)
        with open("%s.%s"%(fileName, ftype), "wb") as file:
            file.write(fileContent.content)
    except:
        print("保存 %s 文件的时候，出现了异常，文件可能已损坏。"%fileName)
    count += 1


def menu():
    """
    显示类别，提供目录导航
    """
    global kindsDict
    kinds = ['嵌入式系统', '模拟/电源', '射频/微波', '基础器件', 'EDA/PCB', '可编程逻辑', '网络/通信', '汽车电子', '消费电子', '传感技术', '测试测量', '控制器/处理器', '工业电子', '医疗电子']
    kindsDict = {
        '嵌入式系统' : 'embedded',
        '模拟/电源' : 'analog',
        '射频/微波' : 'rf',
        '基础器件' : 'component',
        'EDA/PCB' : 'eda',
        '可编程逻辑' : 'fpga',
        '网络/通信' : 'communication',
        '汽车电子' : 'automobile',
        '消费电子' : 'consumer-electronics',
        '传感技术' : 'sensor',
        '测试测量' : 'test',
        '控制器/处理器' : 'controller',
        '工业电子' : 'industrial-electronics',
        '医疗电子' : 'medical-electronics'
    }
    print("\n程序更新于：2020-04-03-v1.0")
    print("\n--此程序下载与非网(资料下载页面)文件--")
    print("程序仅供研究学习使用，请勿用于非法用途！")
    print("---请于下载24小时之内删除本程序！---\n")
    print("正在解析页数，请稍后：")
    print("-"*30)
    print("序号\t类别\t\t页数")
    print("-"*30)
    for i in range(len(kinds)):
        print("%d\t%s\t\t页数：%s"%(i,kinds[i],get_page_num(kinds[i])))
        #print("序号", i, kinds[i],"\t页数：",  get_page_num(kinds[i]))
    print("-"*30)
    choice = int(input("请选择你要下载的类别(序号)："))
    choice = kinds[choice%14]
    print("-"*30)
    print("你选择了：%s"%choice)

    pageurl = fileurl + kindsDict[choice] + "?p="
    startPage = int(input("请输入开始页数："))
    endPage = int(input("请输入结束页数："))
    print("-"*30)
    if (endPage-startPage) >= 0:
        for i in range(startPage,endPage+1):
            url = pageurl + str(i)
            print("开始获取第%d页"%(i))
            get_page(url)
    else:
        print("\n你怕是输错了页数~\n")
    print("-"*30)
    print("下载已完成，文件保存在：%s"%getcwd())
    input("按下回车键退出")

def main():
    """
    主函数调用菜单函数以开始
    """
    global fileurl
    global downurl
    global header
    global count
    fileurl = "https://www.eefocus.com/document/"
    downurl = "https://www.eefocus.com//docextendres/download/index/id-"
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'}
    count = 1

    menu()

if __name__ == "__main__":
    main()
            
