from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@172.17.0.2:3306/web'

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
        todos.append(todo)
    return render_template("todo.html", todos=todos)

@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    #为了在容器外能访问容器内，这样设置
    app.run(host='0.0.0.0', port=5000, debug=True)


