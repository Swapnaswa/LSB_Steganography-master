from PIL import Image
from colorama import Fore, Back, Style
import math
import os
import docopt

ENDING_CHARACTER = "11111111"

def to_bits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def xor_bit(a,b):
    return a^b

def get_lsb(byte):
    return byte[-1]

def get_binary(number):
    return bin(number)[2:].zfill(8)

def binary_to_decimal(binary):
    return int(binary, 2)

def ascii_to_char(number):
    return chr(number)

def char_to_ascii(character):
    return ord(character)

def get_bits_list(text,key):
    bit_list = []
    for character in text:
        ascii_representation = char_to_ascii(character)
        binary_representation = get_binary(ascii_representation)
        for bit in binary_representation:
            bit_list.append(bit)
    for bit in key:
        bit_list.append(bit)
    return bit_list

def change_last_bit(byte, new_bit):
    return byte[:-1] + str(new_bit)

def modify_color(original_color, bit):
    binary_color = get_binary(original_color)
    modified_color = change_last_bit(binary_color, bit)
    return binary_to_decimal(modified_color)


def hide_text(message, original_image_path, output_image_path,key):
    print("Hiding message...".format(message))
    image = Image.open(original_image_path)
    pixels = image.load()

    size = image.size
    width = size[0]
    height = size[1]

    bit_list = get_bits_list(message,key)
    counter = 0
    length = len(bit_list)
    for x in range(width):
        for y in range(height):
            if counter < length:
                pixel = pixels[x, y]

                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]

                if counter < length:
                    modified_red = modify_color(red, bit_list[counter])
                    counter += 1
                else:
                    modified_red = red

                if counter < length:
                    modified_green = modify_color(green, bit_list[counter])
                    counter += 1
                else:
                    modified_green = green

                if counter < length:
                    modified_blue = modify_color(blue, bit_list[counter])
                    counter += 1
                else:
                    modified_blue = blue

                pixels[x, y] = (
                    modified_red, modified_green, modified_blue)
            else:
                break
        else:
            continue
        break

    if counter >= length:
        print(Fore.GREEN + "Message hidden successfully")
    else:
        print(Fore.RED + "Warning: couldn't write the entire message, {} characters left".format(
            math.floor((length - counter) / 8)))

    print("")
    print(Style.RESET_ALL)
    image.save(output_image_path)

def show_text(image_path,key):
    image = Image.open(image_path)
    pixels = image.load()

    size = image.size
    width = size[0]
    height = size[1]

    byte = ""
    message = ""

    for x in range(width):
        for y in range(height):
            pixel = pixels[x, y]

            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]

            byte += get_lsb(get_binary(red))
            if len(byte) >= 8:
                if byte == key:
                    break
                message += ascii_to_char(
                    binary_to_decimal(byte))
                byte = ""

            byte += get_lsb(get_binary(green))
            if len(byte) >= 8:
                if byte == key:
                    break
                message += ascii_to_char(
                    binary_to_decimal(byte))
                byte = ""

            byte += get_lsb(get_binary(blue))
            if len(byte) >= 8:
                if byte == key:
                    break
                message += ascii_to_char(
                    binary_to_decimal(byte))
                byte = ""

        else:
            continue
        break
    return message

def ask_number():
    correct = False
    num = 0
    while(not correct):
        try:
            num = int(input("Enter an integer: "))
            correct = True
        except ValueError:
            print(Fore.RED + "Error, enter an integer")
        print(Style.RESET_ALL)
    return num

def get_extension(name):
    extension = ".png"
    sep = '.'
    rest = name.split(sep)
    return rest[0]+extension


def main():
    exit_program = False
    option = 0
    text = ""
    path = ""
    while not exit_program:
        imagen = ""
        text = ""
        print(Fore.BLUE + "- LSB - Steganography -")

        print(Style.RESET_ALL)
        print("1. Hide message")
        print("2. Read message")
        print("3. Exit")
        print("")

        option = ask_number()
        if option == 1:
            key = ENDING_CHARACTER
            text = input("Text to hide: ")
            imagen = input("Enter the image name with extension: ")
            imagen_salida = extension(input("Enter the output image name: "))
            new_key = to_bits(input("Key: "))
            key = xor_bit(int(ENDING_CHARACTER), new_key[0])
            #key = ''.join(str(x) for x in new_key)
            print(key)
            #path = path + "\\" + imagen
            #imagen_salida = "hide"+imagen
            hide_text(text, imagen, output_image, key)
        elif option == 2:
            key = ENDING_CHARACTER
            new_key = to_bits(input("Key: "))
            #key = ''.join(str(x) for x in new_key)
            image = extension(input("Enter the image name with extension: "))
            print("")
            #path = path + "\\" + imagen
            message = show_text(image, key)
            if message != "":
                print("The hidden message is:")
                print(Fore.GREEN + message)
            else:
                print(Fore.RED + "There is no hidden message")
            print(Style.RESET_ALL)
        elif option == 3:
            exit_program = True
        else:
            print("Enter a number between 1 and 3")

if __name__ == "__main__":
    main()
