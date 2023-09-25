import joblib
import time
from phe import paillier

# public_key1, private_key1 = paillier.generate_paillier_keypair()
keyring_a = paillier.PaillierPrivateKeyring()
public_key_a, private_key_a = paillier.generate_paillier_keypair(keyring_a)

secret_num_a = 3
a = time.time()
public_num_a = public_key_a.encrypt(secret_num_a)
print('encryption time per entry:', (time.time() - a))
# encryption time per entry: 0.01190495491027832

secret_list_b = list(range(100))

a = time.time()
computed_by_b = [a-x for a in [public_num_a] for x in secret_list_b]
print('computation time per entry:', (time.time() - a) / len(computed_by_b))
# computation time per entry: 0.00017836189270019532
# computed_by_b[0].ciphertext()
len(computed_by_b)
cipher_computed_by_b = [(a-x).ciphertext() for a in [public_num_a] for x in secret_list_b]

joblib.dump(computed_by_b, 'computed_by_b.pkl')
joblib.dump(cipher_computed_by_b, 'cipher_computed_by_b.pkl')
# from functools import reduce
# reduce(lambda x,y: x*y, computed_by_b)

time.time() - a
# 0.001s per computation

a = time.time()
decrypted_list = [private_key_a.decrypt(x) for x in computed_by_b]
print('number', secret_num_a, 'in B side:', 0 in decrypted_list)
print('decryption time per entry:', (time.time() - a) / len(decrypted_list))
# decryption time per entry: 0.10290706324577331

decrypted_list.index(0)

# scalability
    # time: 
        # step 1: encryption on side A, 0.37s per entry --> 1 time, not affect scalability
        # step 2: computation of encrypted data of A and naked data of B on B side -> 0.0012s per entry
        # step 3: decryption on computed data on A side -> 0.1s per entry on single machine --> easy to parralel
    # object size transmission 
        # 1kb per serialized entry
        # general case: 100,000 entry to check --> 100,000 KB --> 100 MB :v impossible to zip
        # zip ratio: 97% -> almost nothing
        # we need better way to do this
        # if give partition signal ratio 100: go to 1000 --> 1 MB: possible


# zip test

import lzma
import zlib
import gzip
import bz2
import numpy as np
compressors = ['lzma','zlib','gzip','bz2'] 
a = np.exp(np.random.rand(1024))
b = np.arange(1024)
b[32] = -10
b[96] = 20000
a = bytes(a)
b = bytes(b)

for i in range(len(compressors)):
    print("{} compression ratio: ".format(compressors[i]))
    a_lzma = eval(compressors[i]).compress(a)
    b_lzma = eval(compressors[i]).compress(b)
    print(float(len(a_lzma))/len(a),float(len(b_lzma))/len(b))
    print("\n")

