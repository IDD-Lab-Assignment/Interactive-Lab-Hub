import os

# play intro message
os.system('sh intro.sh')

while True:
    os.system('sh askColor.sh')
    f = open("response.txt", "r")
    response = f.read()

    # if the user wants to learn a color
    if response == "red":
        os.system('sh red.sh')
    elif response == "blue":
        os.system('sh blue.sh')
    elif response == "orange":
        os.system('sh orange.sh')
    elif response == "green":
        os.system('sh green.sh')
    elif response == "yellow":
        os.system('sh yellow.sh')
    f = open("response.txt", "r")
    response = f.read()
    if response == "yes":
        os.system('sh feel.sh')
        break
    elif response == "no":
        os.system('anotherColor.sh')
        # if the user wants to learn a color
        if response == "red":
            os.system('sh red.sh')
        elif response == "blue":
            os.system('sh blue.sh')
        elif response == "orange":
            os.system('sh orange.sh')
        elif response == "green":
            os.system('sh green.sh')
        elif response == "yellow":
            os.system('sh yellow.sh')
        f = open("response.txt", "r")
        response = f.read()
        if response == "yes":
            os.system('sh feel.sh')
            break
        else:
            break
