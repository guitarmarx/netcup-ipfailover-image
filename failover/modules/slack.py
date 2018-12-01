import requests


class Slack:

    webhookURL = None
    logger = None

    def __init__(self, webhookURL, logger):
        self.webhookURL = webhookURL
        self.logger = logger

    def sendMessage(self, message):
        message = '{"text" : "' + message + '"}'
        self.logger.info("Try to send Slackmessage: " + message)
        self.logger.info(requests.post(self.webhookURL, data=message))
