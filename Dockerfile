FROM python:3

RUN apt-get update
RUN apt-get install python3-pip -y
RUN pip3 install virtualenv

WORKDIR /home/ubuntu/aws-sample-general-app-master
COPY . .
RUN mkdir -p static/uploads

RUN virtualenv venv
RUN . venv/bin/activate
RUN pip3 install -r requirements.txt

EXPOSE 80

CMD ["python", "./main.py"]
