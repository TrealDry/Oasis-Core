import smtplib
from config import Security
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


letter_types = {
    1: "Activate your account | PleasantSpace",
    2: "Password recovery | PleasantSpace"
}


def sending_letter(type_letter, basic_data):
    msg = MIMEMultipart()

    msg['From'] = basic_data["sender"]
    msg['To'] = basic_data["recipient"]
    msg['Subject'] = letter_types[type_letter]

    msg.attach(MIMEText(basic_data["message"], 'plain'))
    text = msg.as_string()

    with smtplib.SMTP_SSL(Security.MAIL_SERVER, 465) as server:
        server.login(Security.MAIL_LOGIN, Security.MAIL_PASSWORD)
        server.sendmail(basic_data["sender"], basic_data["recipient"], text)
        server.quit()
