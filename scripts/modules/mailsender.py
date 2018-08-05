import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mailsender:

    smtpServer = ""
    smtpPort = ""
    smtpUser = ""
    smtpPassword = ""
    smtpSourceMail = ""
    smtpTargetMail = ""
    logger = ""

    def __init__(smtpServer, smtpPort, smtpUser, smtpPassword, smtpSourceMail, smtpTargetMail, logger):
        self.smtpServer = smtpServer
        self.smtpPort = smtpPort
        self.smtpPassword = smtpPassword
        self.smtpSourceMail = smtpSourceMail
        self.smtpTargetMail = smtpTargetMail
        self.logger = logger

    def sendNotification(subject, body):
        # Message definition
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = smtpSourceMail
        msg['To'] = smtpTargetMail
        msg.attach(MIMEText(body, 'plain'))

        # Open Connection
        server = smtplib.SMTP(smtpServer, smtpPort)
        server.starttls()
        server.login(smtpUser, smtpPass)

        # Send Mail
        logger.debug('sending message to ' + self.smtpSourceMail)
        server.sendmail(smtpSourceMail, [smtpTargetMail], msg.as_string())
        server.quit()
