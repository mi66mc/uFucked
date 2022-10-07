import sys

def translate(code:str):
    translated = []
    unt = 0
    for i in code:
        if i == ">":
            unt += 1
        elif i == "+":
            try:
                translated.append(chr(unt))
                unt = 0
            except Exception as e:
                print(e)
        elif i == "=":
            for i in translated:
                print(i, end="")
        else: pass
    return translated

def execute(filename):
    f = open(filename, "r")
    translate(f.read())
    f.close()

def main():
    if len(sys.argv) == 2: execute(sys.argv[1])
    else: print("Please specify a filename.")

if __name__ == "__main__":
    main()