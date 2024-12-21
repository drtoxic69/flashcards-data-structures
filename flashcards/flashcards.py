import random
import json
from colorama import init, Fore, Style

init()

def create_box(question, answer, topic, index):
    # Calculate the width based on the longest content
    content_width = max(
        len(f"Question: {question}"),
        len(f"Answer: {answer}"),
        len(f"Topic: {topic}")
    ) + 4  # Add some padding

    def format_line(label, content, color):
        return f"{Fore.CYAN}║{Fore.WHITE} {label}:{color} {content}{' ' * (content_width - len(f'{label}: {content}') - 1)}{Fore.CYAN}║{Style.RESET_ALL}"

    box = [
        f"{Fore.CYAN}╔{'═' * content_width}╗{Style.RESET_ALL}",
        f"{Fore.CYAN}║{Fore.WHITE}{f' #{index}'.center(content_width)}{Fore.CYAN}║{Style.RESET_ALL}",
        f"{Fore.CYAN}║{Fore.WHITE}{'─' * content_width}{Fore.CYAN}║{Style.RESET_ALL}",
        format_line("Question", question, Fore.GREEN),
        format_line("Answer", answer, Fore.YELLOW),
        format_line("Topic", topic, Fore.MAGENTA),
        f"{Fore.CYAN}╚{'═' * content_width}╝{Style.RESET_ALL}"
    ]
    return '\n'.join(box)

class Flashcard:
    def __init__(self, question, answer, topic):
        self.question = question
        self.answer = answer
        self.topic = topic

class FlashcardQuiz:
    def __init__(self):
        self.flashcards = []
        self.history_stack = []

    def add_flashcard(self, question, answer, topic):
        self.flashcards.append(Flashcard(question, answer, topic))
        print("Flashcard added!")

    def remove_flashcard(self, index):
        if not self.flashcards:
            print("No flashcards available to remove.")
            return None

        if 0 <= index < len(self.flashcards):
            removed_card = self.flashcards.pop(index)
            print(f"Removed flashcard: Question: {removed_card.question} | Topic: {removed_card.topic}")
        else:
            print("Invalid index. Please try again.")

    def view_flashcards(self):
        if not self.flashcards:
            print("No flashcards available.")
            return

        print("\nCurrent Flashcards:")
        for i, flashcard in enumerate(self.flashcards, 1):
            print(f"{i}. Topic: {flashcard.topic}")
            print(create_box(flashcard.question, flashcard.answer, flashcard.topic, i))
        print()

    def save_flashcards(self, filename):
        with open(filename, 'w') as file:
            json.dump([flashcard.__dict__ for flashcard in self.flashcards], file)
        print(f"Flashcards saved to {filename}")

    def load_flashcards(self, filename):
        try:
            with open(filename, 'r') as file:
                flashcards_data = json.load(file)
                self.flashcards = [Flashcard(**data) for data in flashcards_data]
            print(f"Flashcards loaded from {filename}")
        except FileNotFoundError:
            print(f"No such file: {filename}")

    def start_quiz(self):
        if not self.flashcards:
            print("No flashcards available. Add some flashcards to start the quiz!")
            return None

        random.shuffle(self.flashcards)
        print("Flashcards shuffled!")

        self.history_stack = []  # Reset the history stack
        score = 0  # Initialize score

        for flashcard in self.flashcards:
            print(f"\nQuestion: {flashcard.question}")
            user_answer = input("Your Answer: ").strip()
            if user_answer.lower() == flashcard.answer.lower():
                print("Correct!")
                score += 1
            else:
                print(f"Incorrect. The correct answer is: {flashcard.answer}")
            self.history_stack.append(flashcard)  # Push flashcard onto the stack

        print(f"\nQuiz completed! Your score: {score}/{len(self.flashcards)}")

    def review_history(self):
        if not self.history_stack:
            print("No quiz history to review.")
            return None
        print("\nFlashcard History (Last to First):")
        for i, flashcard in enumerate(reversed(self.history_stack), 1):
            print(create_box(flashcard.question, flashcard.answer, flashcard.topic, i))
            print()

    def clear_quiz_history(self):
        confirm = input("Are you sure you want to clear the quiz history? (yes/no): ").strip().lower()
        if confirm == 'yes':
            self.history_stack.clear()
            print("Quiz history cleared.")
        else:
            print("Operation cancelled.")

quiz = FlashcardQuiz()

while True:
    print("\nFlashcard Quiz App")
    print("1. Add a flashcard")
    print("2. Remove a flashcard")
    print("3. View flashcards")
    print("4. Start quiz")
    print("5. Review quiz history")
    print("6. Save flashcards")
    print("7. Load flashcards")
    print("8. Clear quiz history")
    print("9. Exit")

    choice = int(input("Choose an option (1-9): "))

    match choice:
        case 1:
            question = input("Enter the question: ")
            answer = input("Enter the answer: ")
            topic = input("Enter the topic: ")
            quiz.add_flashcard(question, answer, topic)

        case 2:
            if not quiz.flashcards:
                print("No flashcards available to remove.")
            else:
                quiz.view_flashcards()
                try:
                    index = int(input("Enter the index of the flashcard to remove (1-based): ")) - 1
                    quiz.remove_flashcard(index)
                except ValueError:
                    print("Invalid input. Please enter a number.")

        case 3:
            quiz.view_flashcards()

        case 4:
            quiz.start_quiz()

        case 5:
            quiz.review_history()

        case 6:
            filename = input("Enter the filename to save flashcards: ")
            quiz.save_flashcards(filename)

        case 7:
            filename = input("Enter the filename to load flashcards: ")
            quiz.load_flashcards(filename)

        case 8:
            quiz.clear_quiz_history()

        case 9:
            print("Exiting the app.")
            break

        case _:
            print("Invalid choice. Please select a valid option.")
