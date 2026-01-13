from .cipher_base import Cipher

class PlayfairCipher(Cipher):
    def _create_matrix(self, key):
        key = self._sanitize_text(key).replace('J', 'I')
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        matrix_chars = []
        for char in key:
            if char not in matrix_chars and char in alphabet:
                matrix_chars.append(char)
        for char in alphabet:
            if char not in matrix_chars:
                matrix_chars.append(char)
        
        matrix = [matrix_chars[i:i+5] for i in range(0, 25, 5)]
        self._add_step("Playfair Matrix (5x5):")
        for row in matrix:
            self._add_step("  " + " ".join(row))
        return matrix, matrix_chars

    def _get_pos(self, char, matrix):
        for r, row in enumerate(matrix):
            if char in row:
                return r, row.index(char)
        return None

    def _prepare_text(self, text):
        text = self._sanitize_text(text).replace('J', 'I')
        res = []
        i = 0
        while i < len(text):
            c1 = text[i]
            if i + 1 < len(text):
                c2 = text[i+1]
                if c1 == c2:
                    res.append(c1 + 'X')
                    i += 1
                else:
                    res.append(c1 + c2)
                    i += 2
            else:
                res.append(c1 + 'X')
                i += 1
        return res

    def encrypt(self, plaintext, key):
        self._clear_steps()
        if not key:
            raise ValueError("Key for Playfair Cipher cannot be empty.")
        
        matrix, matrix_list = self._create_matrix(key)
        pairs = self._prepare_text(plaintext)
        
        result = []
        detailed_steps = []
        
        for pair in pairs:
            r1, c1 = self._get_pos(pair[0], matrix)
            r2, c2 = self._get_pos(pair[1], matrix)
            
            if r1 == r2:
                # Same row
                n1_col, n2_col = (c1 + 1) % 5, (c2 + 1) % 5
                n1, n2 = matrix[r1][n1_col], matrix[r2][n2_col]
                rule = "Same Row"
                coords = [(r1, c1), (r2, c2), (r1, n1_col), (r2, n2_col)]
            elif c1 == c2:
                # Same column
                n1_row, n2_row = (r1 + 1) % 5, (r2 + 1) % 5
                n1, n2 = matrix[n1_row][c1], matrix[n2_row][c2]
                rule = "Same Column"
                coords = [(r1, c1), (r2, c2), (n1_row, c1), (n2_row, c2)]
            else:
                # Rectangle
                n1, n2 = matrix[r1][c2], matrix[r2][c1]
                rule = "Rectangle"
                coords = [(r1, c1), (r2, c2), (r1, c2), (r2, c1)]
            
            result.append(n1 + n2)
            step_desc = f"{pair} -> {n1}{n2} ({rule})"
            self._add_step(step_desc)
            detailed_steps.append({
                "pair": pair,
                "result": n1 + n2,
                "rule": rule,
                "coords": coords # [(orig1), (orig2), (new1), (new2)]
            })

        self._animation_data = {
            "matrix": matrix,
            "steps": detailed_steps
        }
        return "".join(result)

    def decrypt(self, ciphertext, key):
        self._clear_steps()
        if not key:
            raise ValueError("Key for Playfair Cipher cannot be empty.")
        
        matrix, _ = self._create_matrix(key)
        ciphertext = self._sanitize_text(ciphertext)
        if len(ciphertext) % 2 != 0:
            raise ValueError("Ciphertext for Playfair must have even length.")
            
        pairs = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
        
        result = []
        detailed_steps = []
        
        for pair in pairs:
            r1, c1 = self._get_pos(pair[0], matrix)
            r2, c2 = self._get_pos(pair[1], matrix)
            
            if r1 == r2:
                n1_col, n2_col = (c1 - 1) % 5, (c2 - 1) % 5
                n1, n2 = matrix[r1][n1_col], matrix[r2][n2_col]
                rule = "Same Row"
                coords = [(r1, c1), (r2, c2), (r1, n1_col), (r2, n2_col)]
            elif c1 == c2:
                n1_row, n2_row = (r1 - 1) % 5, (r2 - 1) % 5
                n1, n2 = matrix[n1_row][c1], matrix[n2_row][c2]
                rule = "Same Column"
                coords = [(r1, c1), (r2, c2), (n1_row, c1), (n2_row, c2)]
            else:
                n1, n2 = matrix[r1][c2], matrix[r2][c1]
                rule = "Rectangle"
                coords = [(r1, c1), (r2, c2), (r1, c2), (r2, c1)]
            
            result.append(n1 + n2)
            step_desc = f"{pair} -> {n1}{n2} ({rule})"
            self._add_step(step_desc)
            detailed_steps.append({
                "pair": pair,
                "result": n1 + n2,
                "rule": rule,
                "coords": coords
            })

        self._animation_data = {
            "matrix": matrix,
            "steps": detailed_steps
        }
        return "".join(result)
