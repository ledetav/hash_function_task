import unittest
import os
from hash_function import custom_hash, OUTPUT_LENGTH

class TestCustomHashFunction(unittest.TestCase):

    def test_output_length_is_correct(self):
        """Verify the hash output is always OUTPUT_LENGTH bytes."""
        data = b"some test data"
        hash_result = custom_hash(data)
        self.assertEqual(len(hash_result), OUTPUT_LENGTH)

    def test_output_length_empty_input(self):
        """Verify the hash output length for empty input."""
        data = b""
        hash_result = custom_hash(data)
        self.assertEqual(len(hash_result), OUTPUT_LENGTH)

    def test_output_length_long_input(self):
        """Verify the hash output length for long input."""
        # Generate 1MB of random data
        data = os.urandom(1024 * 1024)
        hash_result = custom_hash(data)
        self.assertEqual(len(hash_result), OUTPUT_LENGTH)

    def test_output_type_is_bytes(self):
        """Verify the return type is bytes."""
        data = b"test type"
        hash_result = custom_hash(data)
        self.assertIsInstance(hash_result, bytes)

    def test_determinism(self):
        """Verify hashing the same input twice yields the same output."""
        data = b"consistency check"
        hash1 = custom_hash(data)
        hash2 = custom_hash(data)
        self.assertEqual(hash1, hash2)

    def test_empty_input_consistency(self):
        """Verify hashing empty input twice yields the same output."""
        hash1 = custom_hash(b"")
        hash2 = custom_hash(b"")
        self.assertEqual(hash1, hash2)

    def test_different_inputs_produce_different_hashes(self):
        """Verify two different inputs produce different hashes."""
        data1 = b"input one"
        data2 = b"input two"
        hash1 = custom_hash(data1)
        hash2 = custom_hash(data2)
        self.assertNotEqual(hash1, hash2)

    def test_sensitivity_small_change_at_start(self):
        """Verify a small change at the start of input changes the hash."""
        data1 = b"Slight difference test"
        data2 = b"slight difference test" # Case change
        hash1 = custom_hash(data1)
        hash2 = custom_hash(data2)
        self.assertNotEqual(hash1, hash2, "Case change at start did not change hash")

    def test_sensitivity_small_change_at_end(self):
        """Verify a small change at the end of input changes the hash."""
        data1 = b"Testing small change at the end."
        data2 = b"Testing small change at the end!" # Punctuation change
        hash1 = custom_hash(data1)
        hash2 = custom_hash(data2)
        self.assertNotEqual(hash1, hash2, "Change at end did not change hash")

    def test_sensitivity_length_change(self):
        """Verify changing the length slightly changes the hash."""
        data1 = b"Length test"
        data2 = b"Length test." # Added one character
        hash1 = custom_hash(data1)
        hash2 = custom_hash(data2)
        self.assertNotEqual(hash1, hash2, "Length change did not change hash")

    def test_input_type_validation(self):
        """Verify non-bytes input raises TypeError."""
        with self.assertRaises(TypeError):
            custom_hash("this is a string, not bytes")
        with self.assertRaises(TypeError):
            custom_hash(12345)
        with self.assertRaises(TypeError):
            custom_hash([1, 2, 3]) # list of ints

    def test_known_value_empty(self):
        """Test against a pre-computed hash for empty input (if stable)."""
        expected_hash_hex = "4b96f53bc7c8fbe7b188792cc9e2848de6849176692eac1fa716c182a4fa7c9e"
        self.assertEqual(custom_hash(b"").hex(), expected_hash_hex)

    def test_known_value_simple(self):
        """Test against a pre-computed hash for a simple string."""
        expected_hash_hex = "d3d34411d67b4fdf7a3503d82f164ed3c12593fa8b8a42155ee1efb6e6a2f4f7" # Calculated for b"abc"
        self.assertEqual(custom_hash(b"abc").hex(), expected_hash_hex)

    def test_null_byte_input(self):
        """Test input containing null bytes."""
        data1 = b"test\x00data"
        data2 = b"test\x01data"
        hash1 = custom_hash(data1)
        hash2 = custom_hash(data2)
        self.assertNotEqual(hash1, hash2, "Input with null bytes not handled correctly")
        self.assertEqual(len(hash1), OUTPUT_LENGTH)

    def test_single_byte_input(self):
        """Test hashing a single byte."""
        data = b"\x42"
        hash_result = custom_hash(data)
        self.assertEqual(len(hash_result), OUTPUT_LENGTH)
        # Check if different single bytes produce different hashes
        hash_other = custom_hash(b"\x43")
        self.assertNotEqual(hash_result, hash_other)


if __name__ == '__main__':
    unittest.main()