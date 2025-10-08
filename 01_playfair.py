import string
import matplotlib.pyplot as plt
from collections import Counter

# === 2 & 3: KEY MATRIX GENERATION ===
def generate_row_key_matrix(secret_key):
    secret_key = secret_key.upper().replace("J", "I")
    key_letters = []
    for ch in secret_key:
        if ch.isalpha() and ch not in key_letters:
            key_letters.append(ch)
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in key_letters:
            key_letters.append(ch)
    return [key_letters[i*5:(i+1)*5] for i in range(5)]

def generate_column_key_matrix(secret_key):
    secret_key = secret_key.upper().replace("J", "I")
    key_letters = []
    for ch in secret_key:
        if ch.isalpha() and ch not in key_letters:
            key_letters.append(ch)
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in key_letters:
            key_letters.append(ch)
    columns = [key_letters[i*5:(i+1)*5] for i in range(5)]
    return [list(row) for row in zip(*columns)] # transpose

def display_matrix(matrix):
    print("\nKey Matrix:")
    for row in matrix:
        print(' '.join(row))
    print()

# === 5: PLAINTEXT PREPROCESSING & CIPHER ROUTINES ===
def prepare_bigrams(text):
    text = text.upper().replace("J", "I")
    text = ''.join(c for c in text if c.isalpha())
    pairs = []
    i=0
    while i < len(text):
        first = text[i]
        second = text[i+1] if i+1 < len(text) else 'X'
        if first == second:
            pairs.append(first + 'X')
            i += 1
        else:
            pairs.append(first + second)
            i += 2
    if len(pairs[-1]) == 1:
        pairs[-1] += 'X'
    return pairs

def locate_char(matrix, ch):
    for row_idx, row in enumerate(matrix):
        for col_idx, val in enumerate(row):
            if val == ch:
                return row_idx, col_idx
    raise ValueError(f"Char {ch} not in matrix")

def encrypt_pair(matrix, ch1, ch2):
    r1, c1 = locate_char(matrix, ch1)
    r2, c2 = locate_char(matrix, ch2)
    if r1 == r2:
        return matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
    if c1 == c2:
        return matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
    return matrix[r1][c2] + matrix[r2][c1]

def decrypt_pair(matrix, ch1, ch2):
    r1, c1 = locate_char(matrix, ch1)
    r2, c2 = locate_char(matrix, ch2)
    if r1 == r2:
        return matrix[r1][(c1-1)%5] + matrix[r2][(c2-1)%5]
    if c1 == c2:
        return matrix[(r1-1)%5][c1] + matrix[(r2-1)%5][c2]
    return matrix[r1][c2] + matrix[r2][c1]

def playfair_encrypt(plain_text, secret_key, layout='row'):
    matrix = generate_row_key_matrix(secret_key) if layout == 'row' else generate_column_key_matrix(secret_key)
    bigrams = prepare_bigrams(plain_text)
    return ''.join(encrypt_pair(matrix, pair[0], pair[1]) for pair in bigrams)

def playfair_decrypt(cipher_text, secret_key, layout='row'):
    matrix = generate_row_key_matrix(secret_key) if layout == 'row' else generate_column_key_matrix(secret_key)
    bigrams = [cipher_text[i:i+2] for i in range(0, len(cipher_text), 2)]
    return ''.join(decrypt_pair(matrix, pair[0], pair[1]) for pair in bigrams)

# === 4: COMPARATIVE ANALYSIS ===
def analyze_cipher_difference(ct1, ct2):
    diff = sum(x != y for x, y in zip(ct1, ct2))
    print(f"\nHamming Distance: {diff}/{len(ct1)} differing characters")
    freq1 = Counter(ct1[i:i+2] for i in range(0, len(ct1), 2))
    freq2 = Counter(ct2[i:i+2] for i in range(0, len(ct2), 2))
    labels = sorted(set(freq1) | set(freq2))
    v1 = [freq1.get(label, 0) for label in labels]
    v2 = [freq2.get(label, 0) for label in labels]
    plt.figure(figsize=(12, 5))
    plt.bar(labels, v1, alpha=0.6, label='Row-wise')
    plt.bar(labels, v2, alpha=0.6, label='Col-wise')
    plt.title('Digraph Frequency Comparison')
    plt.xlabel('Digraph')
    plt.ylabel('Count')
    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()
    plt.show()

# === 6: BRUTE-FORCE CRYPTANALYSIS ===
def looks_like_english(text):
    return any(word in text for word in ["THE", "AND", "ING", "ION"])

def brute_force_decrypt(cipher_text, trial_keys):
    print("\nStarting brute-force attack...")
    for test_key in trial_keys:
        for layout_type in ('row', 'col'):
            try:
                possible = playfair_decrypt(cipher_text, test_key, layout_type)
                if looks_like_english(possible):
                    print(f"Match: Key={test_key}, Mode={layout_type}")
                    print("Decrypted:", possible)
                    return
            except:
                continue
    print("No match found.")

# === RUN SAMPLE ===
if __name__ == '__main__':
    secret = "PLAYFAIR EXAMPLE"
    message = "Hide the gold in the tree stump"
    print("Original:", message)

    row_encrypted = playfair_encrypt(message, secret, 'row')
    col_encrypted = playfair_encrypt(message, secret, 'col')

    print("Row-wise:", row_encrypted)
    print("Col-wise:", col_encrypted)

    display_matrix(generate_row_key_matrix(secret))
    display_matrix(generate_column_key_matrix(secret))

    print("Decrypted Row:", playfair_decrypt(row_encrypted, secret, 'row'))
    print("Decrypted Col:", playfair_decrypt(col_encrypted, secret, 'col'))

    analyze_cipher_difference(row_encrypted, col_encrypted)
    brute_force_decrypt(row_encrypted, ["SECRET", "PLAYFAIR", "EXAMPLE", "KEYWORD"])