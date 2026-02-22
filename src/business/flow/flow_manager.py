from datetime import datetime

from business import message_manager
from business.business_manager import get_origin, MessageOrigin, get_service_from_msg, \
    get_bv_service_from_msg, is_bv_service, is_new_lead
from business.flow.flow import IFlowManager
from business.flow.flow_resolver import resolve

from business.whatsapp_sender import send_whatsapp_message
from domain.enums import State, Service
from domain.lead import Lead
from domain.lead_repository import LeadRepository
from infrastructure.db import MySQLDatabase

# todo: Create new domain.Message, should be agnostic of whether it should be sent in whatsapp or sms or other.

class FlowManager(IFlowManager):

    lead: Lead
    message: str

    lead_repo : LeadRepository # todo: This should later become an interface, implementation to be defined in infrastructure level

    def __init__(self, num: str, phone_id: str, text: str, db: MySQLDatabase):
        self.message = text

        self.lead_repo = LeadRepository(db)

        # todo: this shouldn't be in init, move to process ?
        self.lead = self.lead_repo.try_get_latest(num, phone_id)

    # todo: This should be made async
    def process(self):

        print(f"Starting process for {self.lead}")

        if self.lead.state is None : self.lead.start()

        fn = resolve(self.lead.state, self)

        fn()

        self.lead_repo.add_or_update(self.lead)



    # ---------- Flow :

    # todo: Have all the flow methods return the message to be sent if any, have the message sending centrelized in the process method

    def start(self):
        origin, service = get_origin(self.message)
        self.lead.start()
        self.lead.service = service
        self.lead.is_organic = origin == MessageOrigin.ORGANIC # todo: Move this to domain.Enums
        self.lead.state = State.GET_LANG

        # todo: The send_whatsapp message function will need some refactoring to adhere to a clean architecture
        send_whatsapp_message(self.lead.phone_id, "buttons",
                              message_manager.welcome_get_lang_values(self.lead.num)
                              )

    def get_lang(self):
        if self.message == "lang_ar":
            self.lead.lang = "ar"
        else:
            self.lead.lang = "fr"

        # if service is empty, ask for service.
        if self.lead.service is None or self.lead.service == "":
            self.lead.state = State.GET_SERVICE

            send_whatsapp_message(self.lead.phone_id, "buttons",
                                  message_manager.service_selection_get_values(self.lead.num, self.lead.lang)
                                  )
            return

        # todo: this failed, why >
        if self.lead.service == Service.BV: # todo: Move to Enums
            self.lead.state = State.GET_SERVICE_BV

            send_whatsapp_message(self.lead.phone_id, "buttons",
                                  message_manager.bache_vinyl_get_values(self.lead.num, self.lead.lang))
            return

        self.lead.state = State.GET_CITY

        send_whatsapp_message(self.lead.phone_id, "buttons",
                              message_manager.are_you_in_casa_get_values(self.lead.num, self.lead.lang))
        return

    def get_service(self):
        service = get_service_from_msg(self.message) # TODO: REFACTOR
        self.lead.service = service

        if service == Service.BV:
            self.lead.state = State.GET_SERVICE_BV
            send_whatsapp_message(self.lead.phone_id, "buttons",
                                  message_manager.bache_vinyl_get_values(self.lead.num, self.lead.lang))

            return

        if service is None:
            self.lead.state = State.UNEXPECTED  # todo: process UNEXPECTED
            # todo: Call lead.complete(expected=false)
            self.lead.is_complete = True  # todo: This should be moved to manage unexpected, and have it set ended_at instead.
            self.lead.ended_at = datetime.now()

            send_whatsapp_message(self.lead.phone_id, "text",
                                  message_manager.thank_you_get_values(self.lead.num, self.lead.lang))

            return

        self.lead.state = State.GET_CITY
        send_whatsapp_message(self.lead.phone_id, "buttons",
                              message_manager.are_you_in_casa_get_values(self.lead.num, self.lead.lang))

        return

    def get_service_bv(self):
        service = get_bv_service_from_msg(self.message) # todo: refactor

        if service is None:
            # todo: Call lead.complete(expected=false)
            self.lead.state = State.UNEXPECTED  # todo: process UNEXPECTED
            self.lead.is_complete = True  # todo: remove
            self.lead.ended_at = datetime.now()

            send_whatsapp_message(self.lead.phone_id, "text",
                                  message_manager.thank_you_get_values(self.lead.num, self.lead.lang))

            return

        self.lead.state = State.GET_CITY
        self.lead.service = service
        send_whatsapp_message(self.lead.phone_id, "buttons",
                              message_manager.are_you_in_casa_get_values(self.lead.num, self.lead.lang))

        return

    def get_city(self):
        self.lead.in_casa = (self.message == "loc_yes") # todo: message ids to enum ? avoid magic consts

        # if the main service was bache/vinyl ask for dimensions else ask for activity

        if is_bv_service(self.lead.service):
            self.lead.state = State.GET_DIM

            send_whatsapp_message(self.lead.phone_id, "text",
                                  message_manager.ask_dimensions_get_values(self.lead.num, self.lead.lang))

            return

        self.lead.state = State.GET_ACTIVITY

        send_whatsapp_message(self.lead.phone_id, "list",
                              message_manager.activity_selection_get_values(self.lead.num, self.lead.lang))

        return

    def get_dim(self):

        self.lead.complete(expected=True)
        self.lead.state = State.COMPLETE
        self.lead.ended_at = datetime.now()


        send_whatsapp_message(self.lead.phone_id, "text",
                              message_manager.final_thank_you_with_assets_get_values(self.lead.num, self.lead.lang))

        return

    def get_activity(self):
        self.lead.activity = self.message
        # todo: call lead.complete()
        self.lead.state = State.COMPLETE
        self.lead.ended_at = datetime.now()

        send_whatsapp_message(self.lead.phone_id, "text",
                              message_manager.final_thank_you_with_assets_get_values(self.lead.num, self.lead.lang))

        return

    def complete(self):
        # check if the conversation has already ended ?
        if is_new_lead(self.lead):
            new_lead = Lead().new_from(self.lead)
            new_lead.start()
            if self.lead.lang is not None:
                new_lead.state = State.GET_SERVICE
                self.lead_repo.add_or_update(new_lead)

                send_whatsapp_message(self.lead.phone_id, "list",
                                      message_manager.welcome_service_selection_get_values(self.lead.num, self.lead.lang)
                                      )

                return
            self.lead.state = State.GET_LANG

            send_whatsapp_message(self.lead.phone_id, "buttons",
                                  message_manager.welcome_get_lang_values(self.lead.num)
                                  )

            return
        return "No message"  # todo: implement maybe an error to be caught !

    def unexpected(self):
        # todo: if there is no extra conditioning, have it mapped to complete in flow resolver
        self.complete()
