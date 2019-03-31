# Bencode Decoder

Python library used to decode bencoded strings.

More info about bencode can be found [here](https://en.wikipedia.org/wiki/Bencode).

## Getting Started

### Prerequisites

The program solely uses libraries found in the [Python Standard Library](https://docs.python.org/3/library/). The ones used are:

- `collections` to make use of the `OrderedDict` class, with which we can sort dictionary keys.
- `json` to neatly dump outputted results with the `dumps()` method (useful for dumping `OrderedDict`).
- `unittest` for tests.

### Running

To use the program, run `python3 bencode.py` or simply `./bencode.py`. If the latter is used, make sure the script is executable.

This launches a script that accepts user input, and decodes the string provided. You can always end the program by inputting an empty string (i.e. pressing `Enter`).

```
./bencode.py

Enter a bencoded string that you wish to decode, or press enter to terminate the program.
i12e
12

Enter a bencoded string that you wish to decode, or press enter to terminate the program.
11:hello world
"hello world"

Enter a bencoded string that you wish to decode, or press enter to terminate the program.
li12e4:i12eleli1e4:testee
[12, "i12e", [], [1, "test"]]

Enter a bencoded string that you wish to decode, or press enter to terminate the program.
d1:b1:b1:a1:a4:testd6:nested4:dictee
{"a": "a", "b": "b", "test": {"nested": "dict"}}        # Keys are sorted alphabetically
```

## Authors

- **Vartan Benohanian** - *ID:* 27492049

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
