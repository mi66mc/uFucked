def translate(t:str):
    translated = ""
    for i in t:
        n = ord(i)
        for i in range(0,n):
            translated += ">"
        translated += "+"
    translated += "="
    return translated

if __name__ == "__main__":
    print(translate(input("Translate: ")))