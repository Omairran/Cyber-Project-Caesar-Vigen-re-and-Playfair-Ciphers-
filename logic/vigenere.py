from .cipher_base import Cipher

class VigenereCipher(Cipher):
    def encrypt(self, plaintext, key):
        self._clear_steps()
        if not key:
            raise ValueError("Key for Vigenère Cipher cannot be empty.")

        result = []
        k_idx = 0
        for char in plaintext:
            if char.isalpha():
                k_char = key[k_idx % len(key)]
                shift = ord(k_char.upper()) - ord('A')
                base = ord('A') if char.isupper() else ord('a')
                new_char = chr((ord(char) - base + shift) % 26 + base)
                result.append(new_char)
                self._add_step(f"{char} + {k_char} -> {new_char}")
                k_idx += 1
            else:
                result.append(char)

        return "".join(result)

    def decrypt(self, ciphertext, key):
        self._clear_steps()
        if not key:
            raise ValueError("Key for Vigenère Cipher cannot be empty.")

        result = []
        k_idx = 0
        for char in ciphertext:
            if char.isalpha():
                k_char = key[k_idx % len(key)]
                shift = ord(k_char.upper()) - ord('A')
                base = ord('A') if char.isupper() else ord('a')
                new_char = chr((ord(char) - base - shift) % 26 + base)
                result.append(new_char)
                self._add_step(f"{char} - {k_char} -> {new_char}")
                k_idx += 1
            else:
                result.append(char)

        return "".join(result)
