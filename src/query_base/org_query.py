from src.constants import Constants

constant = Constants()


class Contact:

    @staticmethod
    def complain(reason_id, comment, user_id):
        query = f"INSERT INTO complains (reason_id, comment, user_id, active) VALUES(" \
                f"{reason_id}, '{comment}', {user_id}, 1); "
        return constant.insert_query(query)
