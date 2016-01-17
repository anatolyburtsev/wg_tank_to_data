import json

class Gun:

    move_down_arc = 0
    move_up_arc = 0
    name = ""
    fire_rate = 0
    dispersion = 0
    reload_time = 0
    aim_time = 0

    def fill_fields(self, json_response):
        gun_data = json_response["gun"]
        self.move_down_arc = gun_data["move_down_arc"]
        self.move_up_arc = gun_data["move_up_arc"]
        self.name = gun_data["name"]
        self.fire_rate = gun_data["fire_rate"]
        self.dispersion = gun_data["dispersion"]
        self.reload_time = gun_data["reload_time"]
        self.aim_time = gun_data["aim_time"]

    def __str__(self):
        result = """
Орудие:
название - {}
увн вверх - {} гр
увн вниз - {} гр
выстрелов в минуту - {}
перезарядка - {} с
разброс на 100м - {}
время сведения - {} c
    """.format(self.name, self.move_up_arc, self.move_down_arc, self.fire_rate, self.reload_time, self.dispersion,
               self.aim_time)
        return result


if __name__ == "__main__":
    file = "test/localdump.json"
    with open(file) as data_file:
        data = json.load(data_file)

    a = Gun()
    a.fill_fields(data["data"]["305"]["default_profile"])
    print(a)
