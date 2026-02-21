from datetime import datetime, timedelta
from enum import Enum

from domain.lead import Lead
from domain.lead_repository import LeadRepository
from infrastructure.db import MySQLDatabase


class MessageOrigin(Enum):
    ORGANIC = 1
    AD = 2

class Service(Enum):
    BV = "srv_bache_vinyl"
    BEACH_FLAG = "srv_beachflag"
    ROLLUP = "srv_rollup"
    X_BANNER = "srv_xbanner"


class BvService(Enum):
    BV_BACHE = "BACHE"
    BV_VINYL = "VINYL"
    BV_STICKER = "STICKER"

service_messages = {
    Service.BV : "opt_bache",
    Service.ROLLUP : "opt_vinyl",
    Service.BEACH_FLAG : "opt_sticker"
}

def get_origin(text: str) -> tuple[MessageOrigin, Service | None]:
    """
    Checks if the origin of the message is organic, or ad, based on the message sent checked against the preconfigured values
    :param text:
    :return:
    """
    # todo: test ad origin, there will be a bug because we are returning the service enum and not the str value
    for service, message in service_messages.items():
        if message in text: return MessageOrigin.AD, service
    return MessageOrigin.ORGANIC, None

def get_service_from_msg(text: str) -> str | None:
    # todo: Will have to be changed after introducing whatsapp select buttons
    for service in Service:
        if service.value == text: return service.value
    return None

def get_bv_service_from_msg(text: str) -> str | None:
    for service in BvService:
        if service.value == text: return service.value
    return None

def is_bv_service(lead_service: str) -> bool:
    for service in BvService:
        if service.value == lead_service : return True
    return False


def is_new_lead(lead: Lead) -> bool:
    """
    Checks if a lead in the state Complete should be considered new and have a new conversation started.
    """

    # If the lead has no ended_at, it cannot be considered new
    compared_to = lead.ended_at

    if lead.ended_at is None:
        compared_to = lead.started_at

    grace_period_h = 72  # TODO: implement configuration pattern

    # Compare timedelta against timedelta
    return (datetime.now() - compared_to) > timedelta(hours=grace_period_h)     # todo: Check if this works well


def get_lead(number: str, phone_id: str):  # todo manage completed clients ?
    lead = LeadRepository(MySQLDatabase()).get_by_num(number, latest_only=True)   # todo: An error can be thrown here, to manage earlier. move any potential lead if they exist to unexpected
    if lead is None :
        return Lead(num=number, phone_id=phone_id)
    return lead

def save(lead: Lead):
    #todo: Call repository add or update
    repo = LeadRepository(MySQLDatabase())
    if lead.id is None:
        repo.add(lead)
    else:
        repo.update(lead)
