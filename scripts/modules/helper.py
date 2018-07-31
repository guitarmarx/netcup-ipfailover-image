import os
from ConfigParser import SafeConfigParser


def getMessages(file):
    parser = SafeConfigParser()
    parser.read('file')
    return parser


def isPingable(ip):
    command = "ping -c 1 -W 4 " + ip + " > /dev/null 2>&1"
    response = os.system(command)

    if response == 0:
        return True
    else:
        return False


def initLogging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(config.get('logging', 'logFormat'))

    # Init file logging
    handler = logging.FileHandler(config.get('logging', 'logFile'))
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Init console logging
    handler2 = logging.StreamHandler()
    handler2.setFormatter(formatter)
    logger.addHandler(handler2)


def sendNotification(body, returnmessage):

    try:
        # Message definition
        msg = MIMEMultipart()
        msg['Subject'] = 'Backend Info'
        msg['From'] = smtp_source_mail
        msg['To'] = smtp_target_mail
        body = body + returnmessage
        msg.attach(MIMEText(body, 'plain'))

        # Open Connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)

        # Send Mail
        server.sendmail(smtp_source_mail, [smtp_target_mail], msg.as_string())
        server.quit()
        logger.info('Mail notifiaction sent')
    except Exception as e:
        logger.error(str(e))

    return
