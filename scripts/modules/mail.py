import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


smtpServer = ""
smtpPort = ""
smtpUser = ""
smtpPass = ""
smtpSourceMail = ""
smtpTargetMail = ""


smtpServer = os.environ["SMTP_SERVER"]
smtpPort = os.environ["SMTP_PORT"]
smtpUser = os.environ["SMTP_USER"]
smtpPass = os.environ["SMTP_PASS"]
smtpSourceMail = os.environ["SMTP_SOURCE_MAIL"]
smtpTargetMail = os.environ["SMTP_TARGET_MAIL"]


class Mail:

    def __init__(self, )
