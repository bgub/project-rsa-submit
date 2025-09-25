import sys
from pathlib import Path
from time import time
from typing import Iterable, Literal, Tuple

from prime_number_generation import mod_exp

sys.setrecursionlimit(5000)

HeaderSize = 8  # bytes for original length (unsigned big-endian)


def read_key(key_file: Path) -> Tuple[int, int, int, int]:
    """
    Returns: (n_bytes, plain_bytes, N, exponent)
    n_bytes    = modulus size in bytes (for ciphertext chunking)
    plain_bytes= safe plaintext block size (< N) to avoid m >= N
    """
    N_str, exponent_str = key_file.read_text().splitlines()
    N = int(N_str)
    exponent = int(exponent_str)
    n_bytes = (N.bit_length() + 7) // 8
    plain_bytes = (N.bit_length() - 1) // 8  # ensure m < N
    if plain_bytes <= 0:
        raise ValueError("Modulus too small.")
    return n_bytes, plain_bytes, N, exponent


def chunks(b: bytes, size: int) -> Iterable[bytes]:
    for i in range(0, len(b), size):
        yield b[i : i + size]


def decide_mode(input_len: int, n_bytes: int) -> Literal["encrypt", "decrypt"]:
    # Heuristic: ciphertext length must be a multiple of n_bytes
    return "decrypt" if input_len % n_bytes == 0 else "encrypt"


def add_len_header_and_pad(plain: bytes, plain_bytes: int) -> bytes:
    header = len(plain).to_bytes(HeaderSize, "big")
    data = header + plain
    rem = len(data) % plain_bytes
    if rem:
        data += b"\x00" * (plain_bytes - rem)
    return data


def strip_len_header_and_unpad(decrypted: bytes) -> bytes:
    if len(decrypted) < HeaderSize:
        raise ValueError("Decrypted data too short for header.")
    L = int.from_bytes(decrypted[:HeaderSize], "big")
    body = decrypted[HeaderSize : HeaderSize + L]
    if len(body) != L:
        raise ValueError("Decrypted length header mismatch.")
    return body


def transform(
    data: bytes,
    N: int,
    exponent: int,
    in_chunk_bytes: int,
    out_chunk_bytes: int,
) -> bytes:
    out = []
    for block in chunks(data, in_chunk_bytes):
        if len(block) != in_chunk_bytes:
            raise ValueError("Input not aligned to chunk size.")
        x = int.from_bytes(block, "big")
        y = mod_exp(x, exponent, N)
        out.append(y.to_bytes(out_chunk_bytes, "big"))
    return b"".join(out)


def main(key_file: Path, message_file: Path, output_file: Path):
    """
    Encrypt or decrypt `message_file` and write the result in `output_file`.

    Heuristic:
      - If input length is multiple of modulus-bytes: treat as ciphertext (decrypt).
      - Otherwise: treat as plaintext (encrypt).
    """
    n_bytes, plain_bytes, N, exponent = read_key(key_file)
    input_bytes = message_file.read_bytes()

    mode = decide_mode(len(input_bytes), n_bytes)

    start = time()

    if mode == "encrypt":
        prepared = add_len_header_and_pad(input_bytes, plain_bytes)
        # plaintext blocks -> ciphertext blocks
        result = transform(
            prepared, N, exponent, in_chunk_bytes=plain_bytes, out_chunk_bytes=n_bytes
        )
    else:
        # ciphertext blocks -> plaintext blocks
        decrypted_blocks = transform(
            input_bytes,
            N,
            exponent,
            in_chunk_bytes=n_bytes,
            out_chunk_bytes=plain_bytes,
        )
        result = strip_len_header_and_unpad(decrypted_blocks)

    print(f"{mode} in {time() - start:.6f} seconds")
    output_file.write_bytes(result)


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
