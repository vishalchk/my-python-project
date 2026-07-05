# my-python-project

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python main.py check <number>   # is it prime? (trial division)
python main.py sieve <limit>    # list all primes up to limit
python main.py large <number>   # is it prime? (Miller-Rabin, for big numbers)
```

## Test

```bash
pytest
```
