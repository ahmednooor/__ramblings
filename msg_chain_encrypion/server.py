import uuid
import hashlib
import json
import copy
from encryption_tool import EncryptionTool
from rand_prime import generate_prime_number
from flask import Flask, escape, request, jsonify

from helpers import (
    encrypt,
    decrypt,
    new_actor_state
)

app = Flask(__name__)

STORE = {
    "clients": {}
}

@app.route("/")
def hello():
    return f"Working!"

@app.route("/dh_key_exchange", methods=["POST"])
def dh_key_exchange():
    temp_state = new_actor_state()

    temp_state["dh_exchange_nums"]["s"] = generate_prime_number(8)
    
    temp_state["dh_exchange_nums"]["p"] = int(request.args.get("a"))
    temp_state["dh_exchange_nums"]["g"] = int(request.args.get("b"))
    temp_state["dh_exchange_nums"]["A"] = int(request.args.get("c"))
    
    temp_state["dh_exchange_nums"]["B"] = \
        temp_state["dh_exchange_nums"]["g"] ** \
        temp_state["dh_exchange_nums"]["s"] % \
        temp_state["dh_exchange_nums"]["p"]
    
    temp_state["dh_exchange_nums"]["key"] = \
        temp_state["dh_exchange_nums"]["A"] ** \
        temp_state["dh_exchange_nums"]["s"] % \
        temp_state["dh_exchange_nums"]["p"]
    
    temp_state["secret_key"] = str(temp_state["dh_exchange_nums"]["key"])

    client_uuid = str(uuid.uuid4())
    client_password = str(uuid.uuid4())
    client_password_hash = hashlib.new("SHA256")
    client_password_hash.update(bytes(client_password, "utf-8"))
    client_password_hash = client_password_hash.hexdigest()
    
    temp_state["id"] = client_uuid
    temp_state["password"] = client_password_hash
    
    encrypt(
        temp_state,
        json.dumps({
            "id": client_uuid,
            "password": client_password
        })
    )

    STORE["clients"][client_uuid] = temp_state
    
    print("B")
    print(str(temp_state["dh_exchange_nums"]["B"]))
    print("sec_key")
    print(STORE["clients"][client_uuid]["secret_key"])
    print("id")
    print(client_uuid)
    print("password hash")
    print(STORE["clients"][client_uuid]["password"])
    print("password")
    print(client_password)
    print("sending msg")
    print(STORE["clients"][client_uuid]["sending_msg"])

    return jsonify({
        "B": str(STORE["clients"][client_uuid]["dh_exchange_nums"]["B"]),
        "payload": STORE["clients"][client_uuid]["sending_msg"]
    })

@app.route("/verify_dh_key_exchange", methods=["POST"])
def verify_dh_key_exchange():
    client_uuid = request.args.get("a")
    client_password = request.args.get("b")

    print(client_password)

    temp_state = copy.deepcopy(STORE["clients"][client_uuid])

    if client_uuid != temp_state["id"]:
        return jsonify({"status": "error"})
    
    decrypt(
        temp_state, 
        client_password
    )

    client_password = temp_state["receiving_msg"]
    
    client_password_hash = hashlib.new("SHA256")
    client_password_hash.update(bytes(client_password, "utf-8"))
    client_password_hash = client_password_hash.hexdigest()
    
    if client_password_hash != temp_state["password"]:
        return jsonify({"status": "error"})
    
    print(client_password)
    print(client_password_hash)
    print(temp_state["password"])
    
    STORE["clients"][client_uuid] = temp_state
    
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)