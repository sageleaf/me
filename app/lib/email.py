import smtplib
from config import SAGELEAF_EMAIL_ADDRESS, GMAIL_EMAIL_ADDRESS, GMAIL_PASSWORD

def send_email(email, subject, message):
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(GMAIL_EMAIL_ADDRESS, GMAIL_PASSWORD)
    msg = "\r\n".join([
        "From: " + SAGELEAF_EMAIL_ADDRESS,
        "To: " + email,
        "Subject: " + subject,
        "",
        message
    ])
    server.sendmail(GMAIL_EMAIL_ADDRESS, email, msg)
    server.quit()