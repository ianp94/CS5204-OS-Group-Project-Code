from random import randint

def main(args):
    value = args.get("value", randint(0,100))
    print(value)
    return {"value": value}

