from bencode.exceptions import DecodeException


def decode(b):
    try:
        return decoding_functions[b[0]](b)
    except (IndexError, KeyError):
        raise DecodeException('Cannot decode value: invalid bencode provided.')


def decode_string(b):
    """
    Decode a bencode into a string.
    E.g.: If b == '4:test', the method should return 'test'. The number 4 represents the length of the string 'test'.
    E.g.: If b == '11:hello world', the method should return 'hello world'. The space is accounted for in the length.
    :param b: the bencoded string
    :return: the decoded string
    """
    try:
        colon_index = b.index(':')
        length = int(b[:colon_index])
    except ValueError:
        raise DecodeException('Cannot decode string: bencode must start with length of string, followed by a colon.')

    string = b[colon_index + 1:]
    if len(string) != length:
        raise DecodeException('Cannot decode string: invalid length for bencode.')

    return string


def decode_int(b):
    """
    Decode a bencode into an int.
    E.g.: If b == 'i12e', the method should return 12.
    E.g.: If b == 'i43278593753845734985724e', the method should return 43278593753845734985724.
    :param b: the bencoded string
    :return: the decoded number
    """
    try:
        if b[-1] != 'e':
            raise DecodeException('Cannot decode int: bencode does not end with \'e\'.')
        return int(b[1:-1])
    except (IndexError, ValueError):
        raise DecodeException('Cannot decode int: invalid bencode provided.')


def decode_list(b):
    pass


def decode_dictionary(b):
    pass


"""
Store references to the decoding functions.
If the bencoded string starts with a digit, it can (probably) be decoded into a string.
If the bencoded string starts with 'i', 'l', 'd', it can (probably) be decoded into an int, list, or dictionary, respectively.
"""
decoding_functions = {
    '0': decode_string,
    '1': decode_string,
    '2': decode_string,
    '3': decode_string,
    '4': decode_string,
    '5': decode_string,
    '6': decode_string,
    '7': decode_string,
    '8': decode_string,
    '9': decode_string,
    'i': decode_int,
    'l': decode_list,
    'd': decode_dictionary,
}


if __name__ == '__main__':
    print(decode('2:hi'))
