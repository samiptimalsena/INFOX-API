FROM python:3.8.13-buster

RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc libsndfile1 

WORKDIR /INFOX
COPY ./requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=app/app.py
ENV UPLOAD_FOLDER=app/UPLOADS
ENV SECRET_KEY=infox9876
ENV MONGO_URI=mongodb+srv://infoxapi:CPWcGqI01Y5HQiLi@cluster0.wr85z.mongodb.net/myFirstDatabase?retryWrites=true&w=majority

CMD ["flask","run","--host=0.0.0.0"]
