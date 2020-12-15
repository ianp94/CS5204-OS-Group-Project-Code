def main(args):
    value = args.get("value", False)
    message = "your number is Below 70: " + str(value) + "!"
    return { "message" : message }
