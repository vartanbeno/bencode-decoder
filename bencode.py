#!/usr/bin/env python3
import json

from bencode import decode, DecodeException


def print_decoded_bencode(b):
    try:
        # Using json dumps so that the OrderedDict is pretty printed
        print(json.dumps(decode(b)[0]))
    except DecodeException as e:
        print(e)


if __name__ == '__main__':

    while True:

        try:
            bencode = input('Enter a bencoded string that you wish to decode, or press enter to terminate the program.\n')
        except KeyboardInterrupt:
            break

        if not bencode:
            break
        else:
            print_decoded_bencode(bencode)
            print()
