"""
目标：用于下载 php.cn 的文件
开始时间：2020年4月27日 15:51:09
完成时间：2020年4月27日 22:08:47
入口：https://www.php.cn/xiazai/

该网站由于路由守卫设置问题，可以无登录遍历文件，
只需替换超链关键字即可实现下载。
链接对应关系：

{
'js' : 'down',
'code' : 'updown',
'gongju' : 'download',
'shouce' : 'downs',
'leiku' : 'downloads',
'sucai' : 'wpdown',
}

"""

from requests import get
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from urllib.parse import unquote
from os import mkdir


def confirm_path():
    """
    说明.txt认文件保存路径是否存在
    """
    try:
        with open("./file_down/success.txt", "w")as file:
            file.write("程序正常开始")
        return ""
    except:
        mkdir("./file_down")
        confirm_path()

"""
显示菜单用于选择
"""
def menu():
    show = {
        'title' : '欢迎使用 php中文网 文件下载器',
        'time' : '程序更新于：2020年4月27日',
        'notice' : '仅供学习，请勿用于非法用途',
        'dash1' : '-'*30,
        'info' : '已支持下列类型：',
        'dash2' : '-'*30,
        'js' : '0、js',
        'code' : '1、代码',
        'gongju' : '2、工具',
        'shouce' : '3、手册',
        'leiku' : '4、类库',
        'sucai' : '5、素材'
    }

    for item in show.values():
        print("\t\t", item)
    try:
        select = int(input("\n\t\t请输入你要下载的类型序号："))
        select = select % 6
    except:
        print("\t\t你是输入了个锤子吗？？")
        return None
    return select


def fileShow(select):
    """
    显示可以下载的文件信息，比如页数
    """
    # 确定基准超链接
    rootUrl = "https://www.php.cn/xiazai/"
    pageShow = ['js','code','gongju','shouce','leiku','sucai']
    keyword = pageShow[select]
    pageUrl = rootUrl + keyword
    print("\n你选择了：%s，超链接是：%s\n"%(keyword, pageUrl))

    response = get(pageUrl)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 有的只有一页，所以分类讨论
    if select in [0, 1, 4, 5]:
        ul_tags = soup.find('ul', class_ = 'page')
        max_page = ul_tags.find_all('a')[-2].string
        print("总共：%s 页。"%max_page)
        file_down_page(keyword)
    else:
        dd_tags = soup.find_all('dd', class_ = 'phpcn-col-md3')
        print("总共发现：%s 个工具/手册。"%len(dd_tags))
        file_down_item(keyword)



def file_down_page(keyword):
    """
    按页下载文件
    """
    # 确定基准超链和对应的替换词
    pageUrl = "https://www.php.cn/xiazai/" + keyword
    key_down = {
        'js' : 'down',
        'code' : 'updown',
        'leiku' : 'downloads',
        'sucai' : 'wpdown'
    }

    try:
        page_start = int(input("请输入你想下载的开始页："))
        page_end = int(input("请输入你想下载的结束页："))
    except:
        print("好像发现了什么奇怪的东西~")
        return None

    page_num = page_end - page_start
    if (page_num >= 0):
        while(page_end - page_start >= 0):
            pageUrl = "https://www.php.cn/xiazai/" + keyword + "?p=%d"%page_start
            print("\n%s\n正在访问：%s\n%s\n"%('-'*30, pageUrl, '-'*30))
            page_start += 1

            try:
                response = get(pageUrl)
                soup = BeautifulSoup(response.text, 'html.parser')
                if keyword == 'leiku':
                    class_name = 'phpcn-clear'
                else:
                    class_name = 'phpcn-col-md3'
                tags = soup.find_all('dd', class_ = class_name)
                for tag in tags:
                    id = tag.div.a['href'].split("/")[-1]
                    if keyword == 'leiku':
                        name = tag.div.a.string
                    else:
                        name = tag.div.h2.a.string
                    down_url = "https://www.php.cn/xiazai/%s/%s"%(key_down[keyword], id)
                    try:
                        urlretrieve(down_url, "./file_down/%s.zip"%name)
                        print("正在下载：", name)
                    except KeyboardInterrupt:
                        print("已终止。")
                        return
                    except:
                        print("此项下载失败。")
            except:
                print("当前页访问失败。")
    else:
        print("好像出现了什么奇怪的问题~")



def file_down_item(keyword):
    """
    文件较少，按个下载
    """
    key_down = {
        'gongju' : 'download',
        'shouce' : 'downs'
    }
    pageUrl = "https://www.php.cn/xiazai/" + keyword

    response = get(pageUrl)
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.find_all('dd', class_ = 'phpcn-col-md3')

    # 建立字典存放序号和对应的ID，为选择做准备
    file_dict = {}
    file_count = 0
    for tag in tags:
        file_count += 1
        id = tag.a['href'].split("/")[-1]
        name = tag.div.h2.string
        file_dict[file_count] = id
        print(file_count, name)
    print('-'*30)

    def down(down_url):
        # 使用请求响应的 URL 来解析文件名，主要是解析后缀名
        response = get(down_url)
        file_name = response.url.split("?")[0].split("/")[-1]
        # 解码 URL 编码，使其变成中文
        file_name = unquote(file_name)
        
        try:
            with open("./file_down/%s"%file_name, 'wb')as file:
                file.write(response.content)
                print("下载完成：%s"%file_name)
        except:
            print("下载失败：%s"%file_name)
        
    while(True):
        num = int(input("请输入你要下载的文件（0退出999全部）:"))
        if num == 0:
            break
        if num == 999:
            for id in file_dict.values():
                down_url = "https://www.php.cn/xiazai/%s/%s"%(key_down[keyword], id)
                down(down_url)
            break
        else:
            down_url = "https://www.php.cn/xiazai/%s/%s"%(key_down[keyword], file_dict[num])
            down(down_url)
            

def main():
    confirm_path()
    print("\n\n")
    select = menu()
    if select in [0, 1, 2, 3, 4, 5]:
        try:
            fileShow(select)
        except KeyboardInterrupt:
            print("已终止")
            return None
        except:
            print("已停止")
            return None
    print("\n\n%s\n如果下载的文件只有1KB大小，那么有极大可能是这个文件not found!删除即可。"%('-'*60))
    print("具体内容可访问：https://www.php.cn/xiazai/")
    end = input("按回车键关闭窗口")

if __name__ == '__main__':
    main()
