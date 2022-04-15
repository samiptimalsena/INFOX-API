FROM python:3.8.13-buster
RUN apt update
RUN apt-get install libsndfile1 -y
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN pip install --ignore-installed numpy==1.21
COPY . /app
ENV FLASK_APP=app/app.py
ENV UPLOAD_FOLDER=app/UPLOADS
ENV SECRET_KEY=sample
ENV MONGO_URI=mongodb+srv://infoxapi:CPWcGqI01Y5HQiLi@cluster0.wr85z.mongodb.net/myFirstDatabase?retryWrites=true&w=majority
CMD ["flask","run","--host=0.0.0.0"]
