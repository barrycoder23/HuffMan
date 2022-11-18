import csv

codes, huffman_encoding, sort, freq = {}, {}, {}, {}
string = ""

# alfabeto = ['!', '\"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
#            'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'Á', 'É', 'Í', 'Ó', 'Ú', 'Ñ', 'á', 'é', 'í', 'ó', 'ú', 'ñ', ' ']

alfabeto = {" ": "0000000", "!": "0000001", "\"": "0000010", "#": "0000011", "$": "0000100", "%": "0000101", "&": "0000110", "'": "0000111", "(": "0001000", ")": "0001001", "*": "0001010", "+": "0001011", ",": "0001100", "-": "0001101", ".": "0001110", "/": "0001111", "0": "0010000", "1": "0010001", "2": "0010010", "3": "0010011", "4": "0010100", "5": "0010101", "6": "0010110", "7": "0010111", "8": "0011000", "9": "0011001", ":": "0011010", ";": "0011011", "<": "0011100", "=": "0011101", ">": "0011110", "?": "0011111", "@": "0100000", "A": "0100001", "B": "0100010", "C": "0100011", "D": "0100100", "E": "0100101", "F": "0100110", "G": "0100111", "H": "0101000", "I": "0101001", "J": "0101010", "K": "0101011", "L": "0101100", "M": "0101101", "N": "0101110", "O": "0101111", "P": "0110000", "Q": "0110001", "R": "0110010", "S": "0110011", "T": "0110100",
            "U": "0110101", "V": "0110110", "W": "0110111", "X": "0111000", "Y": "0111001", "Z": "0111010", "[": "0111011", "\\": "0111100", "]": "0111101", "^": "0111110", "_": "0111111", "`": "1000000", "a": "1000001", "b": "1000010", "c": "1000011", "d": "1000100", "e": "1000101", "f": "1000110", "g": "1000111", "h": "1001000", "i": "1001001", "j": "1001010", "k": "1001011", "l": "1001100", "m": "1001101", "n": "1001110", "o": "1001111", "p": "1010000", "q": "1010001", "r": "1010010", "s": "1010011", "t": "1010100", "u": "101010", "v": "101011", "w": "101100", "x": "101101", "y": "101110", "z": "101111", "{": "110000", "|": "110001", "}": "110010", "~": "110011", "Á": "110100", "É": "110101", "Í": "110110", "Ó": "110111", "Ú": "111000", "Ñ": "111001", "á": "111010", "é": "111011", "í": "111100", "ó": "111101", "ú": "111110", "ñ": "111111"}

class Node:
    def __init__(self, prob, data, left = None, right = None):
        self.left = left
        self.right = right
        self.prob = prob
        self.data = data
        self.code = ''

# ----------------Clase wordProcessing----------------
def possibleChar(palabra):
    text = palabra
    for ch in text:
        if ch not in alfabeto:
            print(f'Simbolo no perteneciente al alfabeto')
            exit(0)

# Método que cuenta la frecuencia que tiene un caracter dentro del string dado
def decodeString(str):
    caracteres = {}
    for i in str:
        if caracteres.get(i) == None:
            caracteres[i] = 1
        else:
            caracteres[i] += 1
    return caracteres

def sortCaracteres(dicc):
    return dict(sorted(dicc.items(), key=lambda x: x[1]))


# ----------------Clase runTree----------------
# Función que saca la salida pero codificada
def outputEnc(data, coding):
    encoding_output = []
    for c in data:
        encoding_output.append(coding[c])
    string = ''.join([str(item) for item in encoding_output])
    return string

# Calcula los bits que se redujeron con huff
def sizeReduced(data, coding):
    antes = len(data) * 8
    despues = 0
    symbols = coding.keys()
    for s in symbols:
        count = data.count(s)
        despues += count * len(coding[s])
    print("--------Bits size--------")
    print(f"Antes (bits): {antes}")
    print(f"Después (bits): {despues}")

def huffDecode(encData, huffTree):
    treeHead = huffTree
    decoded_output = []
    for x in encData:
        if x == '1':
            huffTree = huffTree.right
        elif x == '0':
            huffTree = huffTree.left
        try:
            if huffTree.left.data == None and huffTree.right.data == None:
                pass
        except AttributeError:
            decoded_output.append(huffTree.data)
            huffTree = treeHead
    string = ''.join([str(item) for item in decoded_output])
    return string

def codeHuff(node, val=''):
    newVal = val + str(node.code)
    if (node.left):
        codeHuff(node.left, newVal)
    if (node.right):
        codeHuff(node.right, newVal)
    if (not node.left and not node.right):
        codes[node.data] = newVal
    return codes

def huffman():
    caracter = sort.keys()
    valores = sort.values()
    nodes = []
    # creando nodos a partir de los caracteres del string
    for i in caracter:
        nodes.append(Node(sort.get(i), i))
    #print(nodes[3].data)
    #print(type(nodes))
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.prob)

        right = nodes[0]
        left = nodes[1]
        left.code = 1
        right.code = 0
        newNode = Node(left.prob + right.prob, left.data+right.data, left, right)
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)
    huffman_encoding = codeHuff(nodes[0])
    sizeReduced(string, huffman_encoding)
    return nodes[0], huffman_encoding

def outputFile(data, huff):
    string = data
    file = ""
    lst = [x for x in string]
    for item in lst:
        # file <- alfabeto[item]:(La letra pero en binario)
        file += alfabeto[item] + huff[item]
    return file

#string = 'ABBACABBCD'
string = input("Ingrese el string: ")

# Verifica que no hayan caracteres extran~os 
possibleChar(string)

freq = decodeString(string)
sort = sortCaracteres(freq)
nodes, huffman_encoding = huffman()
message = f"""
\tstring: {string}
\tfreq: {freq}
\tsorted: {sort}
\thuffman: {huffman_encoding}
\t---------------------
"""
""" h = huffDecode(huffman_encoding, nodes)
print(f"Huff {h}") """

asd = outputEnc(string, huffman_encoding)
print(f"Encoded {asd}")
# Método para imprimir como es solicitado
n = 2*len(alfabeto)
for letra in freq.keys():
    items = []
    n -= 1
    items.append(letra)
    items.append(freq[letra])
    items.append(n)
    message += f"\t{items}\n"
#freq[letra] = items

print(message)

print(f"binarioFile: {outputFile(string, huffman_encoding)}")

#with open("texto", w):
input("Presione enter para continuar.....")

#print(f'freq: {freq}')
