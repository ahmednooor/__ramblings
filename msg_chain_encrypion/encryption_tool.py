import hashlib
from Cryptodome.Cipher import AES

class EncryptionTool:
    """ "EncryptionTool" class from "github.com/nsk89" for file encryption.
    (Has been modified a bit.) """
    def __init__(self, message, user_key, user_salt):
        self.message = message
        
        # convert the key and salt to bytes
        self.user_key = bytes(user_key, "utf-8")
        self.user_salt = bytes(user_key[::-1], "utf-8")
        
        # hash type for hashing key and salt
        self.hash_type = "SHA256"

        # dictionary to store hashed key and salt
        self.hashed_key_salt = dict()

        # hash key and salt into 16 bit hashes
        self.hash_key_salt()

    def encrypt(self):
        # create a cipher object
        cipher_object = AES.new(
            self.hashed_key_salt["key"],
            AES.MODE_CFB,
            self.hashed_key_salt["salt"]
        )

        # encrypt the message
        encrypted_message = cipher_object.encrypt(self.message)

        # clean up the cipher object
        del cipher_object

        return encrypted_message

    def decrypt(self):
        #  exact same as above function except in reverse
        cipher_object = AES.new(
            self.hashed_key_salt["key"],
            AES.MODE_CFB,
            self.hashed_key_salt["salt"]
        )
        
        # decrypt the message
        decrypted_message = cipher_object.decrypt(self.message)

        # clean up the cipher object
        del cipher_object

        return decrypted_message

    def hash_key_salt(self):
        # --- convert key to hash
        #  create a new hash object
        hasher = hashlib.new(self.hash_type)
        hasher.update(self.user_key)

        # turn the output key hash into 32 bytes (256 bits)
        self.hashed_key_salt["key"] = bytes(hasher.hexdigest()[:32], "utf-8")

        # clean up hash object
        del hasher

        # --- convert salt to hash
        #  create a new hash object
        hasher = hashlib.new(self.hash_type)
        hasher.update(self.user_salt)

        # turn the output salt hash into 16 bytes (128 bits)
        self.hashed_key_salt["salt"] = bytes(hasher.hexdigest()[:16], "utf-8")
        
        # clean up hash object
        del hasher
