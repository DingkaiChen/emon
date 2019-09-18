import os
from dotenv import load_dotenv

basedir=os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'env'))

class Config(object):
	MAIL_SERVER=os.environ.get('MAIL_SERVER')
	MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
	MAIL_DATABASE=os.environ.get('MAIL_DATABASE')
