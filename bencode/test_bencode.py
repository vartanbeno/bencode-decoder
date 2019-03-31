from collections import OrderedDict
from unittest import TestCase, main

from bencode import decode, DecodeException


class TestBencode(TestCase):

    def test_decode_string_success(self):
        foo, _ = decode('4:test')
        self.assertEqual(foo, 'test')

        foo, _ = decode('11:hello world')
        self.assertEqual(foo, 'hello world')

        foo, _ = decode('0:')
        self.assertEqual(foo, '')

        foo, _ = decode('4:i12e')
        self.assertEqual(foo, 'i12e')

    def test_decode_string_fail(self):
        self.assertRaises(DecodeException, decode, '-1:test')
        self.assertRaises(DecodeException, decode, 'test')
        self.assertRaises(DecodeException, decode, ':test')
        self.assertRaises(DecodeException, decode, '5:test')
        self.assertRaises(DecodeException, decode, '5test')
        self.assertRaises(DecodeException, decode, '1:')

    def test_decode_int_success(self):
        foo, _ = decode('i12e')
        self.assertEqual(foo, 12)

        foo, _ = decode('i0e')
        self.assertEqual(foo, 0)

        foo, _ = decode('i123456789e')
        self.assertEqual(foo, 123456789)

        foo, _ = decode('i-1e')
        self.assertEqual(foo, -1)

    def test_decode_int_fail(self):
        self.assertRaises(DecodeException, decode, '7')
        self.assertRaises(DecodeException, decode, 'i7')
        self.assertRaises(DecodeException, decode, '7e')
        self.assertRaises(DecodeException, decode, 'ie')
        self.assertRaises(DecodeException, decode, 'i00e')
        self.assertRaises(DecodeException, decode, 'i-0e')
        self.assertRaises(DecodeException, decode, 'i07e')
        self.assertRaises(DecodeException, decode, 'i--7e')

    def test_decode_list_success(self):
        foo, _ = decode('le')
        self.assertEqual(foo, [])

        foo, _ = decode('lllleeee')
        self.assertEqual(foo, [[[[]]]])

        foo, _ = decode('li12ee')
        self.assertEqual(foo, [12])

        foo, _ = decode('l4:testi12ei12e3:foolleee')
        self.assertEqual(foo, ['test', 12, 12, 'foo', [[]]])

        foo, _ = decode('l4:testd3:foo3:baree')
        self.assertEqual(foo, ['test', OrderedDict([('foo', 'bar')])])

    def test_decode_list_fail(self):
        self.assertRaises(DecodeException, decode, 'l')
        self.assertRaises(DecodeException, decode, 'e')
        self.assertRaises(DecodeException, decode, 'liee')
        self.assertRaises(DecodeException, decode, 'l4:e')

    def test_decode_dictionary_success(self):
        foo, _ = decode('de')
        self.assertEqual(foo, OrderedDict())

        foo, _ = decode('d4:test4:teste')
        self.assertEqual(foo, OrderedDict([('test', 'test')]))

        foo, _ = decode('d4:test4:test1:z1:ze')
        self.assertEqual(foo, OrderedDict([('test', 'test'), ('z', 'z')]))

        foo, _ = decode('d4:test4:test1:a1:ae')
        self.assertEqual(foo, OrderedDict([('a', 'a'), ('test', 'test')]))

        foo, _ = decode('d4:test4:test1:ad1:bdeee')
        self.assertEqual(foo, OrderedDict([('a', OrderedDict([('b', OrderedDict())])), ('test', 'test')]))

        foo, _ = decode('d1:ad1:bd1:cd1:dd1:edeeeeee')
        self.assertEqual(foo, OrderedDict([('a', OrderedDict([('b', OrderedDict([('c', OrderedDict([('d', OrderedDict([('e', OrderedDict())]))]))]))]))]))

    def test_decode_dictionary_fail(self):
        self.assertRaises(DecodeException, decode, 'd')
        self.assertRaises(DecodeException, decode, 'e')
        self.assertRaises(DecodeException, decode, 'di12ei12ee')


if __name__ == '__main__':
    main()
