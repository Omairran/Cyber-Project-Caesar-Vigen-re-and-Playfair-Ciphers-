from .cipher_base import Cipher

class CaesarCipher(Cipher):
    def encrypt(self, plaintext, key):
        self._clear_steps()
        try:
            shift = int(key) % 26
        except ValueError:
            raise ValueError("Key for Caesar Cipher must be an integer.")

        result = []
        for char in plaintext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                new_char = chr((ord(char) - base + shift) % 26 + base)
                result.append(new_char)
                self._add_step(f"{char} -> {new_char} (Shift {shift})")
            else:
                result.append(char)
        
        return "".join(result)

    def decrypt(self, ciphertext, key):
        self._clear_steps()
        try:
            shift = int(key) % 26
        except ValueError:
            raise ValueError("Key for Caesar Cipher must be an integer.")

        result = []
        for char in ciphertext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                new_char = chr((ord(char) - base - shift) % 26 + base)
                result.append(new_char)
                self._add_step(f"{char} -> {new_char} (Inverse Shift)")
            else:
                result.append(char)
        
        return "".join(result)
