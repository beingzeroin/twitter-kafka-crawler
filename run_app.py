#!/usr/bin/env python3
from twitter_kafka_crawler import app

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9776, debug=True)
