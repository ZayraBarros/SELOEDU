import os


class Config:
	SECRET_KEY = os.environ.get('FLASK_SECRET', 'dev-secret')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///seloedu.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
	DEBUG = True
	# MAIL_SERVER = "localhost"
	# MAIL_PORT = 1025
	# MAIL_USE_TLS = False
	# MAIL_USERNAME = " "
	# MAIL_PASSWORD = " "
	# MAIL_DEPAULT_SENDER = "reset_password@seloedu"

	MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
	MAIL_PORT = int(os.environ.get('MAIL_PORT', 1025))
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'False').lower() == 'true'
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
	MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'newpassword@seloedu.com')
	
	UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
	THUMBNAIL_SIZE = (200, 200)
	MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
