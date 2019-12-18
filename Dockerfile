FROM python:3.7

ENV APP_HOME /app

# Download 
RUN apt-get update && apt-get install -y gcc

ADD . ${APP_HOME}
WORKDIR ${APP_HOME}

RUN pip install -r requirements.txt

# Run the web service on container startup. 
# TODO: Add argument to specify data dir, allowing us to be more dynamic with data/
# TODO: /app/app/app.py is confusing
EXPOSE 8080
CMD python main.py