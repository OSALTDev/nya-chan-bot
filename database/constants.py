class Constants:
    class Templates:
        SELECT = "SELECT {distinct}`{item}` FROM `{table}`"
        INSERT = "INSERT INTO `{table}` ({items}) VALUES ({values})"
        UPDATE = "UPDATE `{table}` SET {items}"
        DELETE = "DELETE FROM `{table}`"
        WHERE = "WHERE {values}"

    token_to_order = {
        ">": "ASC",
        "<": "DESC"
    }


class DBFunction:
    def __init__(self, val):
        self.val = val
