import configparser
import os

project_root = os.path.dirname(os.path.dirname(__file__))


class Settings:
    def __init__(self, file):
        self.parser = configparser.ConfigParser()
        file = f'{project_root}/resources/{file}'
        self.parser.read(file)

    def getParser(self):
        return self.parser
