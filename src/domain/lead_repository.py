from domain.lead import Lead
from infrastructure.db import MySQLDatabase
from infrastructure.query_manager import LeadQueries


# todo: LeadRepository should be in infrastructure, domain should contain the abstraction / interface -- Move it
# todo: To be moved to infrastructure/repositories/lead_repository.py

class LeadRepository:

    db : MySQLDatabase

    def __init__(self, db: MySQLDatabase):
        self.db = db

    def try_get_latest(self, number: str, phone_id: str):  # todo manage completed clients ?
        lead = self.get_by_num(number,
                                             latest_only=True)  # todo: An error can be thrown here, to manage earlier. move any potential lead if they exist to unexpected
        if lead is None:
            return Lead(num=number, phone_id=phone_id)
        return lead

    def get_by_num(self, num: str, latest_only=False):
        if latest_only:
            row = self.db.execute(LeadQueries.GET_BY_NUM_MOST_RELEVANT, (num,), list_all=False)
            return Lead(**row) if row else None
        rows = self.db.execute(LeadQueries.GET_BY_NUM, (num,))
        return [Lead(**row) for row in rows] if rows else None

    def add_or_update(self, lead: Lead):
        if lead.id is None:
            self.add(lead)
        else:
            self.update(lead)

    def add(self, lead: Lead):
        query, params, is_valid = LeadQueries.try_get_insert_statement(lead)
        self.db.execute(query, params, False)


    def update(self, lead: Lead):
        query, params, is_valid = LeadQueries.try_get_update_statement(lead)

        if is_valid:
            self.db.execute(query, params, False)
