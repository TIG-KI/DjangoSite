from django.shortcuts import render, render_to_response
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
import pymysql
import requests
import json

# Create your views here.

# 连接mysql数据库
con = pymysql.Connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="199745",
    db="python",
    charset="utf8"
)


def index(request):  
    return render(request, "cmdb/login.html")

#登录验证
def login(request):
    jfun()
    #return HttpResponse("hello")
    movie_list = []
    #防止直接输入URL就能进入登录成功后的界面
    if request.method == "POST":

        #获取用户输入的值
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)

        #获取游标
        cursor = con.cursor()

        #编写sql语句
        sql = "select * from user where username='" + username+"'"
        print(sql)
        #向服务器发送sql语句
        cursor.execute(sql)

        if len(cursor.fetchall()) != 0:
            cursor.execute(sql)
            for x in cursor.fetchall():
                print(x[2])
                if x[2] == password:
                    sql = "select * from json"

                    # 向服务器发送sql语句
                    cursor.execute(sql)
                    for x in cursor.fetchall():
                        dict = {}
                        dict["rate"] = x[0]
                        dict["title"] = x[1]
                        dict["url"] = x[2]
                        dict["cover"] = x[3]
                        movie_list.append(dict)
                    return render(request, "cmdb/success.html", {"info": username, "data": movie_list})
                    #return render_to_response(request, "cmdb/success.html", locals())
                else:
                    return render(request, "cmdb/login.html", {"info": "密码错误"})
        else:
            return render(request, "cmdb/login.html", {"info": "账号不存在！"})
    else:
        return render(request, "cmdb/login.html", {"info": "请求错误!"})

def register(request):
    return render(request, "cmdb/addUser.html")

def addUser(request):

    movie_list = []

    username = request.POST.get("username", None)
    password = request.POST.get("password", None)

    print("%s %s" % (username, password))

    if len(username)!= 0 and len(password)!=0:
        #获取游标
        cursor = con.cursor()

        #编写sql语句
        sql = "insert into  user(username,password) values ('%s','%s')"
        data = (username, password)

        #向服务器发送sql语句
        cursor.execute(sql % data)
        con.commit()

        sql = "select * from json"

        # 向服务器发送sql语句
        cursor.execute(sql)
        for x in cursor.fetchall():
            dict = {}
            dict["rate"] = x[0]
            dict["title"] = x[1]
            dict["url"] = x[2]
            dict["cover"] = x[3]
            movie_list.append(dict)

        return render(request, "cmdb/success.html", {"info": username, "data": movie_list})
    else:
        return render(request, "cmdb/addUser.html", {"info": "错误"})


def jfun():
    con = pymysql.Connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="199745",
        db="python",
        charset="utf8"
    )

    cursor = con.cursor()

    for a in range(1, 4):
        url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start={}"
        url2 = url.format(a*20)
        print(url2)
        data = requests.get(url2).text
        list = json.loads(data)
        # print(list)
        # print(type(list))
        #得到需要的内容
        movoeList = list.get("subjects")
        print(movoeList)
        # print(type(movoeList))
        for x in movoeList:
            sql = "insert into json(rate,title,url,cover) values ('%s','%s','%s','%s')"
            data = (x.get("rate"), x.get("title"),
                    x.get("url"), x.get("cover"))
            cursor.execute(sql % data)
            con.commit()
    cursor.close()
    con.close()
