import numpy as np
import time

class Mersenne:
    def __init__(self, seed: int = 5489):
        """
        initialiator voor de mersenne twister

        :param seed: (int)
            start waarde voor de algoritme
        """

        self.seed = seed
        self.w = 32
        self.r = 31
        self.n = 624
        self.m = 397
        self.u = 11
        self.s = 7
        self.t = 15
        self.l = 18
        self.a = 0x9908b0df
        self.b = 0x9d2c5680
        self.c = 0xefc60000
        self.f = 0x6c078965
        self.compress_mask = 0xffffffff
        self.Z = [seed]
        self.random_numbers = None

        self.upmask = int('10000000000000000000000000000000', 2)
        self.lowmask = int('01111111111111111111111111111111', 2)
        self.initialize_seed()
        self.twist()

    def twist(self):
        """
        dit functie gebruikt de mersenne twister om een block met random nummers gegeneert

        :return: (list)
            lijst met random nummers
        """

        new_block = []
        mid_index = self.m
        first_index = 0
        second_index = 1

        while len(new_block) < self.n:
            mid_b = self.Z[mid_index]
            first_b = self.Z[first_index]
            second_b = self.Z[second_index]

            mid_index += 1
            first_index += 1
            second_index += 1
            if mid_index == self.n:
                mid_index = 0
            if second_index == self.n:
                second_index = 0

            concat = (first_b & self.upmask) | (second_b & self.lowmask)
            least_sig = concat & 1
            if least_sig == 0:
                out = concat >> 1
            else:
                out = (concat >> 1) ^ self.a
            new_block.append(mid_b ^ out)

        twisted_block = []
        for i in new_block:
            y = i
            y = y ^ (y >> self.u)
            y = y ^ ((y << self.s) & self.b)
            y = y ^ ((y << self.t) & self.c)
            y = y ^ (y >> self.l)
            twisted_block.append(y)
        self.random_numbers = twisted_block
        self.Z = twisted_block.copy()
        return twisted_block

    def randomly(self, left: int = 0, right: int = 100):
        """
        dit functie genereert een random nummer door de mersenne twister te gebruiken

        :param right: (int)
            max waarde
        :param left: (int)
            min waarde
        :return: (int)
            de random nummer
        """

        rn = self.random_numbers[0]
        self.random_numbers.pop(0)
        if len(self.random_numbers) == 0:
            self.twist()
        return round(rn / int('1' + '0' * 10) * right + left)

    def initialize_seed(self):
        """
        initialiseert voor de eerste deel van de mersenne twister
        """
        for i in range(self.n - 1):
            self.Z.append((self.f * (self.Z[i] ^ (self.Z[i] >> (self.w - 2))) + i) & self.compress_mask)
