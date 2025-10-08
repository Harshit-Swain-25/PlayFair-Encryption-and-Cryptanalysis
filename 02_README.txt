Playfair Cipher Encryption and Cryptanalysis
--------------------------------------------

Overview:
This project demonstrates securing messages using the Playfair Cipher encryption method 
and developing a simple cryptanalysis technique to recover the original message. 
It includes encryption, decryption, frequency analysis, and brute-force key testing.

Files:
- 01_playfair.py   : Main Python script for encryption, decryption, and analysis.
- 02_README.txt    : Project description file.

How to Run:
1. Open a terminal in this folder.
2. Run the script:
       python3 01_playfair.py
3. The program will:
   - Encrypt and decrypt a sample message.
   - Display key matrices (row-wise and column-wise).
   - Show a digraph frequency comparison chart.
   - Attempt brute-force decryption with sample keys.

Default Example:
   Secret Key : PLAYFAIR EXAMPLE
   Message    : Hide the gold in the tree stump

Output:
   - Row-wise Ciphertext
   - Column-wise Ciphertext
   - Decrypted Messages
   - Frequency Analysis Plot
   - Brute-force Cryptanalysis Results

Notes:
- 'J' is replaced with 'I' in the Playfair cipher (standard rule).
- You can modify the 'secret' and 'message' variables in the code to test your own text.
- The brute-force attack checks for common English patterns to guess possible keys.

Purpose:
This project is created for the Cryptography and Network Security (CNS) course.
It demonstrates classical cipher implementation and basic cryptanalysis concepts.
