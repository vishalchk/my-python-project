import argparse
import secrets
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


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def is_coprime(a, b):
    return gcd(a, b) == 1


def generate_prime(bits):
    while True:
        candidate = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if is_prime_miller_rabin(candidate):
            return candidate


def mod_inverse(e, phi):
    """Extended Euclidean algorithm: find d such that (e * d) % phi == 1."""
    old_r, r = e, phi
    old_s, s = 1, 0
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
    return old_s % phi


def generate_rsa_keypair(bits):
    p = generate_prime(bits)
    q = generate_prime(bits)
    while q == p:
        q = generate_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    while not is_coprime(e, phi):
        e += 2

    d = mod_inverse(e, phi)
    return (e, n), (d, n)


def rsa_encrypt(message, public_key):
    e, n = public_key
    m = int.from_bytes(message.encode(), "big")
    if m >= n:
        raise ValueError("Message too long for this key size; use more --bits")
    return pow(m, e, n)


def rsa_decrypt(ciphertext, private_key):
    d, n = private_key
    m = pow(ciphertext, d, n)
    length = (m.bit_length() + 7) // 8
    return m.to_bytes(length, "big").decode()


def first_n_primes(count):
    primes = []
    candidate = 2
    while len(primes) < count:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 1
    return primes


def plot_primes(count, output_path):
    import matplotlib.pyplot as plt

    primes = first_n_primes(count)
    indices = list(range(1, count + 1))

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(indices, primes, color="#2563eb", linewidth=2, marker="o", markersize=6)

    for x, y in zip(indices, primes):
        ax.annotate(str(y), (x, y), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8)

    ax.set_xlabel("Index (nth prime)")
    ax.set_ylabel("Prime value")
    ax.set_title(f"First {count} Prime Numbers")
    ax.set_xticks(indices)
    ax.grid(True, linewidth=0.5, alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    print(f"Saved plot to {output_path}")


def build_parser():
    parser = argparse.ArgumentParser(description="Check and generate prime numbers.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check", help="Check if a number is prime (trial division)")
    check_parser.add_argument("number", type=int)

    sieve_parser = subparsers.add_parser("sieve", help="List all primes up to a limit")
    sieve_parser.add_argument("limit", type=int)

    large_parser = subparsers.add_parser("large", help="Check if a large number is prime (Miller-Rabin)")
    large_parser.add_argument("number", type=int)

    plot_parser = subparsers.add_parser("plot", help="Plot the first N primes (index vs value)")
    plot_parser.add_argument("count", type=int, nargs="?", default=10)
    plot_parser.add_argument("--output", default="primes_plot.png")

    coprime_parser = subparsers.add_parser("coprime", help="Check if two numbers are coprime (gcd == 1)")
    coprime_parser.add_argument("a", type=int)
    coprime_parser.add_argument("b", type=int)

    rsa_parser = subparsers.add_parser("rsa", help="Toy RSA demo: generate keys, encrypt & decrypt a message")
    rsa_parser.add_argument("message")
    rsa_parser.add_argument("--bits", type=int, default=256, help="Bit length of each prime (default: 256)")

    return parser


def main():
    args = build_parser().parse_args()

    if args.command == "check":
        print(f"{args.number} is {'prime' if is_prime(args.number) else 'not prime'}")
    elif args.command == "sieve":
        print(sieve(args.limit))
    elif args.command == "large":
        print(f"{args.number} is {'prime' if is_prime_miller_rabin(args.number) else 'not prime'}")
    elif args.command == "plot":
        plot_primes(args.count, args.output)
    elif args.command == "coprime":
        result = is_coprime(args.a, args.b)
        print(f"{args.a} and {args.b} are {'coprime' if result else 'not coprime'} (gcd = {gcd(args.a, args.b)})")
    elif args.command == "rsa":
        public_key, private_key = generate_rsa_keypair(args.bits)
        e, n = public_key
        d, _ = private_key

        try:
            ciphertext = rsa_encrypt(args.message, public_key)
        except ValueError as error:
            print(f"Error: {error}")
            sys.exit(1)

        plaintext = rsa_decrypt(ciphertext, private_key)

        print(f"Public key  (e, n): ({e}, {n})")
        print(f"Private key (d, n): ({d}, {n})")
        print(f"Ciphertext: {ciphertext}")
        print(f"Decrypted:  {plaintext}")


if __name__ == "__main__":
    main()
