import numpy as np
from unittest import TestCase
from src.hamming import Hamming, Converter
from random import sample

class TestHamming(TestCase):
    def test_decryption1(self):
        expected = np.array([0, 1, 1, 0, 0, 1, 1, 0])
        actual = Hamming.decryption(np.array([1, 1, 0, 1]))
        np.testing.assert_array_equal(expected, actual)

    def test_decryption2(self):
        expected = np.array([1, 1, 0, 0, 1, 1, 0, 0])
        actual = Hamming.decryption(np.array([0, 1, 1, 0]))
        np.testing.assert_array_equal(expected, actual)

    def test_decryption3(self):
        expected = np.array([1, 1, 1, 1, 1, 1, 1, 1])
        actual = Hamming.decryption(np.array([1, 1, 1, 1]))
        np.testing.assert_array_equal(expected, actual)


    def test_correction_zero_errors(self):
        code = np.array([1, 1, 0, 0, 1, 1, 0, 0])
        expected = (np.array([1, 1, 0, 0, 1, 1, 0, 0]), 0)
        actual = Hamming.correction(code)
        np.testing.assert_array_equal(expected[0], actual[0])
        self.assertEqual(expected[1], actual[1])

    def test_correction_random_one_error(self):
        code = np.array([1, 1, 0, 0, 1, 1, 0, 0])
        error = sample(range(0, 7), 1)
        code[error[0]] += 1
        code %= 2
        expected = (np.array([1, 1, 0, 0, 1, 1, 0, 0]), 1)
        actual = Hamming.correction(code)
        np.testing.assert_array_equal(expected[0], actual[0])
        self.assertEqual(expected[1], actual[1])

    def test_correction_one_error_in_control_sum(self):
        code = np.array([1, 1, 0, 0, 1, 1, 0, 0])
        code[7] += 1
        code %= 2
        expected = (np.array([1, 1, 0, 0, 1, 1, 0, 0]), 1)
        actual = Hamming.correction(code)
        np.testing.assert_array_equal(expected[0], actual[0])
        self.assertEqual(expected[1], actual[1])

    def test_correction_two_errors(self):
        code = np.array([1, 1, 0, 0, 1, 1, 0, 0])
        error = sample(range(0, 7), 2)
        code[error[0]] += 1
        code[error[1]] += 1
        code %= 2
        expected = (code, 2)
        actual = Hamming.correction(code)
        np.testing.assert_array_equal(expected[0], actual[0])
        self.assertEqual(expected[1], actual[1])

    def test_recover1(self):
        expected = np.array([1, 1, 0, 1])
        actual = Hamming.recover(np.array([0, 1, 1, 0, 0, 1, 1, 0]))
        np.testing.assert_array_equal(expected, actual)

    def test_recover2(self):
        expected = np.array([0, 1, 1, 0])
        actual = Hamming.recover(np.array([1, 1, 0, 0, 1, 1, 0, 0]))
        np.testing.assert_array_equal(expected, actual)

    def test_recover3(self):
        expected = np.array([1, 1, 1, 1])
        actual = Hamming.recover(np.array([1, 1, 1, 1, 1, 1, 1, 1]))
        np.testing.assert_array_equal(expected, actual)

    def test_utf8_to_binary_converter(self):
        expected = "011000010110001001100011"
        actual = Converter.utf8_to_binary("abc")
        self.assertEquals(expected, actual)

    def test_utf8_to_binary_converter_with_spaces(self):
        expected = "011000010010000001100010"
        actual = Converter.utf8_to_binary("a b")
        self.assertEquals(expected, actual)

    def test_utf8_to_binary_converter_symbols(self):
        expected = "0010101000100110010000000010010100100100"
        actual = Converter.utf8_to_binary("*&@%$")
        self.assertEquals(expected, actual)

    def test_binary_to_utf8(self):
        expected = "*&@%$"
        actual = Converter.binary_to_utf8("0010101000100110010000000010010100100100")
        self.assertEquals(expected, actual)

    def test_utf8_to_binary_to_utf8(self):
        expected = "011000010010000001100010"
        actual = Converter.utf8_to_binary(Converter.binary_to_utf8("011000010010000001100010"))
        self.assertEquals(expected, actual)

    def test_utf8_to_binary_to_utf8(self):
        expected = "abc"
        actual = Converter.binary_to_utf8(Converter.utf8_to_binary("abc"))
        self.assertEquals(expected, actual)
