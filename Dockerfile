FROM python:3.7

ENV APP_HOME /app

# Download 
RUN apt-get update && apt-get install -y gcc

ADD . ${APP_HOME}
WORKDIR ${APP_HOME}

RUN pip install -r requirements.txt

# Run the web service on container startup. 
EXPOSE 8080
ENV FLASK_APP=main.py
CMD flask run -h 0.0.0.0 -p 8080