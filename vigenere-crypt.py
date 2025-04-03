from collections import Counter
import re
from math import gcd
from functools import reduce

def calculate_ic(text):
    """Calcule l'Indice de Coïncidence du texte."""
    text = re.sub(r'[^A-Z]', '', text)  # Retirer les espaces et caractères non alphabétiques
    N = len(text)
    if N < 2:
        return 0
    
    freq = Counter(text)
    ic = sum(f * (f - 1) for f in freq.values()) / (N * (N - 1))
    return ic

def letter_frequency_analysis(text):
    """Analyse de fréquence des lettres."""
    text = re.sub(r'[^A-Z]', '', text)
    total_letters = len(text)
    freq = Counter(text)
    freq_percent = {char: (count / total_letters) * 100 for char, count in freq.items()}
    return dict(sorted(freq_percent.items(), key=lambda x: x[1], reverse=True))

def kasiski_test(text, min_length=3):
    """Test de Kasiski pour détecter la longueur de la clé en repérant des séquences répétées."""
    text = re.sub(r'[^A-Z]', '', text)
    substr_positions = {}
    
    for i in range(len(text) - min_length):
        substring = text[i:i + min_length]
        if substring in substr_positions:
            substr_positions[substring].append(i)
        else:
            substr_positions[substring] = [i]
    
    repeated_patterns = {k: v for k, v in substr_positions.items() if len(v) > 1}
    gaps = [positions[j + 1] - positions[j] for positions in repeated_patterns.values() for j in range(len(positions) - 1)]
    
    return repeated_patterns, gaps

def estimate_key_length(gaps):
    """Estime la longueur probable de la clé en calculant le PGCD des écarts Kasiski."""
    return reduce(gcd, gaps) if gaps else None

def decrypt_caesar(cipher_text):
    """Décrypte un texte chiffré par César en testant tous les décalages."""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    best_shift = 0
    best_ic = 0
    best_plaintext = ""
    
    for shift in range(26):
        decrypted_text = "".join(alphabet[(alphabet.index(c) - shift) % 26] if c in alphabet else c for c in cipher_text)
        ic = calculate_ic(decrypted_text)
        
        if ic > best_ic:
            best_ic = ic
            best_shift = shift
            best_plaintext = decrypted_text
    
    return best_shift, best_plaintext

# Texte chiffré
cipher_text = """TAUTF KWKJH ISAJF IFIO JTDTA UTFWG TJHIS AISWI GBTA UTFWG
TJSIZ G’TAJ TOIT AUTFK WKJGP BWNID DIGB TAIDF UIEWG FWKA
IZGID FTWKK IIFF WGDAI DPBWE AIOID DWKFP WDID DWGUJ TKAIN
WGBTB IAIPB IKUI FTAIN NJSIF WGFA IDSLT NNBID IFAID OWFD AI-
DUJ FIDIF AIDKW ODAI DPLBJ DIDIF AIDPT ICID IFOJA CBIAI DOIKJ
SIDUG OJTFB IDWG DAIDL GIIDU IDIKN JKFDP BWUTC IDJH ISAID
SBJTI DUIFW GFIDA IDSWG AIGBD DGBA IFJEA IJGKW TBUGO JA-
LIG BTAU IDDTK IAIHT DJCIU GEWKL IGB"""

# Calculs
ic_value = calculate_ic(cipher_text)
freq_analysis = letter_frequency_analysis(cipher_text)
repeated_patterns, kasiski_gaps = kasiski_test(cipher_text)
estimated_key_len = estimate_key_length(kasiski_gaps)
best_shift, decrypted_text = decrypt_caesar(cipher_text)

# Affichage des résultats
print(f"Indice de Coïncidence: {ic_value}")
print("Analyse de fréquence des lettres:")
for letter, percent in freq_analysis.items():
    print(f"{letter}: {percent:.2f}%")
print(f"Longueur estimée de la clé (Kasiski): {estimated_key_len}")
print(f"Décalage César détecté: {best_shift}")
print("Texte déchiffré:")
print(decrypted_text)
