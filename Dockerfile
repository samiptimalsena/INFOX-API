FROM python:3.8.13-buster

RUN apt update
RUN apt-get install libsndfile1 -y

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app

ENV FLASK_APP=app/app.py
ENV UPLOAD_FOLDER=app/UPLOADS
ENV SECRET_KEY=infox9876
ENV MONGO_URI=mongodb+srv://infoxapi:CPWcGqI01Y5HQiLi@cluster0.wr85z.mongodb.net/myFirstDatabase?retryWrites=true&w=majority

CMD ["flask","run","--host=0.0.0.0"]
