from database import Database
import sys 


def uploadSymbols():
    db = Database()
    connection = db.getConnection()

    cursor = connection.cursor()


    query = "INSERT INTO symbols(symbol, name) VALUES (%s, %s)"
    vals = []
    f = open("symbols.txt", "r")
    for line in f:
        symbol, text = line.split("|")
        vals.append((symbol, text))
        
    cursor.executemany(query, vals)
    connection.commit()

    print("Symbols uploaded")

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



if __name__ == "__main__":
    arg = sys.argv[1:]
    if (arg[0] == "--parse"):
        parseSymbolList()
    elif (arg[0] == "--get"):
        getSymbolList()
    elif (arg[0] == "--push"):
        uploadSymbols()
    else:
        print("Unknown command")