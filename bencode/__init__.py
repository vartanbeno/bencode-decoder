from collections import OrderedDict

from bencode.exceptions import DecodeException


def decode(b, start_index=0):
    try:
        return decoding_functions[b[0]](b, start_index)
    except (IndexError, KeyError):
        raise DecodeException('Cannot decode value: invalid bencode provided.')


def decode_string(b, start_index=0):
    """
    Decode a bencode into a string.
    E.g.: If b == '4:test', the method should return 'test'. The number 4 represents the length of the string 'test'.
    E.g.: If b == '11:hello world', the method should return 'hello world'. The space is accounted for in the length.
    :param b: the bencoded string
    :param start_index: the index from which we will start looking the colon (':') in the string
    :return: the decoded string, new start_index
    """
    try:
        colon_index = b.index(':', start_index)
        length = int(b[start_index:colon_index])
    except ValueError:
        raise DecodeException('Cannot decode string: bencode must start with length of string, followed by a colon.')

    string = b[colon_index + 1:colon_index + 1 + length]
    if len(string) != length:
        raise DecodeException('Cannot decode string: invalid length for bencode.')

    return string, colon_index + len(string) + 1


def decode_int(b, start_index=0):
    """
    Decode a bencode into an int.
    E.g.: If b == 'i12e', the method should return 12.
    E.g.: If b == 'i-12e', the method should return -12.
    :param b: the bencoded string
    :param start_index: the index from which we will start looking the 'e' in the string
    :return: the decoded number, new start_index
    """
    try:
        e_index = b.index('e', start_index)
        string = b[start_index + 1:e_index]

        # Negative 0 not allowed.
        # No leading zeroes, e.g. 007 is not allowed, it should be 7 instead.
        # Zero is just 0, not 00, not 000, etc.
        if len(string) > 1 and (string[0:2] == '-0' or (string[0] == '0' and string[1] != 'e')):
            raise ValueError

        return int(string), e_index + 1
    except (IndexError, ValueError):
        raise DecodeException('Cannot decode int: invalid bencode provided.')


def decode_list(b, start_index=0):
    """
    Decode a bencode into a list.
    E.g.: If b == 'le', the method should return [].
    E.g.: If b == 'li12ee', the method should return [12].
    E.g.: If b == 'li12e4:i12e4:testlleee', the method should return [12, 'i12e', 'test', [[]]].
    :param b: the bencoded string
    :param start_index: the index at which we will check if the corresponding character is 'e'.
    :return: the decoded list, new start_index
    """
    decoded_list = []
    start_index += 1
    try:
        while b[start_index] != 'e':
            content, start_index = decoding_functions[b[start_index]](b, start_index)
            decoded_list.append(content)
        return decoded_list, start_index + 1
    except (IndexError, ValueError):
        raise DecodeException('Cannot decode int: invalid bencode provided.')


def decode_dictionary(b, start_index=0):
    """
    Decode a bencode into a dictionary.
    E.g.: If b == 'de', the method should return an empty OrderedDict.
    E.g.: If b == 'd4:test4:teste', the method should return an OrderedDict with k: 'test' => v: 'test'.
    The dictionary is ordered alphabetically by key.
    E.g.: If b == 'd4:test4:test1:a1:ae', the method should return an OrderedDict with k: 'a' => v: 'a', k: 'test' => v: 'test'.
    :param b: the bencoded string
    :param start_index: the index at which we will check if the corresponding character is 'e'.
    :return: the decoded dictionary, new start_index
    """
    decoded_dictionary = OrderedDict()
    start_index += 1
    try:
        while b[start_index] != 'e':
            key, start_index = decoding_functions[b[start_index]](b, start_index)
            if not isinstance(key, str):
                raise DecodeException('Dictionary keys must be strings.')
            decoded_dictionary[key], start_index = decoding_functions[b[start_index]](b, start_index)

        # All keys must appear in lexicographical order, i.e. alphabetical order
        return OrderedDict(sorted(decoded_dictionary.items())), start_index + 1
    except (IndexError, ValueError):
        raise DecodeException('Cannot decode int: invalid bencode provided.')


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
    print(decode('2:hi')[0])
    print(decode('li12ei12e4:i12e4:test4:test8:hi worldllllleleeeeee')[0])
    print(decode('d4:test4:test1:a1:b3:fooi12e1:cd4:test4:testee')[0])
