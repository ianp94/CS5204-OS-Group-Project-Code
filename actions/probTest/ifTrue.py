def main(args):
    value = args.get("value", True)
    message = "your number is above 70: " + str(value) + "!"
    return { "message" : message }
