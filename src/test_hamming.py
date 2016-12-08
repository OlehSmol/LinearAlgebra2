import numpy as np
from unittest import TestCase
from src.hamming import Hamming
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

    def test_correction2_one_error(self):
        code = np.array([1, 1, 0, 0, 1, 1, 0, 0])
        error = sample(range(0, 7), 1)
        code[error[0]] += 1
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
        expected = np.array([1, 1, 0, 1])
        actual = Hamming.recover(np.array([0, 1, 1, 0, 0, 1, 1, 0]))
        np.testing.assert_array_equal(expected, actual)

    def test_recover3(self):
        expected = np.array([1, 1, 0, 1])
        actual = Hamming.recover(np.array([0, 1, 1, 0, 0, 1, 1, 0]))
        np.testing.assert_array_equal(expected, actual)