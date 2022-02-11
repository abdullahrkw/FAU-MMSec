from calendar import c
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class AES(object):
    def __init__(self, key=None, iv=None) -> None:
        self._key = os.urandom(32) #256 bits

    def encrypt(self, plaintext, associated_data):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self._key), modes.GCM(iv))
        enct = cipher.encryptor()
        enct.authenticate_additional_data(associated_data)
        ciphertext = enct.update(plaintext) + enct.finalize()
        return ciphertext, iv, enct.tag

    def decrypt(self, ciphertext, iv, associated_data, tag):
        cipher = Cipher(algorithms.AES(self._key), modes.GCM(iv, tag))
        dect = cipher.decryptor()
        dect.authenticate_additional_data(associated_data)
        return dect.update(ciphertext) + dect.finalize()

 
from PIL import Image
 
def genData(bytes):
        byte_list = list()
        for byte in bytes:
            byte_list.append(format(ord(byte), "08b"))
        print(byte_list)
        return byte_list
 
# update LSBs
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
    for i in range(lendata):
        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]
 
        # Pixel value should be made odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1
 
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
 
        # Eighth pixel of every set tells whether to stop ot read further.
        # 0 means keep reading; 1 means message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
 
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
 
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]
 
def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
 
    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
 
def encode(img, data):
    image = Image.open(img, 'r')
    newimg = image.copy()
    encode_enc(newimg, data)
 
    new_img_name = input("Enter the name of new image(with extension) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
    return new_img_name
 
def decode(img):
    image = Image.open(img, 'r')
 
    data = ''
    imgdata = iter(image.getdata())
 
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]
 
        # string of binary data
        binstr = ''
 
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
        
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data 

if __name__=="__main__":
    data = input("message: ")
    if (len(data) == 0):
        raise ValueError('message is empty')
    src_img = input("src image path: ")

    aes = AES()
    plaintext = bytes(data, "ascii")
    additional_data = b"addional data for GCM"
    print("Plaintext", plaintext)
    ciphertext, iv, tag = aes.encrypt(plaintext, additional_data)
    print(bytearray(ciphertext))
    print("Ciphertext", ciphertext)
    new_img = encode(src_img, data)
    dec_data = decode(new_img)
    print("Decode Ciphertext", dec_data)
    dectplaintext = aes.decrypt(ciphertext, iv, additional_data, tag)
    print("Decrypted plaintext", dectplaintext)


