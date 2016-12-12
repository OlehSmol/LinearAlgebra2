import numpy as np
from random import randint
class Hamming:
    _G = np.array([
        [1, 0, 1, 1],
        [1, 1, 0, 1],
        [0, 0, 0, 1],
        [1, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 0]
    ])  # generator matrix with extra row for control sum (8x4)

    _C = np.array([
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 0]
    ])  # matrix to calculate control sum (8x8)

    _H = np.array([
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 1, 1, 1, 1, 0],
        [0, 1, 1, 0, 0, 1, 1, 0],
        [1, 0, 1, 0, 1, 0, 1, 0],
    ])  # checker matrix with control sum (4x8)

    _R = np.array([
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
    ])  # recover matrix (4x8)

    def __init__(self, data , resend=False):
        """
        :param: data: list of bit (len(list)%4 == 0)
                send: flag for resending word in case of two errors
        Get data and convert it to (nx4) matrix
        """
        data = [int(i) for i in list(data)]
        if len(data)%4 != 0:
            data += [0]*(4-len(data)%4)
        self.data = np.array(data)
        self.data = self.data.reshape((self.data.size // 4, 4))
        self.resend = resend
        self.iter = 0
        self.errors_count = [0, 0, 0]  # save amounts of words with 0, 1, 2 errors
        self.resends_count = 0  # save amounts of resends
        self.words = list()

    def get_all(self):
        """
        :return: imitate process of message transfer for all words in self.data
        """
        self.iter = 0
        self.errors_count = [0, 0, 0]
        self.resends_count = 0
        self.words = list()
        result = ''
        while self.iter < len(self.data):
            result += self.get_next()
        return result

    def get_next(self):
        """
        :return: imitate process of message transfer for next word of self.data
        """
        if self.iter < len(self.data):
            word = self.data[self.iter].transpose()
            code = Hamming.decryption(word)
            noise_code = Hamming.noise(code)
            corrected_code, errors = Hamming.correction(noise_code)
            self.errors_count[errors] += 1
            while self.resend and errors == 2:
                noise_code = Hamming.noise(code)
                corrected_code, errors = Hamming.correction(noise_code)
                self.resends_count += 1
            word = Hamming.recover(corrected_code)
            self.iter += 1
            word = [str(i) for i in word.transpose().tolist()]
            self.words.append((''.join(word), errors))
            return ''.join(word)

    def get_statistic(self):
        """
        :return: dict with statistic about errors
        """
        return {"words amount": len(self.data),
                "zero error": self.errors_count[0],
                "one error": self.errors_count[1],
                "two error": self.errors_count[2],
                "resends": self.resend and self.resends_count
                }

    @staticmethod
    def decryption(word):
        """
        :param word: (1x4)
        :return code: (1x8)
        Get 4-bit word and decrypt it augmented Hamming code
        """
        code = np.dot(Hamming._G, word) % 2  # multiply word and generation matrix (1x4)(4x8) = (1x8)
        code = np.dot(Hamming._C, code) % 2  # multiply code and control sum  matrix (1x8)(8x8) = (1x8)
        return code

    @staticmethod
    def noise(code):
        """
        :param code: (1x8)
        :return code: (1x8)
        Get Hamming code and distorts in 0, 1 or 2 bits
        """
        code = np.copy(code)
        if randint(0, 2) == 0:
            code[randint(0, 7)] += 1  # add error to random bit
        if randint(0, 2) == 0:
            code[randint(0, 7)] += 1  # add error to random bit

        return code % 2

    @staticmethod
    def correction(code):
        """
        :param code: (1x8)
        :return code: (1x8)
        Get Hamming code which went throw noise chanel and try to correct it.
        If code have no error return this code with flag - 0
        If code have one error return corrected code with flag - 1
        If code have two error return this code with flag - 2
        """
        code = np.copy(code)
        error = np.dot(Hamming._H, code) % 2  # get error vector by multiplying checker matrix with code
        if error[0] == 1:  # if control sum equal to 1 we have only one error and we can correct it
            position = np.dot(error, np.array([0, 4, 2, 1]))  # find position of error bit
            if position > 0:  # if position == 0 error was in control sum
                code[position - 1] = (code[position - 1] + 1) % 2
            return (code, 1)
        else:
            if np.dot(error, np.array([1, 1, 1, 1])) == 0:  # check errors of code
                return (code, 0)
            else:
                return (code, 2)

    @staticmethod
    def recover(code):
        """
        :param code: (1x8) code after correction
        :return word: (1x8) recover word
        """
        code = np.copy(code)
        return np.dot(Hamming._R, code.transpose()).transpose()

class Converter:
    @staticmethod
    def utf8_to_binary(data):
        return ''.join(['0' + format(ord(l), 'b') for l in data])

    @staticmethod
    def binary_to_utf8(data):
        return ''.join([chr(int(data[8*i:8*(i+1)], 2)) for i in range(len(data)//8)])
