FROM tiangolo/uvicorn-gunicorn:python3.10-slim

LABEL maintainer="ranyong"

# 设置工作目录
WORKDIR /sk2

# 复制并安装 Python 依赖
COPY requirements.txt /sk2/requirements.txt

# 升级 pip 并安装依赖
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r /sk2/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 复制项目文件
COPY . /sk2

# 设置容器启动命令
CMD ["python", "main.py"]