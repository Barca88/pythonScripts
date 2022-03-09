import hashlib
from string import ascii_letters
from itertools import product
import datetime

if __name__ == "__main__":

    init = "Name:mail@mail.com:"
    encoded = init.encode()

    hash = hashlib.sha256(encoded).hexdigest()

    sizeKeywords = 1
    r = init
    print("Hash =", hash)
    print("R =", r)
    hash = hashlib.sha256(r.encode()).hexdigest()

    begin = datetime.datetime.now()
    end = datetime.datetime.now()

    print("Tempo=", begin - end)
    while not hash[0:7] == '0000000':
        for x in (''.join(i) for i in product(ascii_letters, repeat=sizeKeywords)):
            if hash[0:7] == '0000000':
                end = datetime.datetime.now()
                break
            r = init + x
            hash = hashlib.sha256(r.encode()).hexdigest()
            #if hash[0:5] == '00000':
            #    print("Temos 5 0's")
            #    print("String =", r)
            #    print("Hash =", hash)
        sizeKeywords += 1



    print("Temos 7 0's pow pow")
    print("Hash =", hash)
    print("r =", r)
    print("Tempo =", end-begin)