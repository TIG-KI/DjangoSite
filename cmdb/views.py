from django.shortcuts import render
from django.shortcuts import HttpResponse
import pymysql

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

    #return HttpResponse("hello")
    user_list = []
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
                    sql = "select * from user"

                    # 向服务器发送sql语句
                    cursor.execute(sql)
                    for x in cursor.fetchall():
                        dict = {}
                        dict["id"] = x[0]
                        dict["username"] = x[1]
                        dict["password"] = x[2]
                        user_list.append(dict)
                    return render(request, "cmdb/success.html", {"info": username, "data": user_list})
                else:
                    return render(request, "cmdb/login.html", {"info": "密码错误"})
        else:
            return render(request, "cmdb/login.html", {"info": "账号不存在！"})
    else:
        return render(request, "cmdb/login.html", {"info": "请求错误!"})

