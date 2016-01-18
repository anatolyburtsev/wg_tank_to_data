import wg_api
import gun
import turret
import suspension
import armor
import shells

type_dict = {"lightTank": "Легкий танк", "mediumTank": "Средний танк", "heavyTank": "Тяжелый танк",
                "AT-SPG": "ПТ-САУ"}
nation_dict = {"ussr": "СССР", "usa": "США", "germany": "Германия", "uk": "Англия", "japan": "Япония",
               "china": "Китай"}


class Tank:

    tank_id = ""
    name = ""
    is_premium = False
    price = 0
    level = 0
    nation = ""
    nation_rus = ""
    raw_data = ""
    default_data = ""
    images = ""
    hp = 0
    type = ""
    type_rus = ""
    speed_forward = 0
    speed_backward = 0
    horse_power = 0
    weight = 0
    density_power = 0
    tier = 0
    description = ""

    gun = gun.Gun()
    turret = turret.Turret()
    suspension = suspension.Suspension()
    armor = armor.Armor()
    shells = shells.Shells()



    def __init__(self, tank_id):
        assert str(tank_id).isdigit()
        self.tank_id = str(tank_id)
        self.shells = shells.Shells()
        self.armor = armor.Armor()

    def fetch_info(self):
        self.raw_data = wg_api.get_tanks_info(self.tank_id)
        self.default_data = self.raw_data["default_profile"]

    def parse_info(self):
        self.gun.fill_fields(self.default_data)
        self.turret.fill_fields(self.default_data)
        self.suspension.fill_fields(self.default_data)
        self.armor.fill_fields(self.default_data)
        self.shells.fill_fields(self.default_data)
        self.name = self.raw_data["name"]
        self.is_premium = self.raw_data["is_premium"]
        self.nation = self.raw_data["nation"]
        self.nation_rus = nation_dict[self.nation]
        self.images = self.raw_data["images"]["normal"]
        self.tier = self.raw_data["tier"]
        self.description = self.raw_data["description"]
        self.type = self.raw_data["type"]
        self.type_rus = type_dict[self.type]

        self.speed_backward = self.default_data["speed_backward"]
        self.speed_forward = self.default_data["speed_forward"]
        self.horse_power = self.default_data["engine"]["power"]
        self.weight = self.default_data["weight"]
        self.density_power = round(float(1000 * self.horse_power) / int(self.weight))
        self.hp = self.default_data["hp"]

    def __str__(self):
        main_info = """
Танк: {}
ID - {}
Изображение - {}
Уровень - {}
Нация - {}
Тип - {}
Прочность - {} HP
Вес - {} кг
Описание: {}

        """.format(self.name, self.tank_id, self.images,
                   self.tier, self.nation_rus, self.type_rus, self.hp, self.weight, self.description)

        speed_info = """
Удельная мощность - {} лс/т
Скорость вперед - {} км/ч
Скорость назад - {} км/ч
        """.format(self.density_power, self.speed_forward, self.speed_backward)

        result = main_info + "\n" + str(self.armor) + "\n" + str(self.gun) + "\n" + \
                 str(self.shells) + "\n" + str(self.turret) + \
                 str(self.suspension) + speed_info
        return result


if __name__ == "__main__":
    t1 = Tank(65329)
    t1.fetch_info()
    t1.parse_info()
    print(t1)

    # t2 = Tank(305)
    # t2.fetch_info()
    # t2.parse_info()
    # print(t2)

    # print(t.gun.aim_time)

