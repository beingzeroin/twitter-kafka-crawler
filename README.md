# Twitter Kafka crawler
----

Simple demo project using [Twitter's streaming API](https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/connecting) to send messages to [Kafka](https://kafka.apache.org/) and then process them out to [Elasticsearch](https://www.elastic.co/products/elasticsearch) and Postgres.

## Setup
This project requires Python 3. After setting up your virtualenv (I recommend [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)), install the required libraries:
```console
$ pip install -r requirements.txt
```

Then, copy [`config.example.py`](/config.example.py) as `config.py` and fill in the blanks. You'll need API keys for Twitter, which you can get [here](https://apps.twitter.com).

Now, you can use `setup_kafka_es_db.py` to automatically create the Kafka topic, ES index and database tables. You may have to create the Kafka topic manually, though - it worked for me locally, but not on another hosted Kafka instance.

## Usage

Run `stream-producer.py` to start sending Tweets to Kafka. You can specify keywords for the Twitter api with `-t` (ala `-t python,js,java,scala,code,programming,node,technology`) and limit messages read with `--limit`.  

```console
$ python stream-producer.py -h
usage: stream-producer.py [-h] [-l LIMIT] [-t TRACK] [-s]

Twitter stream reader - Kafka producer

optional arguments:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        Limit the amount of tweets that will be read. 0 to
                        disable; defaults to 20.
  -t TRACK, --track TRACK
                        Comma-separated list of keywords to track. Defaults to
                        "python"
  -s, --sample          Use Twitter's sample messages instead of filtering by
                        keywords
```

Run `stream-consumer.py` to start processing messages off of Kafka. The messages will be lightly parsed, and the users and tweets will be saved to the database and indexed in ES.  

```console
$ python stream-consumer.py -h
usage: stream-consumer.py [-h] [-s BATCH_SIZE] [-t SECONDS] [-c SECONDS] [-b]

Twitter stream reader - Kafka consumer

optional arguments:
  -h, --help            show this help message and exit
  -s BATCH_SIZE, --batch-size BATCH_SIZE
                        How many tweets to process in one go. Defaults to 50.
  -t SECONDS, --batch-timeout SECONDS
                        Maximum amount of time to wait for the batch to fill
                        up. Defaults to 2.5 seconds.
  -c SECONDS, --consumer-timeout SECONDS
                        Kafka consumer timeout. Defaults to 0.5 seconds.
  -b, --from-beginning  Seek to topic beginning instead of continuing
```

You can also run `run_app.py` to launch a (very) simple Flask-app for viewing and searching the tweets (with ES). You should be able to access it on `http://localhost:9776` (although it is bound to `0.0.0.0` as well). This can be done while `stream-consumer.py` is running.
