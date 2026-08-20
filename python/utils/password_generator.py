"""Generate passwords containing letters, digits, and symbols."""

import secrets
import string
from typing import Optional


MINIMUM_LENGTH = 8
DEFAULT_MAXIMUM_LENGTH = 256
_RANDOM = secrets.SystemRandom()


def generate_password(
    min_length: int = MINIMUM_LENGTH,
    max_length: Optional[int] = None,
    max_length_req: int = DEFAULT_MAXIMUM_LENGTH,
    lower_set: Optional[str] = None,
    upper_set: Optional[str] = None,
    num_set: Optional[str] = None,
    sym_set: Optional[str] = None,
) -> str:
    """Return a password containing at least one character from each set.

    The returned length is selected inclusively between ``min_length`` and
    ``max_length``. When ``max_length`` is omitted, the password is exactly
    ``min_length`` characters long.
    """
    lower_set = string.ascii_lowercase if lower_set is None else lower_set
    upper_set = string.ascii_uppercase if upper_set is None else upper_set
    num_set = string.digits if num_set is None else num_set
    sym_set = string.punctuation if sym_set is None else sym_set

    if max_length is None:
        max_length = min_length

    if not MINIMUM_LENGTH <= min_length <= max_length_req:
        raise ValueError(
            "Minimum length must be between "
            f"{MINIMUM_LENGTH} and {max_length_req} characters."
        )
    if not min_length <= max_length <= max_length_req:
        raise ValueError(
            "Maximum length must be between "
            f"{min_length} and {max_length_req} characters."
        )

    character_sets = (lower_set, upper_set, num_set, sym_set)
    if any(not character_set for character_set in character_sets):
        raise ValueError("Character sets must not be empty.")

    password = [_RANDOM.choice(character_set) for character_set in character_sets]
    password_length = _RANDOM.randint(min_length, max_length)
    all_characters = "".join(character_sets)
    password.extend(
        _RANDOM.choice(all_characters)
        for _ in range(password_length - len(password))
    )
    _RANDOM.shuffle(password)

    return "".join(password)


def main() -> None:
    """Prompt for a maximum length and print a generated password."""
    try:
        maximum_length = int(
            input("Enter the maximum password length (minimum 8 characters): ")
        )
        print(generate_password(max_length=maximum_length))
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
