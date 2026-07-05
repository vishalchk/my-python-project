import argparse


def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    for divisor in range(3, int(n**0.5) + 1, 2):
        if n % divisor == 0:
            return False
    return True


def is_prime_miller_rabin(n):
    """Deterministic Miller-Rabin, correct for all n < 3.3 * 10^24."""
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)

    if n < 2:
        return False
    for p in small_primes:
        if n % p == 0:
            return n == p

    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for a in small_primes:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def sieve(limit):
    if limit < 2:
        return []

    is_candidate = [True] * (limit + 1)
    is_candidate[0] = is_candidate[1] = False

    for number in range(2, int(limit**0.5) + 1):
        if is_candidate[number]:
            for multiple in range(number * number, limit + 1, number):
                is_candidate[multiple] = False

    return [n for n, prime in enumerate(is_candidate) if prime]


def build_parser():
    parser = argparse.ArgumentParser(description="Check and generate prime numbers.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check", help="Check if a number is prime (trial division)")
    check_parser.add_argument("number", type=int)

    sieve_parser = subparsers.add_parser("sieve", help="List all primes up to a limit")
    sieve_parser.add_argument("limit", type=int)

    large_parser = subparsers.add_parser("large", help="Check if a large number is prime (Miller-Rabin)")
    large_parser.add_argument("number", type=int)

    return parser


def main():
    args = build_parser().parse_args()

    if args.command == "check":
        print(f"{args.number} is {'prime' if is_prime(args.number) else 'not prime'}")
    elif args.command == "sieve":
        print(sieve(args.limit))
    elif args.command == "large":
        print(f"{args.number} is {'prime' if is_prime_miller_rabin(args.number) else 'not prime'}")


if __name__ == "__main__":
    main()
