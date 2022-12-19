import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import requests

def get_html_email(name, num_skis, top_ski, image, gender, sellers, overall, speed, man, img_code):
    send_email_a = random.random() < 0.5

    seller_code = f'''
            <br>
            <b>Cost</b>
            <br>
            <table>
        '''
    for seller in sellers:
        seller_code += f'''\
            <tr>
            <td> <a href={seller[2]}>{seller[0]}</a>&emsp; </td> <td> ${seller[1]} </td>
            </tr>
        '''

    seller_code += f'''\
            </tr>
            </table>
            <br>
        '''

    seller_code = seller_code if len(sellers) > 0 else "<br>"
    seller_info_sent = seller_code != "<br>"

    image_code = f'<br><img src={image} alt="Your Ski" border="0"><br><br>' if image else "<br>"
    picture_sent = image_code != "<br>"

    email_a_report_line = '''<a href="https://calendly.com/blacker1/carve-product-consultation">If you schedule a 5-minute meeting with us</a>,  <b>we'll send you the full report -- this is 100% free,</b> we just want to find you the perfect skis and chat with our users. No gimmicks, I promise.'''
    email_b_report_line = '''<a href="https://calendly.com/blacker1/carve-product-consultation">If you schedule a 5-minute meeting with us</a>,  <b>we'll send you the full report and venmo you $5</b> -- this is not a gimmick, we just want to find you the perfect skis and chat with our users. I promise.'''
    report_line = email_a_report_line if send_email_a else email_b_report_line
    name_and_intro = f'''\
        <html>
        <body>
        Hey {name},
        <br><br>
        Thanks for using Carve -- I'm a Stanford graduate student who wants to transform how you buy skis, for free.
        <br><br>
        We analyzed >30,000 data points and every ski to find you {num_skis} choices within your ideal dimensions -- our report ranks each. See your top pick below.
        <br><br>
        {report_line}
        <br><br>
        Don't hesitate to reach out. Speak soon.<br><br>

        Best, <br>
        Aaron (<a href="https://www.linkedin.com/in/aaron-blacker-84442369/">LinkedIn</a>) <br><br>
    '''

    top_recommendation = f'''
        -----------------------------------
        <br><br>
        <b><u>Our top recommendation for you:</u></b>
        <br><br>
        <font face="Trebuchet MS">
        <b>{top_ski}</b>
        <br>
        {gender}''' + seller_code + f'''\
        <b>Match scores (performance)</b>
        <br>
        Overall: &emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&nbsp; {"{:.1f}".format(overall)}%
        <br>
        Speed: &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; {"{:.1f}".format(speed)}%
        <br>
        Manueverability: &emsp;&emsp; {"{:.1f}".format(man)}%
        <br>
        </font>
    ''' + image_code + '------------------------------------------------------------  <br><br>' +'''
    <b><u>Your full report</u></b><br>
    <img src="https://i.ibb.co/r611h2F/image-1-1.png" alt="carve" border="0" width="250">
    '''


    recommendation_notes = f'''
        <br>
        <b><u>Notes about your recommendation:</u></b>
        <ul>
            <li><b>Carve delivers the most accurate ski recommendation in the world</b> by analyzing >30,000 data points across every ski on the market (1250+ skis!) against the information you provided
            </li>
            <li><b>We then find you cheapest place to buy it</b> by scanning the web for sellers with your size and model in stock
            </li>
            <li><b>Our recommendations are 100% unbiased</b> — we have no partnerships with ski brands, manufacturers, or retailers</li>
        </ul>
    '''

    conclusion = f'''
        PS --  Join <b><a href="https://discord.com/invite/sebZZds6">our community!</a></b>! Connect with other skiers to share products and experiences.<br><br>
        <a href="https://www.linkedin.com/in/aaron-blacker-84442369/">Aaron Blacker</a>
        <br>
        Founder/CEO, Carve
        <br>
        (914) 844-9628
        <br>
        <img src="https://i.ibb.co/fvhMTVw/carve.png" alt="carve" border="0" width="125">
        <img src=http://emailtrack.herokuapp.com/image?type={img_code}></img>
        </body>
        </html>
    '''

    html = name_and_intro + top_recommendation + recommendation_notes + conclusion

    return html, seller_info_sent, picture_sent, send_email_a

def send_email(name, num_skis, top_ski, image, gender, sellers, overall, speed, man, email):

    sender_email = "carveresearch@gmail.com"
    receiver_email = email
    password = "Sk1sA5eC00l!"

    image_track_url = 'https://emailtrack.herokuapp.com/'
    tracking_payload = {'sender': sender_email,
            'receiver': receiver_email}
    tracking_response = requests.post(image_track_url, data=tracking_payload)
    img_code = tracking_response.text.split("img src")[-1].split("type=")[-1].split('&')[0]

    html_email, seller_info_sent, picture_sent, sent_email_a = get_html_email(name, num_skis, top_ski, image, gender, sellers, overall, speed, man, img_code)
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your Carve Ski Recommendation!"
    message["From"] = sender_email
    message["To"] = receiver_email

    message.attach(MIMEText(html_email, 'html'))

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

    return name, receiver_email, seller_info_sent, picture_sent, sent_email_a
