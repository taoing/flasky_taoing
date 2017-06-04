import os

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'passwordpwd'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
	FLASKY_MAIL_SENDER = 'Flasky Admin <529982750@qq.com>'
	FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or '529982750@qq.com'
	FLASKY_POSTS_PER_PAGE = 20
	FLASKY_FOLLOWERS_PER_PAGE = 20
	FLASKY_FOLLOWED_PER_PAGE = 20
	FLASKY_COMMENTS_PER_PAGE = 20
	SQLALCHEMY_RECORD_QUERIES = True
	FLASKY_SLOW_DB_QUERY_TIME = 0.5

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.qq.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/data_dev'

class TestingConfig(Config):
	TESTING = True
	WTF_CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/data_test'

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:password@localhost:3306/data_prod'

	@classmethod
	def init_app(cls,app):
		Config.init_app(app)

		import logging
		from logging.handlers import SMTPHandler
		credentials=None
		secure=None
		if getattr(cls,'MAIL_USERNAME',None) is not None:
			credentials=(cls.MAIL_USERNAME,cls.MAIL_PASSWORD)
			if getattr(cls,'MAIL_USE_SSL',None):
				secure=()
		mail_handler=SMTPHandler(
			mailhost=(cls.MAIL_SERVER,cls.MAIL_PORT),
			fromaddr=cls.FLASKY_MAIL_SENDER,
			toaddrs=[cls.FLASKY_ADMIN],
			subject=cls.FLASKY_MAIL_SUBJECT_PREFIX+'Application Error',
			credentials=credentials,
			secure=secure)
		mail_handler.setLevel(logging.ERROR)
		app.logger.addHandler(mail_handler)

class HerokuConfig(ProductionConfig):
	@classmethod
	def init_app(cls, app):
		ProductionConfig.init_app(app)
		# 输出到stderr
		import logging
		from logging import StreamHandler
		file_handler = StreamHandler()
		file_handler.setLevel(logging.WARNING)
		app.logger.addHandler(file_handler)

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
	}