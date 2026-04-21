import random
import os
import pyttsx3

# engine = pyttsx3.init()
# engine.setProperty('rate', 300)
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[24].id)


def parsePair(pair):
    LHS, RHS = "", ""
    parsing_LHS = True
    for c in pair:
        if c == "-":
            parsing_LHS = False
        elif parsing_LHS:
            LHS += c
        else:
            RHS += c
    return LHS[:-1], RHS[1:-1]


def parseFile(fn):
    f = open(fn, "r", encoding="utf-8").readlines()
    out = []
    for line in f:
        out.append(parsePair(line))
    return out


V = parseFile("sentences")
S = parseFile("nouns")
A = parseFile("adjectives")


def paintText(text, color):
    return "\033[" + str(color) + "m" + text + "\033[0m"


def unpaintText(text):
    remove = False
    out = ""
    for c in text:
        if c == "\033":
            remove = True
        if not remove:
            out += c
        elif c == "m":
            remove = False
    return out


artColor = 92
adjColor = 94
nounColor = 0
verbColor = 96
wrongColor = 91


def makeArticle(base, ending):
    if base == "d" and ending == "":
        return "der"
    if base == "d" and ending == "e":
        return "die"
    if base == "d" and ending == "es":
        return "das"
    if base == "ein" and ending == "es":
        return "ein"
    if base == "ein" and ending == "ie":
        return "eine"
    return base + ending


def declinateNoun(art, noun, case, indef):
    ending = ["", "e", "es"][art]
    if case == "A":
        if art == 0:
            ending = "en"
    elif case == "D":
        if art in [0, 2]:
            ending = "em"
        if art == 1:
            ending = "er"
    if indef:
        article = makeArticle("ein", ending)
    else:
        article = makeArticle("d", ending)
    return (article, noun)


def declinateAdj(art, adj, case, indef):
    if case == "D":
        return adj + "en"
    if case == "A" and art == 0:
        return adj + "en"
    if indef:
        return adj + ["er", "e", "es"][art]
    return adj + "e"


def declinateAdjNounPair(adj, noun, case, indef):
    cannonArt = {"r": 0, "e": 1, "s": 2}[noun[2]]
    art, noun = declinateNoun(cannonArt, noun[4:], case, indef)
    if adj == "":
        return art + " " + noun
    adj = declinateAdj(cannonArt, adj, case, indef)
    return art + " " + adj + " " + noun


def randomSentence():
    verb = random.choice(V)
    words = verb[1].split()
    eng_words = verb[0].split()
    out = ""
    eng_out = ""
    for w in words:
        if w in ["N", "D", "A"]:
            indef = random.getrandbits(1)
            addAdjective = random.getrandbits(1)
            chosenWord = random.choice(S)
            firstLetter = chosenWord[0][0]
            chosenAdjective = ("", "")
            if addAdjective:
                chosenAdjective = random.choice(A)
                firstLetter = chosenAdjective[0][0]
            out += declinateAdjNounPair(chosenAdjective[1], chosenWord[1], w, indef)
            out += " "
            if indef:
                if firstLetter in "aeiou":
                    eng_out += paintText("an ", artColor)
                else:
                    eng_out += paintText("a ", artColor)
            else:
                eng_out += paintText("the ", artColor)
            if addAdjective:
                eng_out += paintText(chosenAdjective[0], adjColor)
                eng_out += " "
            eng_out += paintText(chosenWord[0], nounColor)
            eng_out += " "
        else:
            out += w
            out += " "
            if len(eng_words):
                eng_out += paintText(eng_words[0], verbColor)
                eng_words = eng_words[1:]
                eng_out += " "
    return eng_out[:-1], out[:-1]


def printAndSay(text):
    print(text)
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[24].id)
    engine.say(unpaintText(text))
    engine.runAndWait()


ans = ""
os.system("clear")
while ans != "bye" and ans != "q":
    eng, de = randomSentence()
    done = False
    printAndSay(eng)
    while not done:
        ans = input()
        if ans in ["cl", "csl", "clear"]:
            os.system("clear")
            print(eng)
        else:
            if ans != de:
                print(paintText(de, wrongColor))
            done = True
            print()
# os.system("clear")
