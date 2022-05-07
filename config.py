# 数据库的配置变量
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'questions_system'
USERNAME = 'root'
PASSWORD = 'Wodeshe520,'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = '123321'

# 邮箱配置
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = 'zuishuailxy@gmail.com'
MAIL_PASSWORD = 'wdlyhldjzajobijg'
MAIL_DEFAULT_SENDER = 'zuishuailxy@gmail.com'
