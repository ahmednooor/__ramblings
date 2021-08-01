"""
concept:
- two actors A and B
- A and B exchange keys with some method i.e. DH-Exchange
- when one actor sends message to the second actor, 
  it will encrypt it not only with the secret key but also 
  with the hash of previously received message from other actor.
- hash of previous message will not just be a hash of message it self but
  hash of message + hash of previous message. this way the encryption
  will not just be depended upon last received message but on the whole
  conversation forming a sort of message chain
"""

import hashlib
import base64
import random
from rand_prime import generate_prime_number
from encryption_tool import EncryptionTool


class Actor:

    def __init__(self, id_):
        self.secret_key = ""
        self.receiving_msg = ""
        self.sending_msg = ""
        self.sent_counter = 0
        self.received_counter = 0
        self.id = id_
        self.hashes = {
            "receiving_msg_hash": "",
            "sending_msg_hash": ""
        }
        self._dh_exchange_nums = None

    def send(self, sending_msg, to):
        if self._dh_exchange_nums is None:
            print("ERROR")
            return
        self.sending_msg = sending_msg
        print()
        print()
        print("[" + self.id + "] --> [" + to.id + "]")
        print("<-------------------------------------->")
        print(self.id + ": sending msg [plain]")
        print(self.sending_msg)
        print("<-------------------------------------->")
        self._take_hash_of_sending_msg()
        self._encrypt_sending_msg()
        print(self.id + ": sending msg [encrypted]")
        print(self.sending_msg)
        print("<-------------------------------------->")
        self.sending_msg = str(base64.b64encode(self.sending_msg), "utf-8")
        print(self.id + ": sending msg [encrypted] [base64]")
        print(self.sending_msg)
        print("<-------------------------------------->")
        to.receive(self.sending_msg)
        self._update_counters_for_send()

    def receive(self, receiving_msg):
        self.receiving_msg = receiving_msg
        print(self.id + ": receiving msg [encrypted] [base64]")
        print(self.receiving_msg)
        print("<-------------------------------------->")
        self.receiving_msg = base64.b64decode(
            bytes(self.receiving_msg, "utf-8"))
        print(self.id + ": receiving msg [encrypted]")
        print(self.receiving_msg)
        print("<-------------------------------------->")
        self._decrypt_receiving_msg()
        self._take_hash_of_receiving_msg()
        print(self.id + ": receiving msg [plain]")
        print(self.receiving_msg)
        print("<-------------------------------------->")
        self._update_counters_for_receive()

    def _take_hash_of_sending_msg(self):
        hasher = hashlib.new("SHA256")
        hasher.update(
            bytes(
                self.sending_msg + self.hashes["receiving_msg_hash"], 
                "utf-8"))
        self.hashes["sending_msg_hash"] = hasher.hexdigest()
        del hasher
    
    def _take_hash_of_receiving_msg(self):
        hasher = hashlib.new("SHA256")
        hasher.update(bytes(
            self.receiving_msg + self.hashes["sending_msg_hash"], "utf-8"))
        self.hashes["receiving_msg_hash"] = hasher.hexdigest()
        del hasher

    def _encrypt_sending_msg(self):
        self.sending_msg = bytes(self.sending_msg, "utf-8")
        cipher = EncryptionTool(
            self.sending_msg,
            self.hashes["receiving_msg_hash"],
            self.hashes["receiving_msg_hash"]
        )
        self.sending_msg = cipher.encrypt()
        del cipher
        cipher = EncryptionTool(
            self.sending_msg,
            self.secret_key,
            self.secret_key
        )
        self.sending_msg = cipher.encrypt()
        del cipher
        for _ in range(self.sent_counter):
            cipher = EncryptionTool(
                self.sending_msg,
                self.secret_key,
                self.secret_key
            )
            self.sending_msg = cipher.encrypt()
            del cipher

    def _decrypt_receiving_msg(self):
        for _ in range(self.received_counter):
            cipher = EncryptionTool(
                self.receiving_msg,
                self.secret_key,
                self.secret_key
            )
            self.receiving_msg = cipher.decrypt()
            del cipher
        cipher = EncryptionTool(
            self.receiving_msg,
            self.secret_key,
            self.secret_key
        )
        self.receiving_msg = cipher.decrypt()
        del cipher
        cipher = EncryptionTool(
            self.receiving_msg,
            self.hashes["sending_msg_hash"],
            self.hashes["sending_msg_hash"]
        )
        self.receiving_msg = cipher.decrypt().decode("utf-8")
        del cipher

    def _update_counters_for_send(self):
        self.sent_counter += 1
        self.received_counter = 0

    def _update_counters_for_receive(self):
        self.received_counter += 1
        self.sent_counter = 0

    def dh_key_exchange_with(self, with_):
        self._dh_exchange_nums = {
            "s": generate_prime_number(8),
            # "p": 22149933441438428019642564587552585228124573363141857139422919880330823144769391820414465151699878126956877461319981085932391707535633447728637327694483655309184513390423450317672614687321342396603521397323411201435124964246272814681885271466467794836814127306693790639794542143936246227343125430441273155781894775922083981073391045061009954633068766197959650232446007974990492384290116053545775236625856664944160851925873634585913657085126568946341311838169893164466688670723214144528468393675478459438554912206415986204368697578717212156399328867027740191278845224897496525717193558162229041868711482314921486269363,
            "p": generate_prime_number(8),
            "g": generate_prime_number(4),
            "A": None,
            "B": None,
            "key": None
        }
        self._dh_exchange_nums["A"] = \
            self._dh_exchange_nums["g"] ** self._dh_exchange_nums["s"] % \
            self._dh_exchange_nums["p"]
        self._dh_exchange_nums["B"] = with_.dh_key_exchange_receive_initial(
            p=self._dh_exchange_nums["p"],
            g=self._dh_exchange_nums["g"],
            A=self._dh_exchange_nums["A"]
        )
        self._dh_exchange_nums["key"] = \
            self._dh_exchange_nums["B"] ** self._dh_exchange_nums["s"] % \
            self._dh_exchange_nums["p"]
        self.secret_key = str(self._dh_exchange_nums["key"])
        print("---------- s 1")
        print(self._dh_exchange_nums["s"])
        print("---------- p 1")
        print(self._dh_exchange_nums["p"])
        print("---------- g 1")
        print(self._dh_exchange_nums["g"])
        print("---------- sec key")
        print(self.secret_key)


    def dh_key_exchange_receive_initial(self, p, g, A):
        self._dh_exchange_nums = {
            "s": generate_prime_number(8),
            "p": p,
            "g": g,
            "A": A,
            "B": None,
            "key": None
        }
        self._dh_exchange_nums["B"] = \
            self._dh_exchange_nums["g"] ** self._dh_exchange_nums["s"] % \
            self._dh_exchange_nums["p"]
        self._dh_exchange_nums["key"] = \
            self._dh_exchange_nums["A"] ** self._dh_exchange_nums["s"] % \
            self._dh_exchange_nums["p"]
        self.secret_key = str(self._dh_exchange_nums["key"])
        print("---------- s 2")
        print(self._dh_exchange_nums["s"])
        print("---------- g 1")
        print(self._dh_exchange_nums["g"])
        print("---------- p 2")
        print(self._dh_exchange_nums["p"])
        print("---------- sec key")
        print(self.secret_key)
        return self._dh_exchange_nums["B"]
        

def main():
    alice = Actor("Alice")
    bob = Actor("Bob")
    
    alice.dh_key_exchange_with(bob)
    
    alice.send("1 message", to=bob)
    bob.send("2 message", to=alice)
    alice.send("3 message", to=bob)
    alice.send("4 message", to=bob)
    bob.send("5 message", to=alice)
    alice.send("6 message", to=bob)
    alice.send("7 message", to=bob)
    bob.send("8 message", to=alice)
    bob.send("9 message", to=alice)
    bob.send("10 message", to=alice)
    bob.send("same message", to=alice)
    bob.send("same message", to=alice)

if __name__ == "__main__":
    main()
