import pytest

from main import (
    gcd,
    generate_prime,
    generate_rsa_keypair,
    is_coprime,
    is_prime,
    is_prime_miller_rabin,
    mod_inverse,
    rsa_decrypt,
    rsa_encrypt,
    sieve,
)


def test_is_prime_below_two():
    assert is_prime(-5) is False
    assert is_prime(0) is False
    assert is_prime(1) is False


def test_is_prime_small_primes():
    for n in (2, 3, 5, 7, 11, 13, 97):
        assert is_prime(n) is True


def test_is_prime_composites():
    for n in (4, 6, 8, 9, 15, 100):
        assert is_prime(n) is False


def test_is_prime_large_prime():
    assert is_prime(104729) is True  # 10,000th prime


def test_sieve_below_two():
    assert sieve(0) == []
    assert sieve(1) == []


def test_sieve_small_limit():
    assert sieve(20) == [2, 3, 5, 7, 11, 13, 17, 19]


def test_sieve_agrees_with_is_prime():
    limit = 500
    assert sieve(limit) == [n for n in range(2, limit + 1) if is_prime(n)]


def test_miller_rabin_below_two():
    assert is_prime_miller_rabin(-5) is False
    assert is_prime_miller_rabin(0) is False
    assert is_prime_miller_rabin(1) is False


def test_miller_rabin_agrees_with_is_prime():
    limit = 2000
    for n in range(limit):
        assert is_prime_miller_rabin(n) == is_prime(n)


def test_miller_rabin_carmichael_numbers():
    # Carmichael numbers fool the naive Fermat primality test but are composite.
    for n in (561, 1105, 1729, 2465, 2821):
        assert is_prime_miller_rabin(n) is False


def test_miller_rabin_large_mersenne_prime():
    assert is_prime_miller_rabin(2305843009213693951) is True  # 2**61 - 1


def test_miller_rabin_large_composite():
    assert is_prime_miller_rabin(2305843009213693951 * 3) is False


def test_gcd():
    assert gcd(14, 15) == 1
    assert gcd(12, 18) == 6
    assert gcd(0, 5) == 5
    assert gcd(7, 7) == 7


def test_is_coprime_true():
    assert is_coprime(14, 15) is True
    assert is_coprime(17, 5) is True
    assert is_coprime(1, 100) is True


def test_is_coprime_false():
    assert is_coprime(12, 18) is False
    assert is_coprime(10, 20) is False


def test_is_coprime_two_distinct_primes():
    # Any two distinct primes are always coprime.
    for a, b in ((2, 3), (5, 11), (13, 97)):
        assert is_coprime(a, b) is True


def test_generate_prime_returns_a_prime_of_requested_size():
    prime = generate_prime(64)
    assert is_prime_miller_rabin(prime) is True
    assert prime.bit_length() == 64


def test_mod_inverse_textbook_example():
    # Classic textbook RSA example: e=17, phi=3120 -> d=2753.
    assert mod_inverse(17, 3120) == 2753
    assert (17 * 2753) % 3120 == 1


def test_rsa_round_trip():
    public_key, private_key = generate_rsa_keypair(128)
    for message in ("HI", "Hello, RSA!", "prime numbers rock"):
        ciphertext = rsa_encrypt(message, public_key)
        assert rsa_decrypt(ciphertext, private_key) == message


def test_rsa_message_too_long_raises():
    public_key, _ = generate_rsa_keypair(64)
    with pytest.raises(ValueError):
        rsa_encrypt("x" * 100, public_key)
