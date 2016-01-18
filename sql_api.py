import sqlite3
import json
import wg_api


class TanksDB:
    db_name = ""
    conn_db = None
    curs_db = None

    def __init__(self, db_name="tank_db"):
        assert len(db_name.split(".")) < 2
        self.db_name = db_name.split(".")[0]

    def init_connection(self):
        self.conn_db = sqlite3.connect(self.db_name + ".sqlite3")
        self.curs_db = self.conn_db.cursor()

    def init_db(self):
        if not self.conn_db or not self.curs_db:
            self.init_connection()

        cmd = "create table if not exists " + self.db_name + " (tank_id int(6), name char(40), level int(2), nation char(10), " \
                                                             "is_premium bool, type char(5));"
        self.curs_db.execute(cmd)

    def __insert_to_db(self, tank_data_tuple):
        assert self.conn_db
        assert self.curs_db
        assert type(tank_data_tuple) == tuple
        cmd = "insert into " + self.db_name + " values (?,?,?,?,?,?);"
        self.curs_db.execute(cmd, tank_data_tuple)

    def fill_db(self, json_dump):
        self.clean_db()
        for tank_id, tank_data in json_dump["data"].items():
            tuple_to_insert = (int(tank_id), tank_data["name"], int(tank_data["tier"]),
                               tank_data["nation"], tank_data["is_premium"], tank_data["type"])
            self.__insert_to_db(tuple_to_insert)
        self.conn_db.commit()

    def refill_db_from_wg_api(self):
        json_dump = wg_api.get_raw_vehicle()
        self.fill_db(json_dump)

    def clean_db(self):
        try:
            self.curs_db.execute("delete from " + self.db_name)
        except sqlite3.OperationalError:
            pass

    def drop_db(self):
        try:
            self.curs_db.execute("drop table " + self.db_name)
        except sqlite3.OperationalError:
            pass

    def __select(self, cmd):
        if not self.conn_db or not self.curs_db:
            self.init_connection()

        self.curs_db.execute(cmd)
        result = self.curs_db.fetchall()
        return result

    def __nation(self, nation):
        assert type(nation) == str
        cmd = "select tank_id, name from " + self.db_name + " where nation == '" + nation + "' order by level;"
        response = self.__select(cmd)
        result = []
        for tank_name_id in response:
            t = wg_api.TankNameId(tank_name_id[1], tank_name_id[0])
            result.append(t)
        return result

    def all(self):
        cmd = "select tank_id from " + self.db_name + " order by level;"
        return self.__select(cmd)

    def ussr(self):
        return self.__nation("ussr")

    def usa(self):
        return self.__nation("usa")

    def uk(self):
        return self.__nation("uk")

    def china(self):
        return self.__nation("china")

    def japan(self):
        return self.__nation("japan")

    def germany(self):
        return self.__nation("germany")

if __name__ == "__main__":
    # file = "test/vehicles.json"
    # with open(file) as data_file:
    #     data = json.load(data_file)
    # data = wg_api.get_raw_vehicle()
    t = TanksDB()
    t.init_db()
    t.refill_db_from_wg_api()
    # t._TanksDB__nation("ussr")
    # a = t.ussr()
    # b = t.all()
    # print(a[0])
    # print(b)

