import random

def play_game():
    while True:
        number_to_guess = random.randint(1, 100)
        attempts = 0
        print("\n" + "="*35)
        print("--- Welcome to Number Guessing Game ---")
        print("I have picked a number between 1 and 100.")
        print("(Type 'e' or 'exit' to quit the game)")
        print("="*35)
        
        while True:
            user_input = input("Enter your guess: ").lower().strip()
            
            # Logic to exit the game
            if user_input == 'e' or user_input == 'exit':
                print("\nThanks for playing! Goodbye!")
                return 
            
            # Check if input is a valid number
            if not user_input.isdigit():
                print("Invalid input! Please enter a number or 'e' to exit.")
                continue
                
            guess = int(user_input)
            attempts += 1

            if guess < number_to_guess:
                print("Hint: Go Higher! ↑")
            elif guess > number_to_guess:
                print("Hint: Go Lower! ↓")
            else:
                print(f"CONGRATULATIONS! You found it in {attempts} attempts. 🎉")
                break 
        
        print("\nStarting a new round...")

if __name__ == "__main__":
    play_game()
