# Advanced Classical Cipher Suite: A Visualization Tool for Cryptography

## 📘 Project Overview

The **Advanced Classical Cipher Suite** is an interactive graphical user interface (GUI) application designed to visualize the **encryption and decryption processes** of classical cryptographic algorithms. Built with **Python and Tkinter**, this tool serves as an educational platform for students, educators, and cybersecurity enthusiasts to understand cryptography through **dynamic animations** and **step-by-step transformation logs**.

The application currently supports the following classical ciphers:

* **Caesar Cipher**
* **Vigenère Cipher**
* **Playfair Cipher**

---

## ✨ Features

* **Interactive Cipher Selection**
  Easily switch between Caesar, Vigenère, and Playfair ciphers.

* **Encryption & Decryption Modes**
  Perform both encryption and decryption operations.

* **Dynamic Animation**
  Step-by-step visual representation of character transformations.

* **Adjustable Animation Speed**
  Control visualization speed for detailed learning.

* **Real-time Transformation Log**
  Displays each transformation step during cryptographic operations.

* **Modern Dark-Themed UI**
  Designed for clarity, readability, and extended usage.

* **Robust Error Handling**
  Gracefully handles invalid inputs and incorrect keys.

---

## 🏗️ System Architecture

The application follows a **modular and object-oriented design**, separating cryptographic logic from the graphical interface.

| Component            | Technology / Concept         | Description                                                   |
| -------------------- | ---------------------------- | ------------------------------------------------------------- |
| Programming Language | Python 3.11                  | Core application logic and framework                          |
| GUI Framework        | Tkinter                      | Manages UI elements and user interaction                      |
| Cipher Logic         | Abstract Base Class (Cipher) | Ensures consistent interface and extensibility                |
| Animation Engine     | `Tkinter.after()`            | Handles smooth, non-blocking animations                       |
| File Structure       | `main_gui.py`, `logic/`      | UI logic in `main_gui.py`, cipher implementations in `logic/` |

---

## ⚙️ Installation & Setup

### Prerequisites

* Python **3.x** (Recommended: Python 3.11)

### Step 1: Clone or Extract the Project

```bash
# Clone from repository
git clone https://github.com/your-username/cybersecurity-cipher-suite.git
cd cybersecurity-cipher-suite
```

Alternatively, extract the provided **.rar file** into your desired directory.

---

### Step 2: Navigate to Project Directory

```bash
cd "Cyber Security Project"
```

---

### Step 3: Run the Application

```bash
python3 run.py
```

This will launch the GUI application.

---

## 🧭 Usage Guide

1. **Select a Cipher**
   Choose Caesar, Vigenère, or Playfair from the sidebar.

2. **Select Mode**
   Choose either **Encrypt** or **Decrypt**.

3. **Enter Input Text**
   Type the message you want to process.

4. **Enter Key**

   * Caesar: Integer shift value
   * Vigenère / Playfair: Alphabetic keyword

5. **Adjust Animation Speed**
   Use the slider to control visualization speed.

6. **Start Animation**
   Click **START ANIMATION** to begin.

7. **Pause / Resume**
   Temporarily halt the animation to inspect transformations.

8. **Reset**
   Clears all fields and resets the visualization.

---

## 🔐 Cipher Details

### Caesar Cipher

A substitution cipher where each letter in the plaintext is shifted by a fixed number of positions in the alphabet. The key is an integer representing the shift value.

---

### Vigenère Cipher

A polyalphabetic substitution cipher that uses a keyword to apply multiple Caesar shifts, enhancing security over monoalphabetic ciphers.

---

### Playfair Cipher

A digraph substitution cipher that encrypts pairs of letters using a **5×5 key matrix** generated from a keyword. It was the first practical digraph cipher.

---

## 🧪 Testing

The project includes a **`test_logic.py`** file containing unit tests to verify encryption and decryption correctness across all supported ciphers.

### Run Tests

```bash
python3 test_logic.py
```

---

## 🚀 Future Enhancements

* Integration of **cryptanalysis tools** (e.g., frequency analysis, Kasiski examination)
* Support for additional classical ciphers (Hill Cipher, Enigma)
* Export functionality for transformation logs
* Multi-language and extended character set support

---

## 👤 Author

**Manus AI**

---

## 📄 License

This project is **open-source** and available under the **MIT License**.
See the `LICENSE` file for more details.

---

> *An educational visualization tool to bridge theory and practice in classical cryptography.*
