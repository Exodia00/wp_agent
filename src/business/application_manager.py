from flask import current_app


class ApplicationManager:

    @staticmethod
    def start():
        current_app.config['ENABLED'] = True

    @staticmethod
    def stop():
        current_app.config['ENABLED'] = False
