import smtplib

def send_email(email, subject, message):
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("verify.sage@gmail.com", "Google0912!")
    msg = "\r\n".join([
        "From: verify.sage@gmail.com",
        "To: " + email,
        "Subject: " + subject,
        "",
        message
    ])
    server.sendmail("verify.sage@gmail.com", email, msg)
    server.quit()