FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install django-sslserver
RUN pip install tabula-py
RUN pip install hickory

RUN apt-get update \
    && apt-get install -y openjdk-11-jdk \
    && apt-get install -y ant \
    && apt-get clean;

RUN mkdir -p /usr/share/nltk_data \
    && cd /usr/share/nltk_data \
    && mkdir -p sentiment corpora \
    && curl https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/stopwords.zip > corpora/stopwords.zip \
    && curl https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/sentiment/vader_lexicon.zip > sentiment/vader_lexicon.zip

COPY . /code/