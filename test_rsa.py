# ---------------------------------- Imports --------------------------------- #
import random

from byu_pytest_utils import tier

from prime_number_generation import mod_exp, fermat, miller_rabin
from generate_keypair import generate_key_pairs

import sys
sys.setrecursionlimit(4000)

# -------------------------------- Test tiers -------------------------------- #
baseline = tier('baseline', 1)
core = tier('core', 2)
stretch2 = tier('stretch2', 3)

# ----------------------------- Global variables ----------------------------- #
mod_exp_args = [
    (2, 10, 17, 4),
    (3, 7, 13, 3),
    (5, 20, 23, 12),
    (7, 13, 19, 7),
    (10, 24, 345, 100),
    (123, 23, 13, 11),
]

composite_args = [24, 255, 6349202, 123456789, 248239522935, 593872957829392,
                  409359300583028201801840123]

prime_args = [17, 7520681183, 7263570389, 8993337217, 1320230501, 4955627707, 1095542699, 4505853973, 3176051033,
              6620550763, 2175869827, 565873182758780452445419697353, 529711114181889655730813410547,
              600873118804270914899076141007, 414831830449457057686418708951, 307982960434844707438032183853]


# ------------------------------ Baseline Tests ------------------------------ #
@baseline
def test_mod_exp() -> None:
    for x, y, N, expected in mod_exp_args:
        assert mod_exp(x, y, N) == expected


@baseline
def test_primes_fermat() -> None:
    """This function tests multiple known prime numbers to verify that your fermat
    primality tests return True for prime numbers"""
    for N in prime_args:
        call = fermat(N, 100)
        assert call == True


@baseline
def test_composites_fermat() -> None:
    """This function tests multiple known composite numbers to verify that your fermat
    primality tests return False for composite numbers"""
    for N in composite_args:
        call = fermat(N, 100)
        assert call == False


# -------------------------------- Core Tests -------------------------------- #
@core
def test_key_pair_encoding_decoding():
    """
    Test RSA key pairs for various bit sizes to ensure encoding and decoding work correctly.

    Note: this test relies on extended euclid's, prime number generation, key pair generation, and mod_exp algorithms working correctly
    """

    for bits in [64, 128, 256, 512, 1024]:
        # Generate key pairs
        N, e, d = generate_key_pairs(bits)

        # Ensure that N is large enough to encrypt/decrypt a message of the given bit size
        message: int = random.getrandbits(int(bits / 4))

        # Encrypt the message
        ciphertext = mod_exp(message, e, N)

        # Decrypt the message
        decrypted_message = mod_exp(ciphertext, d, N)

        # Check that the decrypted message matches the original message
        assert (
                message == decrypted_message
        ), f"Failed for bit size {bits}: message={message}, decrypted_message={decrypted_message}"


# ------------------------------ Stretch 2 Tests ----------------------------- #
@stretch2
def test_primes_miller_rabin() -> None:
    """This function tests multiple known prime numbers to verify that your
    miller_rabin primality tests return True for prime numbers"""
    for N in prime_args:
        call = miller_rabin(N, 100)
        assert call == True


@stretch2
def test_composites_miller_rabin() -> None:
    """This function tests multiple known composite numbers to verify that your
    miller_rabin primality tests return False for prime numbers"""
    for N in composite_args:
        call = miller_rabin(N, 100)
        assert call == False
