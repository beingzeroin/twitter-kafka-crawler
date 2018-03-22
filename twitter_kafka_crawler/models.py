import sqlalchemy as sqa

from twitter_kafka_crawler import db


class User(db.Model):
	__tablename__ = 'users'

	id = sqa.Column(sqa.BigInteger, primary_key=True)

	name = sqa.Column(sqa.String, nullable=False)
	screen_name = sqa.Column(sqa.String, nullable=False, index=True)

	description = sqa.Column(sqa.String)
	created_time = sqa.Column(sqa.DateTime, nullable=False)

	tweets = sqa.orm.relationship('Tweet', order_by=lambda: Tweet.id.desc())


class Tweet(db.Model):
	__tablename__ = 'tweets'

	id = sqa.Column(sqa.BigInteger, primary_key=True)
	user_id = sqa.Column(sqa.BigInteger, sqa.ForeignKey('users.id'), nullable=False, index=True)

	text = sqa.Column(sqa.String, nullable=False)
	created_time = sqa.Column(sqa.DateTime, nullable=False)

	user = sqa.orm.relationship('User', uselist=False)
