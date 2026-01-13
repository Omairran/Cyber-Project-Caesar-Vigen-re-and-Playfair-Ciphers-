from abc import ABC, abstractmethod

class Cipher(ABC):
    @abstractmethod
    def encrypt(self, plaintext, key):
        pass

    @abstractmethod
    def decrypt(self, ciphertext, key):
        pass

    def _sanitize_text(self, text):
        """Removes non-alphabetic characters and converts to uppercase."""
        return "".join(filter(str.isalpha, text)).upper()

    def _get_intermediate_steps(self):
        """Returns a list of steps taken during the last operation."""
        return getattr(self, '_steps', [])

    def _add_step(self, step):
        if not hasattr(self, '_steps'):
            self._steps = []
        self._steps.append(step)

    def _clear_steps(self):
        self._steps = []
