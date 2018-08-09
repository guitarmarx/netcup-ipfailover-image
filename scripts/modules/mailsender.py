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

    def __init__(self, smtpServer, smtpPort, smtpUser, smtpPassword, smtpSourceMail, smtpTargetMail, logger):
        self.smtpServer = smtpServer
        self.smtpPort = smtpPort
        self.smtpPassword = smtpPassword
        self.smtpSourceMail = smtpSourceMail
        self.smtpTargetMail = smtpTargetMail
        self.logger = logger

    def sendNotification(self, subject, body):
        # Message definition
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.smtpSourceMail
        msg['To'] = self.smtpTargetMail
        msg.attach(MIMEText(body, 'plain'))

        # Open Connection
        server = smtplib.SMTP(self.smtpServer, self.smtpPort)
        server.starttls()
        server.login(self.smtpUser, self.smtpPassword)

        # Send Mail
        self.logger.debug('sending message to ' + self.smtpSourceMail)
        server.sendmail(self.smtpSourceMail, [
                        self.smtpTargetMail], msg.as_string())
        server.quit()

    def buildMailBody(self, logMessages):
        return None
