import requests
import config
import logging


class TankNameId:
    name = ""
    tank_id = ""

    def __init__(self, name, tank_id):
        self.name = name
        self.tank_id = tank_id


def get_tanks_info(tank_id):
    assert str(tank_id).isdigit()
    tank_id = str(tank_id)
    req = "https://api.wotblitz.ru/wotb/encyclopedia/vehicles/?application_id={}&tank_id={}".format(
        config.wargaming_id, tank_id
    )

    response = requests.get(req).json()
    try:
        result = response["data"][tank_id]
    except KeyError:
        logging.error("Coudn't json response for tank_id:" + str(tank_id))
        raise

    if not result:
        return False

    return result


def get_tanks_and_ids():

    req = "https://api.wotblitz.ru/wotb/encyclopedia/vehicles/?application_id={}&fields=name".format(
        config.wargaming_id
    )

    response = requests.get(req).json()
    try:
        result_dict = response["data"]
    except KeyError:
        logging.error("Couldn't json response for all tanks and ids")
        raise

    result = []
    for i in result_dict.keys():
        t = TankNameId(result_dict[i]["name"], i)
        result.append(t)

    return result


def get_api_version():
    req = "https://api.wotblitz.ru/wotb/encyclopedia/info/?application_id={}".format(config.wargaming_id)
    response = requests.get(req).json()
    try:
        version = response["data"]["game_version"]
    except KeyError:
        logging.error("Couldn't json response for api version")
        raise

    return version


if __name__ == "__main__":
    print(get_tanks_info(65329))
    print(get_api_version())
    print(get_tanks_and_ids())

