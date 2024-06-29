import random
import time

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):  # calculates the modular inverse of a modulo m.
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def brute_force_private_exponent(N, e):  # find the private exponent d using brute force
    p, q = factor_modulus(N)
    if p is None or q is None:
        return None
    phi = (p - 1) * (q - 1)
    for d in range(2, phi):
        if (e * d) % phi == 1:
            return d
    return None

def generate_prime(bit_size):
    while True:
        num = random.randrange(2**(bit_size - 1), 2**bit_size)
        if is_prime(num):
            return num

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_rsa_keys(bit_size):  # Generate two random prime numbers p and q
    p = generate_prime(bit_size // 2)
    q = generate_prime(bit_size // 2)
    N = p * q  # Calculate modulus N
    phi = (p - 1) * (q - 1)  # Calculate Euler's totient function
    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    d = mod_inverse(e, phi)  # Calculate private exponent d using the modular inverse of e mod phi
    return (N, e), (N, d)  # Return public and private keys

def factor_modulus(N):
    sqrt_N = int(N**0.5) + 1
    for i in range(2, sqrt_N):
        if N % i == 0:
            p = i
            q = N // i
            return p, q
    return None, None

# Function to test brute force attack
def test_brute_force_attack(N, e):
    print("Attempting brute force attack to find the private exponent...")
    start_time = time.perf_counter()
    found_d = brute_force_private_exponent(N, e)
    end_time = time.perf_counter()
    if found_d is not None:
        print("Brute force found private exponent (d):", found_d)
    else:
        print("Brute force attack failed. Unable to find private exponent (d).")
    print("Brute force attack time:", end_time - start_time, "seconds")

def main():
    try:
        take_bits = int(input("How many bits do you want (8 or 16): "))  # Validate input
        if take_bits not in [8, 16]:
            print("Invalid bit size. Please enter 8 or 16.")
            return
    except ValueError:
        print("Invalid input. Please enter an integer.")
        return

    print(f"Testing RSA with {take_bits}-bit key size:")
    start_time = time.perf_counter()
    public_key, private_key = generate_rsa_keys(take_bits)
    end_time = time.perf_counter()
    print("Public Key (N, e):", public_key)
    print("Private Key (N, d):", private_key)
    print("Key generation time:", end_time - start_time, "seconds")

    test_brute_force_attack(public_key[0], public_key[1])

if __name__ == "__main__":
    main()
