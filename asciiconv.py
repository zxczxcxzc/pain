# Utility to convert text to pixels
# Usage: asciiconv.py [text]

import sys
from PIL import Image


if(len(sys.argv) < 2):
    print("Usage: asciiconv.py [text]")
    sys.exit()

st = ' '.join(sys.argv[1:])

binstr = []
for c in st:
    binstr.append(format(ord(c), 'b')[::-1])
print(' '.join(binstr))

im = Image.new("RGB", (7, len(binstr) * 2), (255, 255, 255))
x = 0
y = 0
for i in binstr:
    for c in i:
        if(c) == "1":
            im.putpixel((x, y), (0, 0, 0))
        x += 1
    x = 0
    im.putpixel((x, y + 1), (0, 255, 0))
    y += 2
im.save("text.png")