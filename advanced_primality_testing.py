import argparse

from prime_number_generation import fermat, miller_rabin


# This is a convenience function for main(). You don't need to touch it.
def prime_test(N: int, k: int) -> tuple[True, True]:
    return fermat(N, k), miller_rabin(N, k)


def main(number: int, k: int):
    fermat_call, miller_rabin_call = prime_test(number, k)

    print(f'Is {number} prime?')
    print(f'Fermat: {fermat_call}')
    print(f'Miller-Rabin: {miller_rabin_call}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('number', type=int)
    parser.add_argument('k', type=int)
    args = parser.parse_args()
    main(args.number, args.k)
