import json
import logging


class Config:
    config: dict = {}
    connectionString: str = None
    tg_bot_token: str = None
    tg_log_channel: str = None

    def init_config(self):
        logging.info("Loading config file...")
        with open('services.json') as conf_file:
            conf = json.load(conf_file)
            self.config = conf
            self.tg_bot_token = conf['telegram']['bot_token']
            self.tg_log_channel = conf['telegram']['log_channel']
            self.connectionString = conf['mongo']['connectionString']

        logging.info("All vars loaded")

    def get_config(self):
        return self.config


