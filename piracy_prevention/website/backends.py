import smtplib, os
import email.message
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from base64 import b64decode


def sendMail(activation_id, email_recv):
    mail_template = os.path.dirname(os.path.abspath(__file__))
    email_content = open(mail_template+'/templates/email-template.html', 'r').read()
    email_content = email_content.replace('@(ACTIVATION)', activation_id)
    email_content = email_content.replace('@(USERNAME)', email_recv)

    msg = email.message.Message()
    msg['Subject'] = 'Activation for Piracy Prevention System'

    msg['From'] = ''
    msg['To'] = email_recv
    password = str(b64decode(''))[2:-1]
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(email_content)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    s.login( msg['From'], password)
 
    s.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))