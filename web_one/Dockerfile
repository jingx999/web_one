#设置基础镜像
FROM python:3.9

#设置工作目录
WORKDIR /app
#复制项目文件到容器中
COPY . /app
#安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
#暴露应用程序端口
EXPOSE 5000
#运行应用程序
CMD ["python3", "app.py"]
