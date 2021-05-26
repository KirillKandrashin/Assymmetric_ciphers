class Encryption:

    def __init__(self):
        pass

    def Enc(self, text, key):  # encryption from txt to byte
        return "".join([chr(ord(text[i]) ^ key) for i in range(len(text))])
