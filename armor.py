import json
from pprint import pprint

class TurretArmor:
    is_exist = False
    front = 0
    sides = 0
    rear = 0

    def __str__(self):
        result = """
Башня:
лоб - {} мм
борта - {} мм
корма - {} мм
        """.format(self.front, self.sides, self.rear)
        return result


class HullArmor:
    front = 0
    sides = 0
    rear = 0

    def __str__(self):
        result = """
Корпус:
лоб - {} мм
борта - {} мм
корма - {} мм
        """.format(self.front, self.sides, self.rear)
        return result


class Armor:
    turret = TurretArmor()
    hull = HullArmor()

    def fill_fields(self, json_response):
        armor_data = json_response["armor"]
        self.hull.front = armor_data["hull"]["front"]
        self.hull.sides = armor_data["hull"]["sides"]
        self.hull.rear = armor_data["hull"]["rear"]

        if "turret" in armor_data:
            self.turret.is_exist = True
            self.turret.front = armor_data["turret"]["front"]
            self.turret.sides = armor_data["turret"]["sides"]
            self.turret.rear = armor_data["turret"]["rear"]

    def __str__(self):
        result = "Бронирование:" + str(self.hull)
        if self.turret.is_exist:
            result = result + str(self.turret)
        return result

if __name__ == "__main__":

    file = "test/localdump.json"
    with open(file) as data_file:
        data = json.load(data_file)

    a = Armor()
    a.fill_fields(data["data"]["305"]["default_profile"])
    print(a)
    # pprint(data)

