from cryptography.fernet import Fernet
import os



def genkey():
    key = Fernet.generate_key()

    print(key)
    print(' help')

    with open('./cfg/.network.key','wb') as n:
        n.write(key)