from phe import paillier

def encrypt_data(data):
    public_key, private_key = paillier.generate_paillier_keypair()
    encrypted_data = public_key.encrypt(data)
    return encrypted_data, private_key

def decrypt_data(encrypted_data, private_key):
    decrypted_data = private_key.decrypt(encrypted_data)
    return decrypted_data
