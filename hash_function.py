# Constants for mixing (using digits of pi and e for "nothing up my sleeve" numbers)
MIX_CONSTANT_1 = 3141592653
MIX_CONSTANT_2 = 2718281828
OUTPUT_LENGTH = 32 # Desired output length in bytes

def custom_hash(data: bytes) -> bytes:
    if not isinstance(data, bytes):
        raise TypeError("Input must be bytes")

    # Initialize state (32 bytes, e.g., with alternating 0x55 and 0xAA)
    # Using a simple pattern to avoid starting with all zeros.
    state = bytearray([(0x55 if i % 2 == 0 else 0xAA) for i in range(OUTPUT_LENGTH)])

    # Process input data
    data_len = len(data)
    for i, byte_val in enumerate(data):
        # Mix byte into the state
        state_index = i % OUTPUT_LENGTH

        # Simple mixing operation: XOR, addition, multiplication with constants
        # Use large integer arithmetic and then take modulo 256 for byte value
        # Accessing bytearray element directly gives its integer value
        current_state_val = state[state_index]

        mixed_val = (current_state_val * MIX_CONSTANT_1) + byte_val + i
        mixed_val ^= (data_len << (i % 5)) # Include data length and position dependency

        state[state_index] = mixed_val % 256

        # Secondary mixing: affect another part of the state
        other_index = (i + byte_val) % OUTPUT_LENGTH
        state[other_index] ^= (mixed_val >> (i % 3)) % 256 # Use shifted mixed value

    # Final mixing/diffusion pass over the state array
    # This helps ensure changes in input affect the whole output
    for _ in range(3): # Repeat a few times for better diffusion
        temp_state = bytearray(state) # Work on a copy for this pass
        for i in range(OUTPUT_LENGTH):
            # Mix adjacent and distant elements
            prev_index = (i - 1 + OUTPUT_LENGTH) % OUTPUT_LENGTH
            next_index = (i + 1) % OUTPUT_LENGTH
            far_index = (i * MIX_CONSTANT_2) % OUTPUT_LENGTH

            # Use direct indexing to get integer values from bytearrays
            new_val = (state[i] ^
                       temp_state[prev_index] ^
                       temp_state[next_index] ^
                       temp_state[far_index])

            # Add a constant and wrap around
            state[i] = (new_val + MIX_CONSTANT_1 // (i+1)) % 256

    return bytes(state)