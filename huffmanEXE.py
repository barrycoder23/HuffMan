
codes, huffman_encoding, sort, freq = {}, {}, {}, {}
string = ""

alfabeto = ['!', '\"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'Á', 'É', 'Í', 'Ó', 'Ú', 'Ñ', 'á', 'é', 'í', 'ó', 'ú', 'ñ', ' ']

class Node:
    def __init__(self, prob, data, left = None, right = None):
        self.left = left
        self.right = right
        self.prob = prob
        self.data = data
        self.code = ''

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
    return nodes[0], huffman_encoding


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

input("Presione enter para continuar.....")

#print(f'freq: {freq}')
