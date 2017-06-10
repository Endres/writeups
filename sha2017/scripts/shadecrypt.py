#!/bin/env python3
from PIL import Image
import sys, os

# usage: ./shadecrypt.py <path/to/image.png|http[s]://example.com/image.png>
# example: ./shadecrypt.py https://cryptoengine.stillhackinganyway.nl/flag

# This first part of the script is just loading the image, scanning through the
# colored blocks in the image, and asking the user for any further text which
# can be read (sorry, OCR was a bit too complicated for that...)
# If you're only interested in the crypto and not in the encoding of the data
# please skip to line 58 and following

if len(sys.argv) < 2:
	print("error: please supply image file path!")
	sys.exit(1)

fname = " ".join(sys.argv[1:])

if fname.startswith("http://") or fname.startswith("https://"):
	import requests
	from io import BytesIO
	f = requests.get(fname)
	file = BytesIO(f.content)
else:
	file = fname

img = Image.open(file)
width = int(img.size[0] / 40)
if width == 0:
	print("error: image too small")
	sys.exit(1)

if width < 2:
	img.show()
else:
	textpart = img.crop(((width - 2) * 40, 0, width * 40, img.size[1]))
	textpart.show()

s = input("please enter the text you see in the image (if any): ")

if s != "" and ((len(s) != 2 and len(s) != 4) or int(s, 16) == None):
	print("error: only supply max. two pairs of hex characters!")
	sys.exit(1)

os.system("killall display") # can be omitted if not ran under linux...

pix = img.load()
code = []
for x in range(int(img.size[0] / 40)):
	c = pix[20+40*x,35]
	for i in range(3):
		code.append(c[i])

for x in range(int(len(s) / 2)):
	code.append(int(s[x*2:x*2+2], 16))

# now the actual decrypt of "code" starts
# simple XOR cipher with blocklength of 4, using the IV "2017" (initialization
# vector. the state with which the ciphertext is XOR-en-/decrypted is
# initialized with the IV, and updates every block with the XOR of decrypted
# characters (inverted CBC mode to say)
iv = "2017"
s = [ord(c) for c in iv]
plaintext = ""

for i in range(len(code)):
	c = code[i] ^ s[i % len(s)]
	s[i % len(s)] = code[i] # this actually equals s[i % 4] = s[i % 4] ^ c
	plaintext = plaintext + chr(c)
print(plaintext)