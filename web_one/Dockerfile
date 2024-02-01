#使用python3.9作为基础镜像
FROM python:3.9

#设置工作目录
WORKDIR /app

#将项目文件复制到工作目录
COPY . /app

#安装项目依赖
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

#暴露flask应用的默认端口
EXPOSE 5000

#启动flask应用
CMD ["python3", "app.py"]