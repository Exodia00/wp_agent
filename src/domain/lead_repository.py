from domain.lead import Lead
from infrastructure.db import MySQLDatabase
from infrastructure.query_manager import LeadQueries


class LeadRepository:

    db : MySQLDatabase

    def __init__(self, db: MySQLDatabase):
        self.db = db

    def get_by_num(self, num: str, latest_only=False):
        if latest_only:
            row = self.db.execute(LeadQueries.GET_BY_NUM_MOST_RELEVANT, (num,), list_all=False)
            return Lead(**row) if row else None
        rows = self.db.execute(LeadQueries.GET_BY_NUM, (num,))
        return [Lead(**row) for row in rows] if rows else None

    def add(self, lead: Lead):
        query, params, is_valid = LeadQueries.try_get_insert_statement(lead)
        self.db.execute(query, params, False)


    def update(self, lead: Lead):
        query, params, is_valid = LeadQueries.try_get_update_statement(lead)

        if is_valid:
            self.db.execute(query, params, False)
