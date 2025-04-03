def vigenere_cipher(text, key, encrypt=True):
    min_ascii, max_ascii = 33, 126 
    alphabet_size = max_ascii - min_ascii + 1
    key_length = len(key)
    result = []
    
    for i, char in enumerate(text):
        if min_ascii <= ord(char) <= max_ascii:
            shift = ord(key[i % key_length]) - min_ascii
            if not encrypt:
                shift = -shift
            new_char = chr(min_ascii + (ord(char) - min_ascii + shift) % alphabet_size)
            result.append(new_char)
        else:
            result.append(char) 
    
    return ''.join(result)

# Test de vérification 
message = "bonjour tous le monde "  
key = "SECRET" 

encrypted_message = vigenere_cipher(message, key, encrypt=True)
decrypted_message = vigenere_cipher(encrypted_message, key, encrypt=False)

print("Message original:", message)
print("Message chiffré:", encrypted_message)
print("Message déchiffré:", decrypted_message)

# Vérification
assert message == decrypted_message, "Erreur : le déchiffrement ne correspond pas au message original"