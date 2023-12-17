from flask_mail import Message
from flask import render_template
from flask_mail import Mail

mail = Mail()

def send_email(subject, recipient, body):
    msg = Message(subject, recipients=[recipient])
    msg.html = body
    mail.send(msg)
