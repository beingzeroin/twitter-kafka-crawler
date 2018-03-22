#!/usr/bin/env python3
import os
import sys

import kafka
import elasticsearch

# Allows importing the config.py file even if ran from other directories
_here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(_here)

import config
from twitter_kafka_crawler import db, models

# Simple Elasticsearch index (no special analysers)
ELASTICSEARCH_INDEX_BODY = {
	'settings' : {
		'index': {
			'number_of_shards' : 1,
			'number_of_replicas' : 0,
			'mapper' : {
				'dynamic' : False
			},
			'query' : {
				'default_field' : 'text'
			},
		}
	},

	'mappings' : {
		'tweet' : {
			'_all' : {
				'enabled' : False
			},
			'properties' : {
				'user_id' : { 'type' : 'long' },

				# Simply store the usernames, don't index
				'user_name' : { 'enabled' : False },
				'user_screen_name' : { 'enabled' : False },

				'text' : { 'type' : 'text' },
				'created_time' : { 'type' : 'date', 'format': 'epoch_millis' },
			}
		}
	}
}


if __name__ == '__main__':
	kafka_client = kafka.client.KafkaClient(**config.KAFKA_CONNECT_OPTIONS)

	# Check if Kafka is set up
	if config.KAFKA_TOPIC not in kafka_client.cluster.topics():
		print('Kafka topic missing, creating: {!r}'.format(config.KAFKA_TOPIC))

		kafka_client.add_topic(config.KAFKA_TOPIC)
		kafka_client.poll()

	es_client = elasticsearch.Elasticsearch(hosts=config.ELASTICSEARCH_HOSTS)

	# Check if ES is set up
	if not es_client.indices.exists(config.ELASTICSEARCH_INDEX):
		print('ES index missing, creating: {!r}'.format(config.ELASTICSEARCH_INDEX))
		es_client.indices.create(config.ELASTICSEARCH_INDEX, body=ELASTICSEARCH_INDEX_BODY)

	# Create databse tables
	db.create_all()
	db.session.commit()
