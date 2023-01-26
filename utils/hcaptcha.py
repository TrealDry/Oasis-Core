from config import Security
from flask_hcaptcha import hCaptcha


hcaptcha = hCaptcha(site_key=Security.SITE_KEY,
                    secret_key=Security.SECRET_KEY)


def init_hc(app):
    hcaptcha.init_app(app)

