import smtplib
from email.mime.text import MIMEText
from random import randrange


def send_verify_mail(email):
    code = randrange(100000, 999999)

    subject = "NotBurada Doğrulama Kodu"

    body = """\
    <html>
    <head> </head>
    <body> <h3>NotBurada'ya üye olduğunuz için teşekkürler! Doğrulama Kodunuz:  </h3>
    <h1 style="font-size: 30px" > {} </h1></body>
    </html>

        """.format(
        code
    )

    sender = "notburadabilisim@gmail.com"
    recipients = [email]
    password = "ppaa uiev vygq jwzp "

    def send_email(subject, body, sender, recipients, password):
        msg = MIMEText(body, "HTML")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Message sent!")

    send_email(subject, body, sender, recipients, password)

    return code
