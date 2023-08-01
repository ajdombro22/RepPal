from cryptography.fernet import Fernet
import os
from pathlib import Path

key = Fernet.generate_key()

print(key)
print(' help')

with open('keys.key','wb') as n:
    n.write(key)

with open('dkey.py','w') as k:
    
    k.writelines('class DKey(object): \n')
    k.writelines('    def __init__(self): \n')
    k.writelines(f'        self.key = {key} \n')
    k.writelines(f'        self.id = 12 \n')
    k.writelines(f'        self.netkey = ')
    if os.path.exists('./cfg/.network.key') :
        file = Path('./cfg/.network.key')
        data = file.read_bytes()
        k.writelines(f'{data}')
    else:
        k.writelines('None')
    
    

    
   
   




