import time
import random

def validate_number(prompt):
    """Get and validate numeric input from user."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def get_yes_no(prompt):
    """Get a yes/no response from user."""
    while True:
        response = input(prompt).lower().strip()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        print("Please answer 'yes' or 'no'.")

def process_data(numbers):
    """Process a list of numbers with some CPU-intensive operations."""
    result = []
    for n in numbers:
        # Simulate some CPU-intensive work
        time.sleep(0.1)  # Artificial delay to show in profiler
        result.append(sum(i * i for i in range(int(n))))
    return result

def analyze_hobbies(hobbies):
    """Perform some analysis on the hobbies list."""
    # Create a dictionary with hobby lengths and randomized scores
    analysis = {}
    for hobby in hobbies:
        time.sleep(0.05)  # Artificial delay
        analysis[hobby] = {
            'length': len(hobby),
            'score': random.randint(1, 100),
            'letters': sorted(set(hobby.lower()))
        }
    return analysis

def main():
    # Basic string input
    name = input("What's your name? ")
    print(f"Hello, {name}!")
    
    # Numeric input with validation
    numbers = []
    for i in range(3):
        num = validate_number(f"Enter number {i+1}: ")
        numbers.append(num)
    
    # Process the numbers (CPU-intensive operation)
    print("\nProcessing numbers...")
    results = process_data(numbers)
    print(f"Processed results: {results}")
    
    # Yes/No input
    likes_coding = get_yes_no("Do you enjoy coding? (yes/no): ")
    if likes_coding:
        print("That's great! Keep coding!")
    else:
        print("Maybe you haven't found the right project yet!")
    
    # Creating a list from multiple inputs
    num_hobbies = int(input("\nHow many hobbies do you have? "))
    hobbies = []
    
    for i in range(num_hobbies):
        hobby = input(f"Enter hobby #{i+1}: ")
        hobbies.append(hobby)
    
    # Analyze hobbies (memory-intensive operation)
    print("\nAnalyzing hobbies...")
    hobby_analysis = analyze_hobbies(hobbies)
    
    print("\nHobby Analysis:")
    for hobby, analysis in hobby_analysis.items():
        print(f"- {hobby}:")
        print(f"  Length: {analysis['length']}")
        print(f"  Score: {analysis['score']}")
        print(f"  Unique letters: {''.join(analysis['letters'])}")

if __name__ == "__main__":
    main()