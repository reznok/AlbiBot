from commands import *
import sqlite3


class CraftConnector:
    def __init__(self, user, db_file="craftserver.sqlite3"):
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()
        self.user_id = self.get_user_id(user)

        if self.user_id is None:
            raise Exception("Invalid User")

    def __del__(self):
        self.conn.close()

    def _check_item(self, item):
        """
        Ensures that items follow: T{#) ITEM
        :return: bool
        """

        if item[0] != "T":
            return False

        if item[1] not in ["0", "1", "2", "3", "4", "5", "6", "7", "8"]:
            return False

        return True

    def get_user_id(self, user):
        user_id_query = """
        SELECT ID FROM users WHERE DISCORD_NAME = '{}';
        """.format(user)

        self.c.execute(user_id_query)

        try:
            user_id = self.c.fetchone()[0]
        except TypeError:
            print("User {} Not Found".format(user))
            return None
        return user_id

    def shop_get(self):
        shop_items = []
        shop_query = """
        SELECT ITEM from shop WHERE USER = {}
        """.format(self.user_id)

        self.c.execute(shop_query)
        for row in self.c:
            for i in row:
                shop_items.append(i)

        return shop_items

    def shop_location_get(self):
        shop_location_query = """
        SELECT SHOP_LOCATION FROM users WHERE ID = {};
        """.format(self.user_id)

        self.c.execute(shop_location_query)
        return self.c.fetchone()[0]

    def shop_status_get(self):
        shop_status_query = """
        SELECT ONLINE_STATUS FROM users WHERE ID = {};
        """.format(self.user_id)

        self.c.execute(shop_status_query)
        return self.c.fetchone()[0]

    def shop_add(self, item):
        if not self._check_item(item):
            raise Exception("Invalid Item")

        shop_add_query = """
        INSERT INTO shop (USER, ITEM) VALUES ('{}', '{}');
        """.format(self.user_id, item)

        self.c.execute(shop_add_query)
        self.conn.commit()

    def shop_remove(self, item):
        shop_remove_query = """
        DELETE FROM shop WHERE USER = '{}' AND ITEM = '{}';
        """.format(self.user_id, item)

        self.c.execute(shop_remove_query)
        self.conn.commit()

    def shop_location_set(self, location):
        shop_set_location_query = """
        UPDATE users set SHOP_LOCATION = '{}' WHERE ID = '{}';
        """.format(location, self.user_id)
        self.c.execute(shop_set_location_query)
        self.conn.commit()

