import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import requests


def get_html_email(img_code):
    return f'''\
        <html>
        <body>
        <img src=http://emailtrack.herokuapp.com/image?type={img_code}></img>
        </body>
        </html>
    '''

def send_email():

    sender_email = "carveresearch@gmail.com"
    receiver_email = "dhruva.bansal00@gmail.com"

    url = 'https://emailtrack.herokuapp.com/'
    myobj = {'sender': sender_email,
            'receiver': receiver_email}

    x = requests.post(url, data = myobj)

    img_code = x.text.split("img src")[-1].split("type=")[-1].split('&')[0]

    password = "Sk1sA5eC00l!"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Your Carve Ski Recommendation!"
    message["From"] = sender_email
    message["To"] = receiver_email

    message.attach(MIMEText(get_html_email(img_code), 'html'))

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

send_email()