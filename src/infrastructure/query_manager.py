from dataclasses import fields, is_dataclass

from domain.lead import Lead

# todo : Move elsewhere in infrastructure
class AutoMapper:

    @staticmethod
    def iterate_dataclass(obj, include_id=True, include_null=True):
        if not is_dataclass(obj):
            raise TypeError("Not a dataclass")

        for f in fields(obj):
            # Skip id if user wants to exclude it
            if f.name == "id" and not include_id:
                continue

            value = getattr(obj, f.name)

            # Include non-null values
            if value is not None:
                yield f.name, value
            else:
                # yield null values only if asked
                if include_null:
                    yield f.name, value


class LeadQueries:
    GET_BY_NUM = "SELECT * FROM leads WHERE num=%s"

    GET_BY_NUM_MOST_RELEVANT = "SELECT * FROM leads WHERE num=%s ORDER BY started_at DESC LIMIT 1; "

    @staticmethod
    def try_get_update_statement(lead: Lead) -> tuple[str, tuple, bool]:
        query = "UPDATE leads SET "
        params = []
        is_valid = False

        for name, value in AutoMapper.iterate_dataclass(lead, include_id=False, include_null=False):
            is_valid = True
            query += f"{name} = %s, "
            params.append(value)

        if is_valid:
            # Remove last ", "
            query = query.rstrip(", ")
            query += " WHERE id = %s"
            params.append(lead.id)

        return query, tuple(params), is_valid


    @staticmethod
    def try_get_insert_statement(lead: Lead) -> tuple[str, tuple, bool]:
        columns = []
        placeholders = []
        params = []
        is_valid = False

        # iterate without id, without nulls
        for name, value in AutoMapper.iterate_dataclass(lead, include_id=False, include_null=False):
            is_valid = True
            columns.append(name)
            placeholders.append("%s")
            params.append(value)

        if not is_valid:
            return "", (), False

        columns_part = ", ".join(columns)
        placeholders_part = ", ".join(placeholders)

        query = f"INSERT INTO leads ({columns_part}) VALUES ({placeholders_part})"
        return query, tuple(params), True

