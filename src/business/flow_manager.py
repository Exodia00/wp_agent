from datetime import datetime
from enum import Enum

from business import message_manager
# todo: will need logs

from business.business_manager import get_origin, MessageOrigin, Service, get_service_from_msg, is_new_lead, get_lead, save, \
    get_bv_service_from_msg, is_bv_service
from business.whatsapp_sender import send_whatsapp_message
from domain.lead import Lead

class State(Enum):
    START = "START"
    GET_LANG = "LANG"
    GET_SERVICE = "SERVICE"
    GET_SERVICE_BV = "SERVICE_BV"
    GET_CITY = "CITY"
    UNEXPECTED = "UNEXPECTED"
    GET_DIM = "DIM"
    GET_DETAILS = "DETAILS"
    GET_ACTIVITY = "ACTIVITY"
    COMPLETE = "COMPLETE"

# todo: move elsewhere

def handle_flow(client_number: str, phone_id: str, text: str) -> str:
    lead = get_lead(client_number, phone_id=phone_id)  # todo: Needs to be implemented
    response = process(lead, text)
    save(lead)                      # todo: Needs to be implemented
    return response

# todo: Change responses to reply buttons or lists !

def process(lead: Lead, text: str) -> str:
    state = lead.state

    if state is None or state == State.START.value:
        return process_start(lead, text)
    if state == State.GET_LANG.value:
        return process_get_lang(lead, text)
    if state == State.GET_SERVICE.value:
        return process_get_service(lead, text)
    if state == State.GET_SERVICE_BV.value:
        return process_get_service_bv(lead, text)
    if state == State.GET_CITY.value:
        return process_get_city(lead, text)
    if state == State.GET_DIM.value:
        return process_get_dim(lead, text)
    if state == State.GET_ACTIVITY.value:
        return process_get_activity(lead, text)
    if state == State.COMPLETE.value:
        return process_complete(lead, text)
    if state == State.COMPLETE or state == State.UNEXPECTED:
        return process_get_details_complete(lead, text)

    # For state unexpected : don't display any message


    # todo: will need to process COMPLETE and COMPLETE WITH DETAILS, to wait 3 before considering the user as a new lead

    # todo: else : State unexpected, message : end_conversation
    return "" #todo: complete me

def process_start(lead: Lead, text: str) -> str :
    origin, service = get_origin(text)
    lead.started_at = datetime.now()
    lead.service    = service
    lead.is_organic = origin == MessageOrigin.ORGANIC
    lead.state = State.GET_LANG.value

    send_whatsapp_message(lead.phone_id, "buttons",
                          message_manager.welcome_get_lang_values(lead.num)
                          )
    return "LANG_SELECTION_SENT"

def process_get_lang(lead: Lead, text: str) -> str:
    if text == "lang_ar": lead.lang = "ar"
    else: lead.lang = "fr"

    # if service is empty, ask for service.
    if lead.service is None or lead.service == "":
        lead.state = State.GET_SERVICE.value

        send_whatsapp_message(lead.phone_id, "buttons",
                              message_manager.service_selection_get_values(lead.num, lead.lang)
                              )

        return "ASKED FOR SERVICE"

    if lead.service == Service.BV.value :
        lead.state = State.GET_SERVICE_BV.value

        send_whatsapp_message(lead.phone_id, "buttons",
                              message_manager.bache_vinyl_get_values(lead.num, lead.lang))

        return "ASKED FOR BV Service"

    lead.state = State.GET_CITY.value

    send_whatsapp_message(lead.phone_id, "buttons",
                          message_manager.are_you_in_casa_get_values(lead.num, lead.lang))

    return "ASKED CASA"

def process_get_service(lead: Lead, text: str) -> str:
    # todo : what if get service returns None : TODO: At each step, add a fail-over to "you will be contacted soon"
    service = get_service_from_msg(text)
    lead.service = service

    if service == Service.BV.value:
        lead.state = State.GET_SERVICE_BV.value
        send_whatsapp_message(lead.phone_id, "buttons",
                              message_manager.bache_vinyl_get_values(lead.num, lead.lang))

        return "ASKED FOR BV Service"


    if service is None:
        lead.state = State.UNEXPECTED.value   # todo: process UNEXPECTED
        lead.is_complete = True # todo: This should be moved to manage unexpected, and have it set ended_at instead.
        lead.ended_at = datetime.now()

        send_whatsapp_message(lead.phone_id, "text",
                              message_manager.thank_you_get_values(lead.num, lead.lang))

        return "ENDED CONVERSATION"


    lead.state = State.GET_CITY.value
    send_whatsapp_message(lead.phone_id, "buttons",
                          message_manager.are_you_in_casa_get_values(lead.num, lead.lang))

    return "ASKED CASA"

def process_get_service_bv(lead: Lead, text: str) -> str:
    service = get_bv_service_from_msg(text)

    if service is None:
        lead.state = State.UNEXPECTED.value  # todo: process UNEXPECTED
        lead.is_complete = True         # todo: remove
        lead.ended_at = datetime.now()

        send_whatsapp_message(lead.phone_id, "text",
                              message_manager.thank_you_get_values(lead.num, lead.lang))

        return "ENDED CONVERSATION"

    lead.state = State.GET_CITY.value
    lead.service = service
    send_whatsapp_message(lead.phone_id, "buttons",
                          message_manager.are_you_in_casa_get_values(lead.num, lead.lang))

    return "ASKED CASA"

def process_get_city(lead: Lead, text: str) -> str:
    lead.in_casa = (text == "loc_yes")

    # if the main service was bache/vinyl ask for dimensions else ask for activity

    if is_bv_service(lead.service):
        lead.state = State.GET_DIM.value

        send_whatsapp_message(lead.phone_id, "text",
                              message_manager.ask_dimensions_get_values(lead.num, lead.lang))

        return "ASKED DIMENSIONS"


    lead.state = State.GET_ACTIVITY.value

    send_whatsapp_message(lead.phone_id, "buttons",
                          message_manager.activity_selection_get_values(lead.num, lead.lang))

    return "ASKED ACTIVITY"


def process_get_dim(lead: Lead, text: str) -> str:

    lead.state = State.COMPLETE.value
    lead.ended_at = datetime.now()

    send_whatsapp_message(lead.phone_id, "text",
                          message_manager.final_thank_you_with_assets_get_values(lead.num, lead.lang))

    return "END WITH DETAILS"


def process_get_activity(lead: Lead, text: str) -> str:
    lead.activity = text
    lead.state = State.COMPLETE.value
    lead.ended_at = datetime.now()

    send_whatsapp_message(lead.phone_id, "text",
                          message_manager.final_thank_you_with_assets_get_values(lead.num, lead.lang))

    return "END WITH DETAILS"

def process_get_details_complete(lead: Lead, text: str) -> str:
    # check if the conversation has already ended ?
    if is_new_lead(lead) :
        new_lead = generate_lead_from(lead)
        new_lead.state = State.START.value
        new_lead.num = lead.num
        new_lead.started_at = datetime.now()
        if lead.lang is not None :
            new_lead.state = State.GET_SERVICE.value
            save(new_lead)
            return message_maager.welcome_get_service(lead.lang)   # TODO: use the send_whatsapp_message template
        lead.state = State.GET_LANG.value

        send_whatsapp_message(lead.phone_id, "buttons",
                              message_manager.welcome_get_lang_values(lead.num)
                              )

        return "LANG_SELECTION_SENT"
    return "No message" # todo: implement maybe an error to be caught !

# todo : complete me
def process_complete(lead: Lead, text: str) -> str:
    if is_new_lead(lead):
        new_lead = generate_lead_from(lead)

def generate_lead_from(lead: Lead) -> Lead:
    result = Lead()
    result.num = lead.num
    result.started_at = datetime.now()
    result.lang = lead.lang

    return result
