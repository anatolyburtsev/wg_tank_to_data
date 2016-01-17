import json

shell_type = {"ARMOR_PIERCING": "ББ", "HOLLOW_CHARGE": "КС", "HIGH_EXPLOSIVE": "ОФ", "ARMOR_PIERCING_CR": "БП"}


class Shell:

    penetration = 0
    type = ""
    type_rus = ""
    damage = 0

    def fill_fields(self, json_response):
        self.penetration = json_response["penetration"]
        self.type = json_response["type"]
        self.type_rus = shell_type[self.type]
        self.damage = json_response["damage"]

    def __str__(self):
        result = """
тип: {}
пробитие: {}
урон: {}""".format(self.type_rus, self.penetration, self.damage)

        return result


class Shells:

    shells = []

    def fill_fields(self, json_response):
        shells_data = json_response["shells"]
        for shell_data in shells_data:
            shell = Shell()
            shell.fill_fields(shell_data)
            self.shells.append(shell)

    def __str__(self):
        shells = ""
        for i in self.shells:
            shells = shells + "\n" + str(i)
        result = "Снаряды:" + shells
        return result


if __name__ == "__main__":
    file = "test/localdump.json"
    with open(file) as data_file:
        data = json.load(data_file)

    a = Shells()
    a.fill_fields(data["data"]["305"]["default_profile"])
    print(a)
