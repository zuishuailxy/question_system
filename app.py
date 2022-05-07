from flask import Flask, session, g
from extensions import db, mail
from blueprints import qa_bp
from blueprints import user_bp
from flask_migrate import Migrate
from models import UserModel
import config

app = Flask(__name__)
# Binging config
app.config.from_object(config)
# Bing database
db.init_app(app)
mail.init_app(app)

# Data migrate
migrate = Migrate(app, db)

# Register Blueprint
app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)


# 钩子函数
@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # 绑定全局变量{'user' : user}
            # setattr(g, 'user', user)
            g.user = user

        except:
            g.user = None


# 执行顺序 ： request来了 => before_request -> 视图函数 -> 视图函数中返回模版 -> context_processor
# 上下文处理器
@app.context_processor
def context_processor():
    # 如果绑定了 user
    if hasattr(g, 'user'):
        return {'user': g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run()
