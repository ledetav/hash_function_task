from hash_function import custom_hash
import os

def print_hash_example(data):
    """Helper function to print data and its hash."""
    if isinstance(data, bytes):
        try:
            # Try decoding for display, use repr if fails
            display_data = data.decode('utf-8', errors='replace')
            if len(display_data) > 60: # Truncate long strings for display
                 display_data = display_data[:57] + "..."
        except Exception:
            display_data = repr(data)
            if len(display_data) > 60:
                 display_data = display_data[:57] + "...'"
    else:
        display_data = repr(data) # Should not happen with type check, but safe

    print(f"Input Data:     {display_data}")

    try:
        hash_value = custom_hash(data)
        print(f"Hash (hex):     {hash_value.hex()}")
        print(f"Hash Length:    {len(hash_value)} bytes")
    except TypeError as e:
        print(f"Error:          {e}")
    print("-" * 40)

if __name__ == "__main__":
    print("--- Custom Hash Function Examples ---")

    # Example 1: Simple string
    print_hash_example(b"Hello, World!")

    # Example 2: Slightly different string
    print_hash_example(b"Hello, world!") # Lowercase 'w'

    # Example 3: Empty string
    print_hash_example(b"")

    # Example 4: Short string
    print_hash_example(b"abc")

    # Example 5: String with repetition
    print_hash_example(b"aaaaabbbbbccccc")

    # Example 6: Longer string
    long_string = b"This is a longer sentence used to test the hash function with more input data than previous examples."
    print_hash_example(long_string)

    # Example 7: Data with null bytes
    print_hash_example(b"Data with\x00null bytes")

    # Example 8: Very long data (e.g., 1KB)
    # Generating some pseudo-random data for demonstration
    long_data = os.urandom(1024)
    print("Input Data:     <1KB of random bytes>") # Don't print the actual bytes
    try:
        hash_value = custom_hash(long_data)
        print(f"Hash (hex):     {hash_value.hex()}")
        print(f"Hash Length:    {len(hash_value)} bytes")
    except TypeError as e: # Should not happen here
        print(f"Error:          {e}")
    print("-" * 40)

    # Example 9: Hashing the same data again (demonstrating determinism)
    print("Hashing 'Hello, World!' again...")
    print_hash_example(b"Hello, World!")

    # Example 10: Invalid input type (demonstrating error handling)
    print("Attempting to hash a non-bytes type (string)...")
    print_hash_example("This is a string") # Passing a str, not bytes

    print("--- End of Examples ---")
