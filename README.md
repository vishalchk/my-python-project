# my-python-project

A prime number toolkit that progresses through three classic algorithms as the
problem size grows:

- **Trial division** (`check`) — simple, correct, fine for small numbers.
- **Sieve of Eratosthenes** (`sieve`) — generates *all* primes up to a limit far
  faster than checking each number individually.
- **Deterministic Miller-Rabin** (`large`) — a primality test that stays fast
  even on numbers with 20+ digits, where trial division would never finish.
- **Euclidean algorithm** (`coprime`) — checks whether two numbers share no
  common factors (gcd == 1).

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
```

Run `python main.py --help` for the full command reference.

## Test

```bash
pytest
```

16 tests cover edge cases (negatives, 0, 1), known primes and composites,
Carmichael numbers (which fool naive Fermat-style tests but are correctly
rejected by Miller-Rabin), a large Mersenne prime, and gcd/coprime checks.

## License

MIT — see [LICENSE](LICENSE).
