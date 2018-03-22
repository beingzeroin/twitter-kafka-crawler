# Get these from https://apps.twitter.com
TWITTER_API_CONFIGURATION = {
	# App keys
	'consumer_key': 'aaaaaaaaaaaaaaaaaaaaaaaaa',
	'consumer_secret': 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
	# User keys
	'access_token_key' : 'cccccccccccccccccc-ccccccccccccccccccccccccccccccc',
	'access_token_secret' : 'ddddddddddddddddddddddddddddddddddddddddddddd'
}


KAFKA_TOPIC = 'tweets'
KAFKA_CONNECT_OPTIONS = {
	'bootstrap_servers' : [
		'localhost:9092'
	],
	# Uncomment these if your Kafka instance is behind SSL (and you have the certs)
	# 'security_protocol': 'SSL',
	# 'ssl_cafile': 'ca.pem',
	# 'ssl_certfile': 'service.cert',
	# 'ssl_keyfile': 'service.key',
}


ELASTICSEARCH_HOSTS = [
	'localhost:9200'
	# 'https://user:pass@host:port'
]
ELASTICSEARCH_INDEX = KAFKA_TOPIC


SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://user:pass@host:port/tweets'
