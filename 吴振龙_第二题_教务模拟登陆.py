import os
import json
import requests
from PIL import Image
from lxml import etree


def landing(s, url, student_id, password, code):  #登陆教务处网站，返回登陆后的response对象

    response = s.get(url)
    __VIEWSTATE = etree.HTML(
        response.content).xpath('//*[@id = "form1"]/input/@value')[0]

    data = {
        "__VIEWSTATE": __VIEWSTATE,
        "txtUserName": student_id,
        "TextBox2": password,
        "txtSecretCode": code,  #验证码
        "Button1": "",
    }

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36",
    }

    response_landed = s.post(url, data=data, headers=headers)
    print("login sucess!")
    return response_landed


def vcode(s, vcode_url):
    #获取验证码图片，打开，然后手动输入验证码，返回验证码
    response_vcode = s.get(vcode_url, stream=True)
    image = response_vcode.content
    imgpath = os.getcwd() + '\\' + 'vcode.jpg'

    with open(imgpath, 'wb') as vimg:
        vimg.write(image)

    img = Image.open("vcode.jpg")
    img.show()
    vcode = input("verification code:")
    return vcode


def get_curriculum(s, curl, student_id):
    #获得课表并保存
    headers = {
        "Referer":
        "http://jw2.ahu.cn/xs_main.aspx?xh=" + student_id,
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
    }
    selector = etree.HTML(s.get(curl, headers=headers).content)
    __VIEWSTATE = selector.xpath(
        '//*[@id="Form1"]/input[@name="__VIEWSTATE" ]/@value')[0]
    data = {
        "__VIEWSTATE": __VIEWSTATE,
        "__EVENTTARGET": "ddlXN",
        "__VIEWSTATEGENERATOR": "FDD5582C",
        "ddlXN": "2018-2019",
        "ddlXQ": "1"
    }
    response = s.post(curl, data=data, headers=headers)
    html = response.content.decode('gbk')
    selector = etree.HTML(html)
    courses = selector.xpath(".//table//tr")
    files = []
    for i in courses[1:]:
        course = i.xpath(".//*/text()")
        data = {
            '课程代码': course[1],
            '课程名称': course[2],
            '学分': course[6],
            '上课时间': course[9],
        }
        files.append(data)
    with open('ahu.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(files, indent=2, ensure_ascii=False))
    print("ahu.json已保存到文件夹!")


def main():
    #基本信息输入
    student_id = input("student_id:")
    password = input("password:")
    s = requests.session()
    url = "http://jw2.ahu.cn/default2.aspx"
    vcode_url = "http://jw2.ahu.cn/CheckCode.aspx?"
    curl = "http://jw2.ahu.cn/xsxkqk.aspx?xh=" + student_id + "&xm=%CD%F5%B7%E1&gnmkdm=N121615"
    #函数调用
    code = vcode(s, vcode_url)
    response_landed = landing(s, url, student_id, password, code)
    get_curriculum(s, curl, student_id)


if __name__ == '__main__':
    main()