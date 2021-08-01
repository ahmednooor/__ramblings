import hashlib
import base64
import copy
from encryption_tool import EncryptionTool

actor_state = {
    "dh_exchange_nums": {
        "s": None,
        "p": None,
        "g": None,
        "A": None,
        "B": None,
        "key": None
    },
    "secret_key": None,
    "password": None,
    "receiving_msg": None,
    "sending_msg": None,
    "sent_counter": 0,
    "received_counter": 0,
    "id": None,
    "hashes": {
        "receiving_msg_hash": None,
        "sending_msg_hash": None
    }
}

def new_actor_state():
    temp_state = copy.deepcopy(actor_state)
    temp_state["dh_exchange_nums"]["s"] = 1
    temp_state["dh_exchange_nums"]["p"] = 1
    temp_state["dh_exchange_nums"]["g"] = 1
    temp_state["dh_exchange_nums"]["A"] = 1
    temp_state["dh_exchange_nums"]["B"] = 1
    temp_state["dh_exchange_nums"]["key"] = 1
    temp_state["secret_key"] = ""
    temp_state["password"] = ""
    temp_state["receiving_msg"] = ""
    temp_state["sending_msg"] = ""
    temp_state["sent_counter"] = 0
    temp_state["received_counter"] = 0
    temp_state["id"] = ""
    temp_state["hashes"]["receiving_msg_hash"] = ""
    temp_state["hashes"]["sending_msg_hash"] = ""
    return temp_state

def encode_sending_msg_to_base64(actor_state):
    actor_state["sending_msg"] = \
        str(base64.urlsafe_b64encode(actor_state["sending_msg"]), "utf-8")

def decode_receiving_msg_from_base64(actor_state):
    actor_state["receiving_msg"] = \
        base64.urlsafe_b64decode(bytes(actor_state["receiving_msg"], "utf-8"))

def take_hash_of_sending_msg(actor_state):
    hasher = hashlib.new("SHA256")
    hasher.update(
        bytes(
            actor_state["sending_msg"] + actor_state["hashes"]["receiving_msg_hash"], 
            "utf-8"))
    actor_state["hashes"]["sending_msg_hash"] = hasher.hexdigest()
    del hasher
    
def take_hash_of_receiving_msg(actor_state):
    hasher = hashlib.new("SHA256")
    hasher.update(bytes(
        actor_state["receiving_msg"] + actor_state["hashes"]["sending_msg_hash"],
        "utf-8"))
    actor_state["hashes"]["receiving_msg_hash"] = hasher.hexdigest()
    del hasher

def encrypt_sending_msg(actor_state):
    actor_state["sending_msg"] = bytes(actor_state["sending_msg"], "utf-8")
    cipher = EncryptionTool(
        actor_state["sending_msg"],
        actor_state["hashes"]["receiving_msg_hash"],
        actor_state["hashes"]["receiving_msg_hash"]
    )
    actor_state["sending_msg"] = cipher.encrypt()
    del cipher
    cipher = EncryptionTool(
        actor_state["sending_msg"],
        actor_state["secret_key"],
        actor_state["secret_key"]
    )
    actor_state["sending_msg"] = cipher.encrypt()
    del cipher
    for _ in range(actor_state["sent_counter"]):
        cipher = EncryptionTool(
            actor_state["sending_msg"],
            actor_state["secret_key"],
            actor_state["secret_key"]
        )
        actor_state["sending_msg"] = cipher.encrypt()
        del cipher

def decrypt_receiving_msg(actor_state):
    for _ in range(actor_state["received_counter"]):
        cipher = EncryptionTool(
            actor_state["receiving_msg"],
            actor_state["secret_key"],
            actor_state["secret_key"]
        )
        actor_state["receiving_msg"] = cipher.decrypt()
        del cipher
    cipher = EncryptionTool(
        actor_state["receiving_msg"],
        actor_state["secret_key"],
        actor_state["secret_key"]
    )
    actor_state["receiving_msg"] = cipher.decrypt()
    del cipher
    cipher = EncryptionTool(
        actor_state["receiving_msg"],
        actor_state["hashes"]["sending_msg_hash"],
        actor_state["hashes"]["sending_msg_hash"]
    )
    actor_state["receiving_msg"] = cipher.decrypt().decode("utf-8")
    del cipher

def encrypt(actor_state, sending_msg):
    actor_state["sending_msg"] = sending_msg
    
    take_hash_of_sending_msg(actor_state)
    encrypt_sending_msg(actor_state)
    encode_sending_msg_to_base64(actor_state)

    return actor_state

def decrypt(actor_state, receiving_msg):
    actor_state["receiving_msg"] = receiving_msg
    
    decode_receiving_msg_from_base64(actor_state)
    decrypt_receiving_msg(actor_state)
    take_hash_of_receiving_msg(actor_state)

    return actor_state
    