import random
import time

DIGIT_COUNT = 4
RED_COLOR = 198
PURPLE = 207
BLUE = 33
GREEN = 118

def colored_text(text, color_code) -> str:
    """Format text with ANSI color code."""
    return f"\033[38;5;{color_code}m{text}\033[0m"

def line() -> str:
    """Return a colored separator line."""
    return colored_text("-", BLUE) * 50

def generate_number() -> list[int]:
    """Generates a random number with unique digits.
    The number does not start with zero.The length is defined by DIGIT_COUNT.
    Returns:
        list[int]: The secret number as a list of unique digits.
    """
    digits = random.sample(range(0, 10), DIGIT_COUNT)
    if digits[0] == 0:
        for i in range(1, DIGIT_COUNT):
            if digits[i] != 0:
                digits[0], digits[i] = digits[i], digits[0]
                break
    return digits

def is_valid_input(user_input: str) -> tuple[bool, list[str]]:
    """Validate the user's input and return a result and error messages.
    Args:
        user_input (str): The value provided by the player.
    Returns:
        tuple[bool, list[str]]: Validation status and list of error messages
    """
    errors = []

    if not user_input.isdigit():
        errors.append("Input must contain only digits.")
    if len(user_input) != DIGIT_COUNT:
        errors.append(f"Input must be {DIGIT_COUNT} digits long.")
    if user_input and user_input[0] == "0":
        errors.append("Number cannot start with zero.")
    if (len(set(user_input)) != len(user_input)):
        errors.append("Digits must be unique.")
    return (len(errors) == 0), errors

def pluralize(count: int, singular: str, suffix: str = "s", show_count: bool = True) -> str:
    """Returns the word in singular or plural form based on count.
    Args:
        count (int): The number to determine singular/plural.
        singular (str): The base word in singular form.
        suffix (str): Optional suffix for plural form (default is 's').
    Returns:
        str: Formatted string with count and correct word form.
    """
    word = singular if count == 1 else singular + suffix
    return f"{count} {word}" if show_count else word

def evaluate_guess(secret: list[int], guess: list[int]) -> tuple[int, int]:
    """Compares the player's guess with the secret number and returns the number of bulls and cows.
    Bulls are correct digit in correct position, Cows are correct digit in wrong position.
    Args:
        secret (list[int]): The secret number as a list of digits.
        guess (list[int]): The player's guess as a list of digits.
    Returns:
        tuple[int, int]: Number of bulls and cows.
    """ 
    bulls = 0
    cows = 0
    unmatched_secret = []
    unmatched_guess = []

    for _pos, (secret_digit, guess_digit) in enumerate(zip(secret, guess)):
        if secret_digit == guess_digit:
            bulls += 1
        else:
            unmatched_secret.append(secret_digit)
            unmatched_guess.append(guess_digit)

    for digit in unmatched_guess:
        if digit in unmatched_secret:
            cows += 1
            unmatched_secret.remove(digit)

    return bulls, cows

def play_game(user_name: str) -> None:
    """Start the Bulls and Cows game.
    Generates a secret number with unique digits,
    handles user input, evaluates guesses, tracks the number of attempts
    and measures the time taken to solve the game.
    """
    secret = generate_number()
    attempts = 0
    start_time = time.time()

    while True:
        try:
            user_input = input("Enter a number: ")
        except (KeyboardInterrupt, EOFError):
            print(colored_text("\nGame interrupted by user (Ctrl+C),\n"
            "or input ended unexpectedly (Ctrl+Z / Ctrl+D). Goodbye!", RED_COLOR))
            exit()
        
        is_valid, messages = is_valid_input(user_input)
        if not is_valid:
            for msg in messages:
                print(colored_text(msg, RED_COLOR))
            print(line())
            continue

        guess = [int(d) for d in user_input]
        attempts += 1
        darts = colored_text(">", PURPLE) * 3
        bulls, cows = evaluate_guess(secret, guess)
        print(f"{darts} {user_input}")
        print(f"{pluralize(bulls, 'bull')}, {pluralize(cows, 'cow')}")
        print(line())

        if bulls == DIGIT_COUNT:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(colored_text("Congratulations!", GREEN))
            print(line())
            print(f"Secret number is: {''.join(map(str, secret))}")
            print(f"Your {pluralize(attempts, 'attempt', show_count=False)}: {attempts}")
            print(f"Your time: {round(elapsed_time, 2)} sec.") 
            print(line())
            print(colored_text(f"{user_name} that's amazing!", GREEN))
            print(line())
            break

def main() -> None:
    """Initialize and start the game."""
    user_name = input("enter your name: ")
    print(line())
    print(f"Hi {user_name}!")
    print(line())
    print(f'''I've generated a random {DIGIT_COUNT} digit number for you.
    Let's play a bulls and cows game.''')
    print(line())
    play_game(user_name)

if __name__ == "__main__":
    main()
