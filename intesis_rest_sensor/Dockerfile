FROM python
MAINTAINER Bradley Scott

COPY . /app
WORKDIR /app

RUN pip install requests
RUN pip install -r requirements.txt

CMD python app.py