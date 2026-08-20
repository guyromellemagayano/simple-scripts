"""Tests for the password generator utility."""

import string
import unittest

from python.utils.password_generator import generate_password


class PasswordGeneratorTests(unittest.TestCase):
    def test_default_password_has_required_length_and_characters(self) -> None:
        password = generate_password()

        self.assertEqual(len(password), 8)
        self.assertTrue(any(character in string.ascii_lowercase for character in password))
        self.assertTrue(any(character in string.ascii_uppercase for character in password))
        self.assertTrue(any(character in string.digits for character in password))
        self.assertTrue(any(character in string.punctuation for character in password))

    def test_password_length_is_within_requested_range(self) -> None:
        for _ in range(25):
            password = generate_password(min_length=8, max_length=20)
            self.assertGreaterEqual(len(password), 8)
            self.assertLessEqual(len(password), 20)

    def test_custom_character_sets_are_used(self) -> None:
        password = generate_password(
            lower_set="a",
            upper_set="B",
            num_set="3",
            sym_set="!",
        )

        self.assertEqual(set(password), {"a", "B", "3", "!"})

    def test_rejects_minimum_length_below_eight(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "Minimum length must be between 8 and 256 characters"
        ):
            generate_password(min_length=7)

    def test_rejects_maximum_length_below_minimum(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "Maximum length must be between 8 and 256 characters"
        ):
            generate_password(min_length=8, max_length=7)

    def test_rejects_maximum_length_above_limit(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "Maximum length must be between 8 and 256 characters"
        ):
            generate_password(min_length=8, max_length=257)

    def test_rejects_empty_character_sets(self) -> None:
        with self.assertRaisesRegex(ValueError, "Character sets must not be empty"):
            generate_password(lower_set="")


if __name__ == "__main__":
    unittest.main()
