# This Python3 script takes UTF-8 encoded text files as input and writes out
# two files: (1) only English text (2) only non-English text

FILEIN = "/home/archjun/Downloads/EngKor.txt"
FILEOUTeng = "/home/archjun/Downloads/EngOnly.txt"
FILEOUTkor = "/home/archjun/Downloads/KorOnly.txt"
WHITELIST = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c“”'
ENGLISH = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

import doctest

def load_file():
    """
    Open textfile and append each line as a string inside a list
    """
    input_list = []
    with open(FILEIN, 'r') as infile:
        for line in infile:
            line = line.strip('\n')
            if line:
                input_list.append(line)
        return input_list

def winnowLos(los):
    """
    ListOfString -> ListOf(ListOfString)

    Given los where each list element is a long string containing spaces
    and multiple words, decompose each long string into a sublist of words.
    Returns a List of sublists of strings

    >>> winnowLos(['시간분리는 물리모순을 시간의 측면에서 독립적으로 바라보는 것이다.'])
    [['시간분리는', '물리모순을', '시간의', '측면에서', '독립적으로', '바라보는', '것이다.']]

    >>> winnowLos(['Who are you?', "I'm yomama"])
    [['Who', 'are', 'you?'], ["I'm", 'yomama']]
    """
    lolos = []
    for line in los:
        lolos.append(line.split())
    return lolos

def rmNonASCII(lol):
    """
    ListOf(ListOfString) -> ListOfString

    Given lolos where each element is a list of individual words,
    (1) check each word in each sublist for non-ASCII chars
    (2) if non-ASCII chars are detected, delete the word
    (3) append ASCII words to a new sublist
    (4) append ASCII-only sublists to a new list
    (5) return ASCII-only ListOf(ListOfStrings)

    >>> rmNonASCII([['ABC가나다', 'EFghijk라마바사'], ['ABC', 'def']])
    [[], ['ABC', 'def']]

    >>> rmNonASCII([['가나다!', '라마바사.', 'wow'], ['Can', 'you', 'hear', 'me?']])
    [['wow'], ['Can', 'you', 'hear', 'me?']]

    >>> rmNonASCII([['', 'F^K', '행복']])
    [['', 'F^K']]

    >>> rmNonASCII([['Once', 'upon'], ['행복', 'a', '“time”']])
    [['Once', 'upon'], ['a', '“time”']]

    """
    asciiLol = [] #ListOf(ListOfString) containing only ASCII words

    for sublist in lol:
        cleanLine = []
        for word in sublist:
            allASCII = True
            for char in word:
                if not char in WHITELIST:
                    allASCII = False
                    break
            if allASCII:
                cleanLine.append(word)
        asciiLol.append(cleanLine)

    return asciiLol

def rmEnglish(lol):
    """
    ListOf(ListOfString) -> ListOfString

    Given lolos where each element is a list of individual words,
    (1) check each word in each sublist for English chars
    (2) if English chars are detected, delete the word
    (3) append non-English words to a new sublist
    (4) append non-English-only sublists to a new list
    (5) return non-English-only ListOf(ListOfStrings)

    >>> rmEnglish([['ABC가나다', 'EFghijk라마바사'], ['가나다', '라마바']])
    [[], ['가나다', '라마바']]

    >>> rmEnglish([['가나다!', '라마바사.', 'wow'], ['Can', 'you', 'hear', 'me?']])
    [['가나다!', '라마바사.'], []]

    >>> rmEnglish([['', 'F^K', '행복']])
    [['', '행복']]

    >>> rmEnglish([['Once', 'upon'], ['행복한', '“인생”']])
    [[], ['행복한', '“인생”']]

    """
    nonEngLol = [] #ListOf(ListOfString) containing only non-ASCII words

    for sublist in lol:
        cleanLine = []
        for word in sublist:
            noEnglish = True
            for char in word:
                if char in ENGLISH:
                    noEnglish = False
                    break
            if noEnglish:
                cleanLine.append(word)
        nonEngLol.append(cleanLine)

    return nonEngLol


##MAIN PROGRAM##
doctest.testmod()

incoming = load_file()
process1 = winnowLos(incoming)
loASCII = rmNonASCII(process1)
loNonEnglish = rmEnglish(process1)

# write only ASCII text to FILEOUTeng
with open(FILEOUTeng, 'w') as outputF:
    for line in loASCII:
        outputF.write(" ".join(line) + '\n')

#write only non-ASCII text to FILEOUTkor
with open(FILEOUTkor, 'w') as outputF:
    for line in loNonEnglish:
        outputF.write(" ".join(line) + '\n')
