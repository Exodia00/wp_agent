from business import message_manager
from business.application_manager import ApplicationManager
from business.whatsapp_sender import send_whatsapp_message


class AdminManager:

    START_INSTRUCTION = "/start"
    STOP_INSTRUCTION = "/stop"


    num: str
    id: str

    application_manager: ApplicationManager

    def __init__(self, number: str, phone_id: str):
        self.num = number
        self.id = phone_id

        self.application_manager = ApplicationManager()


    def process(self, message: str):
        if message == self.START_INSTRUCTION:
            self.application_manager.start()
            send_whatsapp_message(self.id, "text",
                                  message_manager.bot_started_get_values(self.num)
                                  )
            return

        if message == self.STOP_INSTRUCTION:
            self.application_manager.stop()
            send_whatsapp_message(self.id, "text",
                                  message_manager.bot_stopped_get_values(self.num)
                                  )
            return

        send_whatsapp_message(self.id, "text",
                              message_manager.invalid_admin_command_get_values(self.num)
                              )
        return