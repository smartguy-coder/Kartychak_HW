from cryptography.fernet import Fernet
import os
from time import time
import sys

#secondary functions==================================================================================================

def current_directory() -> None:
    """to be sure that current working directory is located where *.py file is located"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # print(os.getcwd())  # for debug purposes


def isascii(s) -> bool:
    """Check if the characters in string s are in ASCII."""
    return len(s) == len(s.encode())


def system_family_slash() -> str:
    """The function helps to create correct path
    https://docs.python.org/2/library/sys.html#platform
    """

    # print(sys.platform)  # for debug purposes

    if sys.platform.startswith('win'):
        return "\\"
    elif sys.platform.startswith('linux'):
        return "/"
    else:
        # !!! WARNING: the author is not familiar with path-building in other systems. Suppose it looks like linux
        return "/"


#main functions==================================================================================================

def encrypt_func(text_to_encrypt: str) -> [tuple, str]:
    """
    :param text_to_encrypt: ASCII text to encrypt
    :return:
            encryption_time - the timestamp in seconds from beginning of the epoch,
            token - encrypted text in binary format

    the function also writes an encryption key and a token in separated files for storing
    """

    if not isascii(text_to_encrypt):
        return "Cannot encrypt the text. You have entered text not in ASCII. "

    current_directory()

    # key is generated
    key = Fernet.generate_key()

    # value of key is assigned to a variable
    f = Fernet(key)

    # the plaintext is converted to ciphertext
    token = f.encrypt(f'{text_to_encrypt}'.encode('utf-8'))

    # create the timestamp too manage tokens and keys
    encryption_time = time()

    # the first creation folder for logfiles
    if not os.path.exists(f"{os.getcwd()}{system_family_slash()}logfiles"):
        os.mkdir('logfiles')

    # writing logfiles
    with open(f'logfiles{system_family_slash()}crypto_key_{encryption_time}.txt', 'wb') as filelog_key:
        filelog_key.write(key)
    
    with open(f'logfiles{system_family_slash()}crypto_token_{encryption_time}.txt', 'wb') as filelog_token:
        filelog_token.write(token)

    with open(f'logfiles{system_family_slash()}fulltime.txt', 'a') as filelog_fulltime:
        filelog_fulltime.write(str(encryption_time) + '\n')

    return encryption_time, token    


def decrypt_func(encryption_time: float) -> str:
    """
    decrypt text using Fernet class, using saved keys and tokens
    :param encryption_time: the timestamp in seconds from beginning of the epoch, defined in encryption process
    :return: decrypted string
    """
    current_directory()

    if not os.path.exists(f'logfiles{system_family_slash()}crypto_key_{encryption_time}.txt') or \
            not os.path.exists(f'logfiles{system_family_slash()}crypto_token_{encryption_time}.txt'):
        #print("There was no data about encryption at the time")
        return "There was no data about encryption based on your timestamp"

    # loads keys and tokens
    with open(f'logfiles{system_family_slash()}crypto_key_{encryption_time}.txt', 'rb') as filelog_key:
        key = filelog_key.read()
    
    with open(f'logfiles{system_family_slash()}crypto_token_{encryption_time}.txt', 'rb') as filelog_token:
        token = filelog_token.read()

    # value of key is assigned to a variable
    f = Fernet(key)

    # decrypting the ciphertext
    d = f.decrypt(token)

    return d.decode()  # return the plaintext and the decode() method, converts it from byte to string
    




if __name__ == '__main__':
    print(encrypt_func("test string"))
    print(decrypt_func(1624565428.560006))
    