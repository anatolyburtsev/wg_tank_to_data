import json

class Turret:
    view_range = 0
    traverse_speed = 0

    def fill_fields(self, json_response):
        turret_data = json_response["turret"]
        self.view_range = turret_data["view_range"]
        self.traverse_speed = turret_data["traverse_speed"]

    def __str__(self):
        result = """
Башня:
Обзор - {} м
Скорость вращения - {} гр/с
    """.format(self.view_range, self.traverse_speed)
        return result

if __name__ == "__main__":
    file = "test/localdump.json"
    with open(file) as data_file:
        data = json.load(data_file)

    a = Turret()
    a.fill_fields(data["data"]["305"]["default_profile"])
    print(a)