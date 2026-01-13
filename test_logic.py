from logic import CaesarCipher, VigenereCipher, PlayfairCipher

def test_ciphers():
    # Caesar Test
    c = CaesarCipher()
    res = c.encrypt("HELLO", 3)
    print(f"Caesar Encrypt: HELLO (3) -> {res}")
    assert res == "KHOOR"
    res = c.decrypt("KHOOR", 3)
    print(f"Caesar Decrypt: KHOOR (3) -> {res}")
    assert res == "HELLO"

    # Vigenere Test
    v = VigenereCipher()
    res = v.encrypt("ATTACKATDAWN", "LEMON")
    print(f"Vigenere Encrypt: ATTACKATDAWN (LEMON) -> {res}")
    assert res == "LXFOPVEFRNHR"
    res = v.decrypt("LXFOPVEFRNHR", "LEMON")
    print(f"Vigenere Decrypt: LXFOPVEFRNHR (LEMON) -> {res}")
    assert res == "ATTACKATDAWN"

    # Playfair Test
    p = PlayfairCipher()
    # Using standard example from Wikipedia or similar
    # Matrix for "MONARCHY":
    # M O N A R
    # C H Y B D
    # E F G I K
    # L P Q S T
    # U V W X Z
    res = p.encrypt("INSTRUMENTS", "MONARCHY")
    print(f"Playfair Encrypt: INSTRUMENTS (MONARCHY) -> {res}")
    # Expected: GATLMZCLRQXA (padded with X)
    assert res == "GATLMZCLRQXA"
    res = p.decrypt("GATLMZCLRQXA", "MONARCHY")
    print(f"Playfair Decrypt: GATLMZCLRQXA (MONARCHY) -> {res}")
    # Note: Playfair might have 'X' padding or 'I/J' substitution
    # "INSTRUMENTS" -> "IN ST RU ME NT SX"
    # Decrypt -> "INSTRUMENTSX"
    assert res == "INSTRUMENTSX"

    print("All logic tests passed!")

if __name__ == "__main__":
    test_ciphers()
