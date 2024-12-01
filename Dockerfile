FROM python:3.9

# 定義對應的app folder
WORKDIR  /app

# 把所有文件複製到app folder裡面
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# 定義fastapi的運行port
EXPOSE 8000

# CMD 設定這個image被跑起來時的預設指令
# reload 如果更新，自行加載
CMD [ "uvicorn", "main:app", "--reload", "--port=8000", "--host=0.0.0.0" ]