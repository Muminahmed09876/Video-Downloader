import random

def rps_game():
    # ম্যাপ তৈরি করা যাতে r দিলে rock বোঝায়
    choice_map = {
        'r': 'rock',
        'p': 'paper',
        's': 'scissors',
        'rock': 'rock',
        'paper': 'paper',
        'scissors': 'scissors'
    }
    
    options = ["rock", "paper", "scissors"]
    
    print("\n" + "="*35)
    print("Welcome to Rock, Paper, Scissors!")
    print("Shortcuts: r=Rock, p=Paper, s=Scissors")
    print("Type 'e' or 'exit' to quit.")
    print("="*35)

    while True:
        user_input = input("\nYour choice (r/p/s): ").lower().strip()

        if user_input == 'e' or user_input == 'exit':
            print("Thanks for playing! Bye!")
            break

        # ইউজার ইনপুট ম্যাপ থেকে চেক করা
        user_choice = choice_map.get(user_input)

        if not user_choice:
            print("Invalid choice! Use r, p, s or full names.")
            continue

        computer_choice = random.choice(options)
        print(f"You: {user_choice.capitalize()}  VS  Computer: {computer_choice.capitalize()}")

        if user_choice == computer_choice:
            print("Result: It's a Tie! 🤝")
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "paper" and computer_choice == "rock") or \
             (user_choice == "scissors" and computer_choice == "paper"):
            print("Result: You Win! 🎉")
        else:
            print("Result: Computer Wins! 🤖")

if __name__ == "__main__":
    rps_game()
