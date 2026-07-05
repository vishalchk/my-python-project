import sys


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


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--sieve":
        limit = int(sys.argv[2])
        print(sieve(limit))
    elif len(sys.argv) == 2:
        n = int(sys.argv[1])
        print(f"{n} is {'prime' if is_prime(n) else 'not prime'}")
    else:
        print("Usage: python main.py <number>")
        print("       python main.py --sieve <limit>")
        sys.exit(1)


if __name__ == "__main__":
    main()
