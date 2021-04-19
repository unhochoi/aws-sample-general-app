FROM python:3

RUN apt-get update
RUN apt-get install python3-pip -y
RUN pip3 install virtual env

WORKDIR /home/ubuntu/aws-sample-general-app-master
COPY . .
RUN mkdir -p static/uploads

RUN virtualenv venv
RUN . venv/bin/activate
RUN pip3 install -r requirements.txt

RUN cp ./main.service /etc/systemd/system/

EXPOSE 5000

CMD ["systemctl", "start", "main"]
CMD ["systemctl", "enable", "main"]
