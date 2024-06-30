#code by samarpan

import struct

# Constants 
A = 0x67452301
B = 0xefcdab89
C = 0x98badcfe
D = 0x10325476

def F(x, y, z):
    return (x & y) | (~x & z)

def G(x, y, z):
    return (x & y) | (x & z) | (y & z)

def H(x, y, z):
    return x ^ y ^ z


def left_rotate(x, n):
    x &= 0xFFFFFFFF
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

#transformation functions for furst,seconf and third round
def FF(a, b, c, d, x, s):
    return left_rotate(a + F(b, c, d) + x, s)

def GG(a, b, c, d, x, s):
    return left_rotate(a + G(b, c, d) + x + 0x5A827999, s)

def HH(a, b, c, d, x, s):
    return left_rotate(a + H(b, c, d) + x + 0x6ED9EBA1, s)


def md4(message):
    message = bytearray(message)  # Convert the message to a byte array
    original_length = (8 * len(message)) & 0xFFFFFFFFFFFFFFFF

    # Padding
    message.append(0x80)
    while (len(message) % 64) != 56:
        message.append(0)
    
    # Append original length as a 64-bit value
    message += struct.pack('<Q', original_length)

    # Process the message in 512-bit chunks
    def process_chunk(chunk):
        X = list(struct.unpack('<16I', chunk))
        a, b, c, d = A, B, C, D

        # Round 1
        a = FF(a, b, c, d, X[0], 3)
        d = FF(d, a, b, c, X[1], 7)
        c = FF(c, d, a, b, X[2], 11)
        b = FF(b, c, d, a, X[3], 19)
        a = FF(a, b, c, d, X[4], 3)
        d = FF(d, a, b, c, X[5], 7)
        c = FF(c, d, a, b, X[6], 11)
        b = FF(b, c, d, a, X[7], 19)
        a = FF(a, b, c, d, X[8], 3)
        d = FF(d, a, b, c, X[9], 7)
        c = FF(c, d, a, b, X[10], 11)
        b = FF(b, c, d, a, X[11], 19)
        a = FF(a, b, c, d, X[12], 3)
        d = FF(d, a, b, c, X[13], 7)
        c = FF(c, d, a, b, X[14], 11)
        b = FF(b, c, d, a, X[15], 19)

        # Round 2
        a = GG(a, b, c, d, X[0], 3)
        d = GG(d, a, b, c, X[4], 5)
        c = GG(c, d, a, b, X[8], 9)
        b = GG(b, c, d, a, X[12], 13)
        a = GG(a, b, c, d, X[1], 3)
        d = GG(d, a, b, c, X[5], 5)
        c = GG(c, d, a, b, X[9], 9)
        b = GG(b, c, d, a, X[13], 13)
        a = GG(a, b, c, d, X[2], 3)
        d = GG(d, a, b, c, X[6], 5)
        c = GG(c, d, a, b, X[10], 9)
        b = GG(b, c, d, a, X[14], 13)
        a = GG(a, b, c, d, X[3], 3)
        d = GG(d, a, b, c, X[7], 5)
        c = GG(c, d, a, b, X[11], 9)
        b = GG(b, c, d, a, X[15], 13)

        # Round 3
        a = HH(a, b, c, d, X[0], 3)
        d = HH(d, a, b, c, X[8], 9)
        c = HH(c, d, a, b, X[4], 11)
        b = HH(b, c, d, a, X[12], 15)
        a = HH(a, b, c, d, X[2], 3)
        d = HH(d, a, b, c, X[10], 9)
        c = HH(c, d, a, b, X[6], 11)
        b = HH(b, c, d, a, X[14], 15)
        a = HH(a, b, c, d, X[1], 3)
        d = HH(d, a, b, c, X[9], 9)
        c = HH(c, d, a, b, X[5], 11)
        b = HH(b, c, d, a, X[13], 15)
        a = HH(a, b, c, d, X[3], 3)
        d = HH(d, a, b, c, X[11], 9)
        c = HH(c, d, a, b, X[7], 11)
        b = HH(b, c, d, a, X[15], 15)

        # Add this chunk's hash to result so far
        return (
            (A + a) & 0xFFFFFFFF,
            (B + b) & 0xFFFFFFFF,
            (C + c) & 0xFFFFFFFF,
            (D + d) & 0xFFFFFFFF,
        )

    h0, h1, h2, h3 = A, B, C, D

    for i in range(0, len(message), 64):
        h0, h1, h2, h3 = process_chunk(message[i:i + 64])

    return struct.pack('<4I', h0, h1, h2, h3)

message = b"Hello, world!"
print(md4(message).hex())
