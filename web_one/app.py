from flask import Flask, render_template, request
import json
import time
import datetime
import mysql.connector

#https://hub.docker.com/_/mysql

app = Flask(__name__)

# MYSQL连接配置
config = {
    #'host': '172.17.0.2',
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123',
}

#创建mysql连接对象
conn = mysql.connector.connect(**config)


@app.route('/createdatabase')
def create_database():
    cursor = conn.cursor()
    #创建数据库
    cursor.execute('CREATE DATABASE IF NOT EXISTS web_one')
    #选择数据库
    cursor.execute('USE web_one')
    #创建数据表
    cursor.execute("CREATE TABLE IF NOT EXISTS message (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100), message VARCHAR(255), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP )")
    cursor.close()
    return 'Database and table created successfully!'

@app.route('/temperature')
def temperature():
    with open("sitka_weather_2014.csv", "rt") as f1:
        data = f1.read()
        data_split = data.split('\n')
        return_data = []
        for one_ in data_split:
            if one_:
                one_split = one_.split(',')
                return_data.append(one_split[-1])
    return render_template('temperature.html', contents=str(return_data[1:]))


@app.route('/population')
def population():
    with open('population_data.json', 'rt') as f2:
        data = json.loads(f2.read())
        return render_template('population_data.html', contents=data)

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    todos = []
    if request.method == 'POST':
        todo = request.form.get('todo')
        username = request.form.get('username')
        if todo:
            if not username:
                username = '匿名用户'
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 创建游标对象
            cursor = conn.cursor()
            # 选择要使用的数据库
            cursor.execute("USE web_one")  # 替换为实际的数据库名称
            # 定义插入数据的SQL语句
            insert_query = "INSERT INTO message (name, message, created_at) VALUES (%s, %s, %s)"
            # 定义要插入的数据
            data = (username, todo, current_time)  # 替换为你要插入的实际数据
            # 执行插入操作
            cursor.execute(insert_query, data)
            # 提交事务
            conn.commit()

            # 关闭游标和数据库连接
            cursor.close()
            #conn.close()

    # 创建游标对象
    cursor = conn.cursor()

    # 执行查询操作
    query = "SELECT * FROM message"
    cursor.execute(query)

    # 获取所有查询结果
    results = cursor.fetchall()
    # 打印查询结果
    for row in results:
        todos.append(f"{row[1]} -- {row[2]} -- {row[3]}")
        print(type(row))

    # 关闭游标和数据库连接
    cursor.close()
    return render_template("todo.html", todos=todos)


@app.route('/logon')
def logon():
    return render_template("logon.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phonenum = request.form.get("phonenum")
        checknum = request.form.get("checknum")
    return render_template("index.html")


@app.route('/')
def index():
    #main page
    return render_template("index.html")


if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0')
    app.run(debug=True)


