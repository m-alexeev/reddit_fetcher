def parseSymbolList():
    r = open("nasdaqtraded.txt", "r")
    w = open("symbols.txt", "w")
    r.readline()
    for line in r:
        data = line.split("|")
        symbol, name = data[1], data[2]
        w.write(symbol + "|"  + name +  "\n")
        
def getSymbolList():
    symbols = set()
    f = open("symbols.txt")
    for symbol in f:
        symbols.add(symbol)

    return symbols

parseSymbolList()