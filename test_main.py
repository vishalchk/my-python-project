from main import is_prime, sieve


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
