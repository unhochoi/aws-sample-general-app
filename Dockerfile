# BASE image를 python 3+로 지정
FROM python:3

# container 내 작업 directory 지정
WORKDIR /app

# host의 파일 및 폴더를 container에 복사
COPY . .

# 명령어를 실행하며, 새로운 image layer 생성
RUN pip install --no-cache-dir -r requirements.txt

# container에서 열어줄 port
EXPOSE 5000

# container 실행 시, 입력되는 명령어
CMD ["python", "./app.py"]
