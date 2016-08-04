from Crypto.Cipher import AES
BLOCK_SIZE = 16
AES_KEY = "YELLOW SUBMARINE"
import time

def cbc_encrypt_keystream(nonce, key):
    cipher = AES.new(key, AES.MODE_ECB)
    cipher_text = cipher.encrypt(nonce)
    return cipher_text

def bitwise_xor(s1,s2):
    return ''.join([chr(ord(x)^ord(y)) for x,y in zip(s1,s2)])

def generate_keystream(key, plain_text):
    needed_length = 1+len(plain_text)//16
    keystream = ''
    for i in range(needed_length):
        nonce = chr(0)*8 + chr(i) + chr(0)*7
        keystream+=cbc_encrypt_keystream(nonce, key)
    return keystream

def ctr_encrypt(plain_text, key):
    keystream = generate_keystream(key, plain_text)
    return bitwise_xor(plain_text, keystream)

def ctr_decrypt(cipher_text, key):
    return ctr_encrypt(cipher_text, key)

def get_texts():
    f = open('20_ciphertext.txt','r')
    c = []
    for line in f:
        c.append(line.rstrip().decode('base64'))
    f.close()
    return c

def encrypt_plaintexts(p):
    c = []
    for pt in p:
        c.append(ctr_encrypt(pt, AES_KEY))
    return c

def get_frequencies(s):
    s = s.upper()
    frequencies = {}
    for char in s:
        try:
            frequencies[char]+=1
        except:
            frequencies[char]=1
    return frequencies

def evaluate_string(s):
    frequencies_observed = get_frequencies(s)
    frequency_dict = {' ': 20.0, 'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
    c = 0
    n = 0
    for char in frequency_dict:
        try:
            observed = frequencies_observed[char]
        except:
            observed = 0
        expected = (frequency_dict[char]/100)*len(s)
        delta = expected-observed
        c+= (delta**2)
        n+= expected**2
    return (c+0.0)/n

def print_cipher_for_key_guess(cyphertexts, current_guess):
    for c in cyphertexts:
        cd = ''
        for i in range(len(c)):
            cc = c[i]
            kt = current_guess[i]
            if kt != '0':
                cd+=chr(ord(kt)^ord(cc))
            else:
                cd+='_'
        print cd

def get_columns(rows):
    columns = []
    for i in range(len(rows[0])):
        c = []
        for j in range(len(rows)):
            c.append(rows[j][i])
        columns.append(c)
    return columns

def guess_key_character(column):
    m = 1000000
    m_key = ''
    for i in range(256):
        c_xor = [chr(ord(c)^i) for c in column]
        c_string = ''.join(c_xor)
        if evaluate_string(c_string)<m:
            m = evaluate_string(c_string)
            m_key = chr(i)
    return m_key

if __name__ == "__main__":
    c = get_texts()
    c_crypt = encrypt_plaintexts(c)
    common_length = min([len(x) for x in c_crypt])
    c_crypt = [x[:common_length] for x in c_crypt]
    columns = get_columns(c_crypt)
    guessed_key = ['0']*common_length
    for index, column in enumerate(columns):
        guessed_key[index] = guess_key_character(column)
    key = ''.join(guessed_key)
    for c in c_crypt:
        print bitwise_xor(key, c)
