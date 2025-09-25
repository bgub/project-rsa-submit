import sys
from time import time
import random


# Used the pseudo-code from the textbook.
def mod_exp(x: int, y: int, N: int) -> int:
    if y == 0:
        return 1

    z = mod_exp(x, y // 2, N)
    if y % 2 == 0:
        return (z**2) % N
    else:
        return (x * (z**2)) % N


def extended_euclid(a: int, b: int) -> int:
    """
    Takes integers such that 0 <= b <= a
    Return integers x,y,d such that
    d = gcd(a, b) and ax + by = d
    """
    if b == 0:
        return (1, 0, a)
    x_prime, y_prime, d = extended_euclid(b, a % b)

    return y_prime, x_prime - (a // b) * y_prime, d


def fermat(N: int, k: int) -> bool:
    """
    Returns True if N is prime
    """

    for i in range(0, k):
        a = random.randint(1, N - 1)
        if mod_exp(a, N - 1, N) != 1:
            return False

    return True


def factor_two(N: int) -> int:
    res = 0
    while True:
        if N % 2 == 0:
            N = N / 2
            res += 1
        else:
            return res


def miller_rabin(N: int, k: int) -> bool:
    """
    Returns True if N is prime
    """

    t = factor_two(N)
    u = (N - 1) // (2**t)

    # possible_
    for i in range(0, k):
        a = random.randint(1, N - 1)

        prev, curr = 0, 0
        curr = mod_exp(a, u, N)

        for i in range(1, t):
            prev = curr
            curr = mod_exp(curr**2, u, N)
            if curr == 1 and prev != 1:
                return False

        if mod_exp(a, N - 1, N) != 1:
            return False

    return True


def generate_large_prime(n_bits: int) -> int:
    """Generate a random prime number with the specified bit length"""

    sys.setrecursionlimit(4000)
    while True:
        num = random.getrandbits(n_bits)
        if num == 0 or num == 1 or num == 2:
            continue
        if fermat(num, k=20):
            return num


def main(n_bits: int):
    start = time()
    large_prime = generate_large_prime(n_bits)
    print(large_prime)
    print(f"Generation took {time() - start} seconds")


if __name__ == "__main__":
    main(int(sys.argv[1]))
