# xor-decrypt
A XOR encrypted files decryptor

python xordecrypt.py -h

- -e : file to decrypt

- -d : file to save the decrypted content

- -l : key's lenght to guess
- -k : key to decrypt (of you already know it)

Example:

python xordecrypt.py -e "tests_files\PA.txt" -d PA_decrypt.txt -l 6
