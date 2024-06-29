import random
import math
import time

def is_prime(n):  # Check if a number is prime
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

def generate_prime(bits):  # Generate a prime number with the specified number of bits
    while True:
        num = random.getrandbits(bits)
        num |= (1 << bits - 1) | 1  # Ensure the number has the correct number of bits and is odd
        if is_prime(num):
            return num

def gcd(a, b):  # Greatest common divisor using the Euclidean method
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a, b):   
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def generate_keys(bits):
    start_time = time.perf_counter()  # Start measuring time
    p = generate_prime(bits // 2 + 1)
    q = generate_prime(bits - (bits // 2 + 1))
    
    n = p * q
    phi = (p - 1) * (q - 1)  # Euler's totient function
    e = random.randrange(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)

    _, d, _ = extended_gcd(e, phi)
    d %= phi
    if d < 0:
        d += phi

    # Validate that (e * d) % phi == 1
    if (e * d) % phi != 1:
        raise ValueError("Failed to generate valid keys. Please try again.")

    end_time = time.perf_counter()
    public_key = (n, e)
    private_key = (n, d)
    return public_key, private_key, end_time - start_time

def factor_modulus(N):  # Function to get (p, q)
    sqrt_N = int(math.sqrt(N)) + 1
    for i in range(2, sqrt_N):
        if N % i == 0:
            p = i
            q = N // i
            return p, q
    return None, None

def encrypt(message, public_key):
    n, e = public_key
    encrypted_message = pow(message, e, n)
    return encrypted_message

def decrypt(encrypted_message, private_key):
    n, d = private_key
    decrypted_message = pow(encrypted_message, d, n)
    return decrypted_message          

def main():
    try:
        take_bits = int(input("How many bits do you want (8 or 16): "))  # Validate input
        if take_bits not in [8, 16]:
            print("Invalid bit size. Please enter 8 or 16.")
            return
        message = int(input("Enter message: "))
        if message < 0:
            print("Invalid message. Please enter a non-negative integer.")
            return
    except ValueError:
        print("Invalid input. Please enter integers only.")
        return

    print(f"Generating {take_bits}-bit RSA keys...")
    public_key, private_key, key_gen_time = generate_keys(take_bits)
    print("Public key (N, e):", public_key)
    print("Private key (N, d):", private_key)
    print("Key generation time:", key_gen_time, "seconds")
    print()
  
    # Test encryption and decryption
    print("Original message:", message)
    encrypted_message = encrypt(message, public_key)
    print("Encrypted message:", encrypted_message)
    decrypted_message = decrypt(encrypted_message, private_key)
    print("Decrypted message:", decrypted_message)        

    # Test p and q
    p, q = factor_modulus(public_key[0])
    if p and q:
        print("Modulus factored successfully. p =", p, ", q =", q)
    else:
        print("Failed to factorize modulus.")

if __name__ == "__main__":
    main()