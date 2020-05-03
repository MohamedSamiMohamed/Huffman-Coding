text_file= open("string.txt", "r")
table=open("table.txt", "w")
decoded_file=open("decoded_file.txt", "w")
encoded_file=open("encoded_file.txt", "wb")

string = text_file.read()
encoded_string=""

class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)


def huffmanCodeTree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffmanCodeTree(l, True, binString + '0'))
    d.update(huffmanCodeTree(r, False, binString + '1'))
    return d


freq = {}
for c in string:
    if c in freq:
        freq[c] += 1
    else:
        freq[c] = 1

freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

nodes = freq

while len(nodes) > 1:
    (key1, c1) = nodes[-1]
    (key2, c2) = nodes[-2]
    nodes = nodes[:-2]
    node = NodeTree(key1, key2)
    nodes.append((node, c1 + c2))

    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

huffmanCode = huffmanCodeTree(nodes[0][0])
reverse_huffmanCode = {}
reverse_huffmanCode = dict([(value, key) for key, value in huffmanCode.items()])

for char in string :
    encoded_string+=huffmanCode[char]

extra_padding = 8 - len(encoded_string) % 8
for i in range(extra_padding):
    encoded_string+="0"
padded_info = "{0:08b}".format(extra_padding)
encoded_string = padded_info + encoded_string

encoded_byte_array=[]

for i in range(0, len(encoded_string), 8):
    byte=0
    for j in range(0,8):
        byte+= int (encoded_string[i+j]) * pow(2 , 7-j)
    encoded_byte_array.append(byte)


encoded = bytearray(encoded_byte_array)
encoded_file.write(encoded)

padded_info = encoded[0]
last_Byte = encoded[-1]
last_Byte=format(last_Byte, '08b')
pad = last_Byte[:-1*padded_info]
encoded_text = encoded[1:-1]


current_code = ""
decoded_text = ""
for bitaya in encoded_text:
    converted_bit =format(bitaya, '08b')
    for bit in converted_bit:
     current_code += bit
     if (current_code in reverse_huffmanCode):
        character = reverse_huffmanCode[current_code]
        decoded_text += character
        current_code = ""
for an in pad:
    current_code += an
    if (current_code in reverse_huffmanCode):
        character = reverse_huffmanCode[current_code]
        decoded_text += character
        current_code = ""

print(decoded_text)
decoded_file.write(decoded_text)
table.write(str(reverse_huffmanCode))

