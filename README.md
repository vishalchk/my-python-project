# my-python-project

[![Tests](https://github.com/vishalchk/my-python-project/actions/workflows/tests.yml/badge.svg)](https://github.com/vishalchk/my-python-project/actions/workflows/tests.yml)

A prime number toolkit that progresses through classic number-theory
algorithms — from basic primality checking up to a working RSA
encryption/decryption demo.

## Why this project

RSA — the algorithm behind HTTPS, SSH, and most public-key cryptography —
is built entirely out of the primitives implemented here:

- Generating large primes (`is_prime_miller_rabin`) is how real RSA key
  generation works: pick a random odd number, run Miller-Rabin, keep it if
  it survives. Trial division is too slow at cryptographic key sizes
  (hundreds of digits), which is exactly why Miller-Rabin exists.
- Picking a valid public exponent (`is_coprime`/`gcd`) is the same check
  RSA uses to validate `e` against `φ(n)`.
- The `rsa` command wires these together into a full, working (if
  intentionally toy-sized) encrypt/decrypt round trip.

## What's implemented

- **Trial division** (`check`) — simple, correct, fine for small numbers.
- **Sieve of Eratosthenes** (`sieve`) — generates *all* primes up to a limit
  far faster than checking each number individually.
- **Deterministic Miller-Rabin** (`large`) — a primality test that stays
  fast even on numbers with 20+ digits, where trial division would never
  finish.
- **Euclidean algorithm** (`coprime`) — checks whether two numbers share no
  common factors (gcd == 1).
- **Toy RSA** (`rsa`) — generates an RSA keypair from two Miller-Rabin
  primes and encrypts/decrypts a message with it.
- **Plotting** (`plot`) — chart of the first N primes (index vs. value).

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python main.py check 97
# 97 is prime

python main.py sieve 30
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

python main.py large 2305843009213693951
# 2305843009213693951 is prime

python main.py plot 10
# Saved plot to primes_plot.png (index vs. value chart of the first 10 primes)

python main.py coprime 14 15
# 14 and 15 are coprime (gcd = 1)

python main.py rsa "Hello, RSA!"
# Public key  (e, n): (65537, ...)
# Private key (d, n): (..., ...)
# Ciphertext: ...
# Decrypted:  Hello, RSA!
```

Run `python main.py --help` for the full command reference.

> **Note:** the `rsa` command is an educational implementation of textbook
> RSA. It is missing padding (e.g. OAEP) and uses small key sizes by
> default, so it should not be used to secure real data — use a vetted
> library (e.g. `cryptography`) for that. It's here to demonstrate *how*
> RSA works, using the same primality-testing building blocks as the rest
> of this project.

## Test

```bash
pytest
```

20 tests cover edge cases (negatives, 0, 1), known primes and composites,
Carmichael numbers (which fool naive Fermat-style tests but are correctly
rejected by Miller-Rabin), a large Mersenne prime, gcd/coprime checks, and
a full RSA encrypt/decrypt round trip validated against a textbook example.

Tests run automatically on every push via GitHub Actions (see badge above).

## License

MIT — see [LICENSE](LICENSE).
