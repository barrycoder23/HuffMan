import threading
import sys


alfabeto = {" ": "0000000", "!": "0000001", "\"": "0000010", "#": "0000011", "$": "0000100", "%": "0000101", "&": "0000110", "'": "0000111", "(": "0001000", ")": "0001001", "*": "0001010", "+": "0001011", ",": "0001100", "-": "0001101", ".": "0001110", "/": "0001111", "0": "0010000", "1": "0010001", "2": "0010010", "3": "0010011", "4": "0010100", "5": "0010101", "6": "0010110", "7": "0010111", "8": "0011000", "9": "0011001", ":": "0011010", ";": "0011011", "<": "0011100", "=": "0011101", ">": "0011110", "?": "0011111", "@": "0100000", "A": "0100001", "B": "0100010", "C": "0100011", "D": "0100100", "E": "0100101", "F": "0100110", "G": "0100111", "H": "0101000", "I": "0101001", "J": "0101010", "K": "0101011", "L": "0101100", "M": "0101101", "N": "0101110", "O": "0101111", "P": "0110000", "Q": "0110001", "R": "0110010", "S": "0110011", "T": "0110100",
            "U": "0110101", "V": "0110110", "W": "0110111", "X": "0111000", "Y": "0111001", "Z": "0111010", "[": "0111011", "\\": "0111100", "]": "0111101", "^": "0111110", "_": "0111111", "`": "1000000", "a": "1000001", "b": "1000010", "c": "1000011", "d": "1000100", "e": "1000101", "f": "1000110", "g": "1000111", "h": "1001000", "i": "1001001", "j": "1001010", "k": "1001011", "l": "1001100", "m": "1001101", "n": "1001110", "o": "1001111", "p": "1010000", "q": "1010001", "r": "1010010", "s": "1010011", "t": "1010100", "u": "101010", "v": "101011", "w": "101100", "x": "101101", "y": "101110", "z": "101111", "{": "110000", "|": "110001", "}": "110010", "~": "110011", "Á": "110100", "É": "110101", "Í": "110110", "Ó": "110111", "Ú": "111000", "Ñ": "111001", "á": "111010", "é": "111011", "í": "111100", "ó": "111101", "ú": "111110", "ñ": "111111"}
codes, sort, freq = {}, {}, {}
string = ""
aux=0
id=0

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter

   def run(self):
    global string
    global id
    id+=1
    localId=id
    i=0
    currString=""
    while i<aux:
        currString=currString+string[i]
        i+=1
    if len(string)>aux:
      string=string[aux:]
    else:
        currString=currString+string

    print ("Starting " + self.name)
    executer(currString, localId)
    print ("Exiting " + self.name)


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
            print(f'Simbolo no perteneciente al alfabeto:' + ch)
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


def codeHuff(node, val=''):
    newVal = val + str(node.code)
    if (node.left):
        codeHuff(node.left, newVal)
    if (node.right):
        codeHuff(node.right, newVal)
    if (not node.left and not node.right):
        codes[node.data] = newVal
    return codes

def huffman(sort):
    global string
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


def executer(currString, id):
    freq = decodeString(currString)
    sort = sortCaracteres(freq)
    nodes, huffman_encoding = huffman(sort)
    message = f"""
    \tstring: {currString}
    \tfreq: {freq}
    \tsorted: {sort}
    \thuffman: {huffman_encoding}
    \t---------------------
    """

    saveResult(message, huffman_encoding, currString, id)

    
# Método para imprimir como es solicitado
def saveResult(message, huffman_encoding, currString, id):
    global string
    n = 2*len(alfabeto)
    for letra in freq.keys():
        items = []
        n -= 1
        items.append(letra)
        items.append(freq[letra])
        items.append(n)
        message += f"\t{items}\n"


    with open(f'texto{id}.BIN', 'w') as f:
        f.write(outputFile(currString, huffman_encoding))

    id+=1



def main():
    global string
    global aux
    fileToComp=sys.argv[1]
    with open(fileToComp, "r", encoding="utf8") as file: #Solo lectura, se cierra luego de leer
        auxStr = file.readlines()

    string=auxStr[0]

    numberOfThreads = int(sys.argv[2])

    if numberOfThreads < 4:
        print("El numero minimo de hilos es 4")
        exit(0)

    possibleChar(string)
    aux=int(len(string)/numberOfThreads)
    i=0
    while i<numberOfThreads:
        j=i+1
        thread = myThread(j, f"Thread-{j}", j)
        thread.start()
        i+=1


main()