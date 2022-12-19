from os import link
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import requests

def get_email_a_main():
    return '<a href="https://calendly.com/blacker1/The-Carve-ski-fitting">Schedule a 5-minute meeting</a> and we\'ll find you the #1 perfect ski at the cheapest price and send you the report afterwards.'

def get_email_b_main(costs, links):
    num_skis = int(random.random() * 23) + 6
    return f'''
        We analyzed >30,000 data points and every ski (1,265) to find you {num_skis} options. We\'d love to help you narrow down to the #1 perfect skis for you.
        <br><br>
        <table>
        <tr>
        <td> <img src="https://i.ibb.co/18YWCgW/report-only.png" alt="carve" border="0" width="250"></img> </td> <td> <img src="https://i.ibb.co/NxWKVSr/consultation.png" alt="carve" border="0" width="250"></img> </td> <td> <img src="https://i.ibb.co/VWJ7K3K/e2e.png" alt="carve" border="0" width="250"></img> </td>
        </tr>
        <tr>
        <td> <a href="{links[0]}"> <img src="{costs[0]}" alt="carve" border="0" width="250"></img></a> </td> <td> <a href="{links[1]}">  <img src="{costs[1]}" alt="carve" border="0" width="250"></img> </a> </td> <td> <a href="{links[2]}"> <img src="{costs[2]}" alt="carve" border="0" width="250"></img> </a> </td>
        </tr>
        </tr>
        </table>
    '''

def get_html_email(name, email, img_code, send_email_a):
    cost_options = [
        ["https://i.ibb.co/pjDH5MQ/0dollars.png", "https://i.ibb.co/PxhjqPp/nineteendollars.png", "https://i.ibb.co/McHhnZz/fourtyninedollars.png"],
        ["https://i.ibb.co/tYpL8yB/ninedollars.png", "https://i.ibb.co/FDhVLhK/twentyninedollars.png", "https://i.ibb.co/0ZkRLdN/ninetyninedollars.png"],
        ["https://i.ibb.co/PxhjqPp/nineteendollars.png", "https://i.ibb.co/McHhnZz/fourtyninedollars.png", "https://i.ibb.co/GRtWtkD/oneninetyninedollars.png"],
    ]
    links = [f"https://docs.google.com/forms/d/e/1FAIpQLSf1E5Zt204EcOmphuu9qGdmQ4Psj-itDdt8NAdASvhDWXMjlQ/viewform", "https://calendly.com/blacker1/the-carve-ski-fitting", "https://calendly.com/blacker1/carve-end-to-end"]
    cost_option_index = random.choice([0, 1, 2])
    options = get_email_a_main() if send_email_a else get_email_b_main(cost_options[cost_option_index], links)
    name_and_intro = f'''\
        <html>
        <body>
        Hey {name},
        <br><br>
        Thanks for using Carve -- we're Stanford graduate students making finding the perfect ski fast and easy.
        <br><br>
        ''' +  options + f'''\
        <br><br>
        Don't hesitate to reach out. Speak soon.
        <br><br>
        <a href="https://www.linkedin.com/in/aaron-blacker-84442369/">Aaron</a>
        <br>
        Founder, Carveresearch.com
        <br>
        <img src="https://i.ibb.co/fvhMTVw/carve.png" alt="carve" border="0" width="125"></img>
        <img src=http://emailtrack.herokuapp.com/image?type={img_code}></img>
        </body>
        </html>
    '''

    html = name_and_intro
    return html, send_email_a, cost_option_index

def send_email(name, email, send_email_a):

    sender_email = "postmaster@mg.carveresearch.com"
    receiver_email = email
    password = "2abe6919810aad106b294c0ef4a9e02b-162d1f80-4484aa84"

    gmail_address = "carveskiresearch@gmail.com"
    image_track_url = 'https://emailtrack.herokuapp.com/'
    tracking_payload = {'sender': gmail_address,
            'receiver': receiver_email}
    tracking_response = requests.post(image_track_url, data=tracking_payload)
    img_code = tracking_response.text.split("img src")[-1].split("type=")[-1].split('&')[0]

    html_email, sent_email_a, cost_option_index = get_html_email(name, email, img_code, send_email_a)
    message = MIMEMultipart("alternative")
    message["Subject"] = "Finding you the perfect ski, 10x easier"
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Reply-To"] = gmail_address

    message.attach(MIMEText(html_email, 'html'))

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.mailgun.org", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

    return name, receiver_email, sent_email_a, cost_option_index

if __name__ == "__main__":
    send_email("Rajas", "rajasb@stanford.edu", True)
