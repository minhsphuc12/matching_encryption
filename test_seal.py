from seal import EncryptionParameters, SEALContext, KeyGenerator, Encryptor, Decryptor, Evaluator, IntegerEncoder

# Create encryption parameters and context
params = EncryptionParameters()
params.set_poly_modulus("1x^2048 + 1")
params.set_coeff_modulus([40961, 65537])
params.set_plain_modulus(2 ** 8)
context = SEALContext(params)

# Create keys and encryptor/decryptor
keygen = KeyGenerator(context)
public_key = keygen.public_key()
secret_key = keygen.secret_key()
encryptor = Encryptor(context, public_key)
decryptor = Decryptor(context, secret_key)

# Create an evaluator for homomorphic operations
evaluator = Evaluator(context)

# Integer encoder for plaintext conversion
encoder = IntegerEncoder(context)

# Plaintext values
plain_text1 = 7
plain_text2 = 3

# Encrypt the plaintext values
encrypted1 = encryptor.encrypt(encoder.encode(plain_text1))
encrypted2 = encryptor.encrypt(encoder.encode(plain_text2))

# Multiply encrypted1 with encrypted2 using re-encryption
re_encrypted1 = evaluator.relinearize(encrypted1)
result = evaluator.multiply(re_encrypted1, encrypted2)

# Decrypt the result
decrypted_result = decryptor.decrypt(result)

print("Encrypted1:", encrypted1)
print("Encrypted2:", encrypted2)
print("Re-encrypted1:", re_encrypted1)
print("Result:", decrypted_result)
