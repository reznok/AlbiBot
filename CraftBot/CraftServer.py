import sqlite3

VALID_CITIES = ["caerleon", "bridgewatch", "thetford", "lymhurst", "fort sterling", "martlock"]

VALID_TIERS = ["1", "2", "3", "4", "4.1", "4.2", "4.3", "5", "5.1", "5.2", "5.3", "6", "6.1", "6.2", "6.3", "7",
               "7.1", "7.2", "7.3", "8", "8.1", "8.2", "8.3"]

VALID_PREFIXES = ["soldier", "knight", "guardian", "royal", "graveguard", "demon", "assassin", "hunter", "mercenary",
                  "royal", "stalker", "hellion", "mage", "cleric", "scholar", "royal", "druid", "fiend", "harvester",
                  "miner", "skinner", "lumberjack", "quarrier"]

VALID_WARRIOR_WEAPONS = ["broadsword", "spinning blades", "claymore", "clarent blade", "carving sword", "battleaxe", "halberd",
                 "hand of khor", "carrioncaller", "infernal scythe", "mace", "heavy mace", "morning star", "bedrock mace",
                 "incubus mace", "hammer", "great hammer", "polehammer", "tombhammer", "forge hammers", "crossbow",
                 "heavy crossbow", "light crossbow", "weeping repeater", "boltcasters"]

VALID_HUNTER_WEAPONS = ["bow", "warbow", "longbow", "whispering bow", "wailing bow", "spear", "pike", "glaive", "heron spear",
                        "spirithunter", "nature staff", "great nature staff", "wild staff", "druidic staff", "blight staff",
                        "dagger", "dagger pair", "claws", "bloodletter", "black hands", "quarterstaff", "iron-clad staff",
                        "double bladed staff", "black monk stave", "soulscythe"]

VALID_MAGE_WEAPONS = ["fire staff", "great fire staff", "infernal staff", "wildfire staff", "brimstone staff", "holy staff",
                      "great holy staff", "divine staff", "lifetouch staff", "fallen staff", "arcane staff", "great arcane staff",
                      "enigmatic staff", "witchwork staff", "occult staff", "frost staff", "great frost staff",
                      "glacial staff", "hoarfrost staff", "icicle staff", "cursed staff", "great cursed staff",
                      "demonic staff", "lifecurse staff", "cursed skull"]

VALID_ARMOR_SLOTS = ["boots", "chest", "helmet"]

VALID_WEAPONS = VALID_HUNTER_WEAPONS + VALID_MAGE_WEAPONS + VALID_WARRIOR_WEAPONS

class CraftConnector:
    def __init__(self, user, db_file="craftserver.sqlite3"):
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()
        self.user_id = self.get_user_id(user)

        if self.user_id is None:
            raise Exception("Invalid User")

    def __del__(self):
        self.conn.close()

    def _check_city(self, city):
        if city not in VALID_CITIES:
            return False
        return True

    def _check_item(self, item):
        """
        Ensures that items follow: T{#) ITEM
        :return: bool
        """

        print(item)

        # Tier Check
        item_tier = item.split(" ")[0]
        tier = item_tier.split("t")[1]
        if tier not in VALID_TIERS:
            print("Tier # Fail: %s" % tier[1])
            return False

        print("?")

        # Weapon Check
        item_weapon = item.split(" ", 1)[1]
        if item_weapon in VALID_WEAPONS:
            print("Weapon Found: %s" % item_weapon)
            return True
        else:
            print("Not A Weapon: %s" % item_weapon)

        # Prefix Check
        item_prefix = item.split(" ", 1)[1].split(" ")[0]
        if item_prefix not in VALID_PREFIXES:
            print("Invalid Prefix: %s" % item_prefix)
            return False
        print("Prefix Found: %s" % item_prefix)

        # Slot Check
        slot = item.split(" ")[-1]
        if slot not in VALID_ARMOR_SLOTS:
            return False
        print("Armor Found: %s" % slot)

        return True

    def get_user_id(self, user):
        user_id_query = """
        SELECT ID FROM users WHERE DISCORD_NAME = '{}';
        """.format(user)

        user_create_query = """
        INSERT into users (DISCORD_NAME, ONLINE_STATUS, SHOP_LOCATION) VALUES ('{}', '{}', '{}')
        """.format(user, 0, "")

        self.c.execute(user_id_query)

        try:
            user_id = self.c.fetchone()[0]
        except TypeError:
            print("User {} Not Found, Creating User...".format(user))
            self.c.execute(user_create_query)
            self.conn.commit()
            return self.get_user_id(user)

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
        item = item.lower()
        if not self._check_item(item):
            raise Exception("Invalid Item")

        shop_add_query = """
        INSERT INTO shop (USER, ITEM) VALUES ('{}', '{}');
        """.format(self.user_id, item)

        self.c.execute(shop_add_query)
        self.conn.commit()

    def shop_remove(self, item):
        item = item.lower()
        shop_remove_query = """
        DELETE FROM shop WHERE USER = '{}' AND ITEM = '{}';
        """.format(self.user_id, item)

        self.c.execute(shop_remove_query)
        self.conn.commit()

    def shop_location_set(self, location):
        location = location.lower()
        if not self._check_city(location):
            return False

        shop_set_location_query = """
        UPDATE users set SHOP_LOCATION = '{}' WHERE ID = '{}';
        """.format(location, self.user_id)
        self.c.execute(shop_set_location_query)
        self.conn.commit()
        return True

    def shop_set_online(self, status):
        shop_set_online_query = """
        UPDATE users SET ONLINE_STATUS = '{}' WHERE ID = '{}'
        """.format(status, self.user_id)

        self.c.execute(shop_set_online_query)
        self.conn.commit()
        return

    def ticket_create(self, item):
        ticket_create_query = """
        INSERT INTO tickets VALUES (REQUESTOR, ITEM, STATUS) VALUES ('{}', '{}', '{}')
        """.format(self.user_id, item, 0)

        if not self._check_item(item):
            raise Exception("Invalid Item")

        self.c.execute(ticket_create_query)
        self.conn.commit()
        return self.c.lastrowid

    def crafters_get(self, location, item):
        """
        Return a list of Discord users that can craft given item
        :param item: string
        :return: []
        """
        can_craft = []

        can_craft_query = """
        SELECT DISCORD_NAME FROM users INNER JOIN shop on shop.USER = users.ID and shop.ITEM = '{}' and users.ONLINE_STATUS = 1 and users.SHOP_LOCATION = '{}';
        """.format(item, location)

        print(can_craft_query)

        self.c.execute(can_craft_query)
        for row in self.c:
            for i in row:
                can_craft.append(i)

        return can_craft


