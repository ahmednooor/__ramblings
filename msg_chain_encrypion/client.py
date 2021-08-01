import json
import requests
import copy
from encryption_tool import EncryptionTool
from rand_prime import generate_prime_number

from helpers import (
    encrypt,
    decrypt,
    new_actor_state
)

STORE = {
    "clients": {}
}

def dh_key_exchange_with():
    temp_state = new_actor_state()

    temp_state["dh_exchange_nums"]["s"] = generate_prime_number(8)
    temp_state["dh_exchange_nums"]["p"] = generate_prime_number(16)
    temp_state["dh_exchange_nums"]["g"] = generate_prime_number(8)

    temp_state["dh_exchange_nums"]["A"] = \
        temp_state["dh_exchange_nums"]["g"] ** \
        temp_state["dh_exchange_nums"]["s"] % \
        temp_state["dh_exchange_nums"]["p"]
    
    response = requests.post(
        f'http://localhost:5000/dh_key_exchange?' + \
        f'a={str(temp_state["dh_exchange_nums"]["p"])}&' + \
        f'b={str(temp_state["dh_exchange_nums"]["g"])}&' + \
        f'c={str(temp_state["dh_exchange_nums"]["A"])}'
    )
    if response.status_code != 200:
        print("HTTP ERROR CODE: " + str(response.status_code))
        return False
    response = json.loads(response.text)

    temp_state["dh_exchange_nums"]["B"] = int(response["B"])

    temp_state["dh_exchange_nums"]["key"] = \
        temp_state["dh_exchange_nums"]["B"] ** \
        temp_state["dh_exchange_nums"]["s"] % \
        temp_state["dh_exchange_nums"]["p"]
    
    temp_state["secret_key"] = str(temp_state["dh_exchange_nums"]["key"])

    decrypt(temp_state, response["payload"])

    payload = json.loads(temp_state["receiving_msg"])
    temp_state["id"] = payload["id"]
    temp_state["password"] = payload["password"]

    print(response)
    print(temp_state["secret_key"])
    print(temp_state["receiving_msg"])
    print(temp_state["password"])
    print(temp_state["id"])

    new_temp_state = copy.deepcopy(temp_state)

    encrypt(new_temp_state, new_temp_state["password"])

    response = requests.post(
        f'http://localhost:5000/verify_dh_key_exchange?' + \
        f'a={new_temp_state["id"]}&' + \
        f'b={new_temp_state["sending_msg"]}'
    )
    if response.status_code != 200:
        print("HTTP ERROR CODE: " + str(response.status_code))
        return False
    response = json.loads(response.text)

    print(response)
    
    temp_state = copy.deepcopy(new_temp_state)
    
    return True
    

if __name__ == "__main__":
    dh_key_exchange_with()