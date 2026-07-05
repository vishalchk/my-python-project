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


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <number>")
        sys.exit(1)

    n = int(sys.argv[1])
    print(f"{n} is {'prime' if is_prime(n) else 'not prime'}")


if __name__ == "__main__":
    main()
