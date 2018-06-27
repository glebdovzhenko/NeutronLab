from cryptography.fernet import Fernet
import os
from config import config
import pickle


if __name__ == '__main__':
    for f_name in os.listdir(config.project_root):
        if 'secret' in f_name and '.key' in f_name:
            break

    with open(f_name, 'r') as f:
        key = bytes(f.read(), encoding='UTF-8')

    cipher_suite = Fernet(key)

    with open('instruments.locked', 'rb') as f:
        unlocked = pickle.loads(cipher_suite.decrypt(f.read()))

    if not os.path.exists(config.instr_path):
        os.makedirs(config.instr_path)

    for f_name in unlocked:
        with open(os.path.join(config.instr_path, f_name), 'w') as f:
            f.write(unlocked[f_name])

    #  #################################################
    #
    # success = []
    # for f_name in os.listdir(config.instr_path):
    #     with open(os.path.join(config.instr_path, f_name)) as f:
    #         with open(os.path.join(config.instr_path + '_', f_name)) as f_:
    #             success.append(f.read() == f_.read())
    #
    # if all(success):
    #     print('Разблокировка успешна')
