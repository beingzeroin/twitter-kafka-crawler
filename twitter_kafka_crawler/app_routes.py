import flask

import sqlalchemy as sqa
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from twitter_kafka_crawler import app, db, models

MAX_RESULTS = 1000


@app.route('/')
def app_index():
	# Turn '' to None
	search_terms = flask.request.args.get('q') or None

	if search_terms:
		tweets = search_tweets(search_terms)
	else:
		tweets = models.Tweet.query.options(sqa.orm.joinedload('user')).order_by(models.Tweet.created_time.desc()).limit(MAX_RESULTS)

	return flask.render_template(
		'index.html.j2',
		search_terms=search_terms,
		tweets=tweets
	)


@app.route('/user/<int:user_id>')
def app_user(user_id):
	user = models.User.query.get(user_id)
	if not user:
		return flask.abort(404)

	return flask.render_template(
		'user.html.j2',
		user=user
	)


def search_tweets(search_terms):
	es_client = Elasticsearch(hosts=app.config['ELASTICSEARCH_HOSTS'])

	search = Search(using=es_client, index=app.config['ELASTICSEARCH_INDEX']).query(
		'simple_query_string',
		default_operator='AND',
		query=search_terms
	).sort('-created_time')[0:MAX_RESULTS]

	return search.execute()
