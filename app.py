from routes import *
from flask import Flask
from config import Kernel
from utils.hcaptcha import *


app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024

init_hc(app)

app.register_blueprint(web)
app.register_blueprint(misc)
app.register_blueprint(user)
app.register_blueprint(level)
app.register_blueprint(score)
app.register_blueprint(account)
app.register_blueprint(comment)
app.register_blueprint(message)
app.register_blueprint(levelpack)
app.register_blueprint(relationship)


if __name__ == "__main__":
    app.run(debug=Kernel.DEBUG,
            host=Kernel.IP,
            port=Kernel.PORT)
