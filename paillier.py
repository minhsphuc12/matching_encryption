from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
PKCS1_OAEP

# A is the one who need to check
# B has the list that A need to check agains

# Key generation (org A and org B would generate their own key pairs)
org_a_key = RSA.generate(2048)
# org_a_key
# org_a_key.public_key()

org_b_key = RSA.generate(2048)

# Data preparation (org A and org B prepare their respective sets)
org_a_set = [123, 456, 789]
org_b_set = [456, 789, 1011, 123]

# Encryption (org A encrypts its set using org B's public key)
org_b_public_key = org_b_key.publickey()
# org_a_encrypted_set = [org_b_public_key.encrypt(str(x).encode(), None) for x in org_a_set]

org_a_encrypted_set = [PKCS1_OAEP.new(str(x).encode(), None) for x in org_a_set]

# Encryption (org B encrypts its set using org A's public key)
org_a_public_key = org_a_key.publickey()
# org_b_encrypted_set = [org_a_public_key.encrypt(str(x).encode(), None) for x in org_b_set]

org_b_encrypted_set = [PKCS1_OAEP.new(str(x).encode(), None) for x in org_b_set]

# Intersection computation (org A and org B exchange and compute)
intersection = []
for encrypted_value_a in org_a_encrypted_set:
    for encrypted_value_b in org_b_encrypted_set:
        # Check if the encrypted values are the same (implies intersection)
        if encrypted_value_a == encrypted_value_b:
            intersection.append(encrypted_value_a)

# Decryption (both parties decrypt the intersection)
cipher = PKCS1_OAEP.new(org_a_key)
plain_intersection = [int(cipher.decrypt(x[0])) for x in intersection]

print("Intersection:", plain_intersection)
