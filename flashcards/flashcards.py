import random
import json
from colorama import init, Fore, Style


# coloroma initilization
init()

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

    def create_box(self, question, answer, topic, index, result_symbol=None, result_color=None):
        content_width = max(
            len(f"Question: {question}"),
            len(f"Answer: {answer}"),
            len(f"Topic: {topic}")
        ) + 4  # padding

        def format_line(label, content, color):
            return f"{Fore.CYAN}║{Fore.WHITE} {label}:{color} {content}{' ' * (content_width - len(f'{label}: {content}') - 1)}{Fore.CYAN}║{Style.RESET_ALL}"

        symbol_str = f" {result_color}{result_symbol}{Style.RESET_ALL}" if result_symbol else ""

        box = [
            f"{Fore.CYAN}╔{'═' * content_width}╗{symbol_str}{Style.RESET_ALL}",
            f"{Fore.CYAN}║{Fore.WHITE}{f' #{index}'.center(content_width)}{Fore.CYAN}║{Style.RESET_ALL}",
            f"{Fore.CYAN}║{Fore.WHITE}{'─' * content_width}{Fore.CYAN}║{Style.RESET_ALL}",
            format_line("Question", question, Fore.GREEN),
            format_line("Answer", answer, Fore.YELLOW),
            format_line("Topic", topic, Fore.MAGENTA),
            f"{Fore.CYAN}╚{'═' * content_width}╝{Style.RESET_ALL}"
        ]
        return '\n'.join(box)

    def view_flashcards(self):
        if not self.flashcards:
            print("No flashcards available.")
            return None

        print("\nCurrent Flashcards:")
        for i, flashcard in enumerate(self.flashcards, 1):
            print(f"{i}. Topic: {flashcard.topic}")
            print(self.create_box(flashcard.question, flashcard.answer, flashcard.topic, i))
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

        # Get and display available topics
        available_topics = sorted(set(card.topic for card in self.flashcards))
        print("\nAvailable Topics:")
        print("Press Enter for all topics")
        for i, topic in enumerate(available_topics, 1):
            print(f"{i}. {topic}")

        # Get topic selection from user
        while True:
            try:
                choice = input("\nSelect topic number (or press Enter for all topics): ").strip()
                if not choice:  # Handle empty input (Enter key)
                    selected_topic = None
                    break

                choice = int(choice)
                if 1 <= choice <= len(available_topics):
                    selected_topic = available_topics[choice - 1]
                    break
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

        if selected_topic:
            quiz_cards = [card for card in self.flashcards if card.topic.lower() == selected_topic.lower()]
            print(f"\nStarting quiz for topic: {selected_topic}")
        else:
            quiz_cards = self.flashcards.copy()
            print("\nStarting quiz for all topics")

        random.shuffle(quiz_cards)
        print(f"Number of questions: {len(quiz_cards)}")

        quiz_results = []
        score = 0

        for i, flashcard in enumerate(quiz_cards, 1):
            print(f"\nQuestion {i}/{len(quiz_cards)}")
            print(f"Topic: {flashcard.topic}")
            print(f"Question: {flashcard.question}")
            user_answer = input("Your Answer: ").strip()
            is_correct = user_answer.lower() == flashcard.answer.lower()
            if is_correct:
                print(f"{Fore.GREEN}Correct!{Style.RESET_ALL}")
                score += 1
            else:
                print(f"{Fore.RED}Incorrect. The correct answer is: {flashcard.answer}{Style.RESET_ALL}")
            quiz_results.append((flashcard, is_correct))

        self.history_stack.append({
            'score': score,
            'total': len(quiz_cards),
            'results': quiz_results
        })

        percentage = (score / len(quiz_cards)) * 100
        print("\nQuiz completed!")
        print(f"Your score: {score}/{len(quiz_cards)} ({percentage:.1f}%)")

    def review_history(self):
        if not self.history_stack:
            print("No quiz history to review.")
            return None

        print("\nFlashcard History (Most Recent First):")
        for quiz_num, quiz_session in enumerate(reversed(self.history_stack), 1):
            score = quiz_session['score']
            total = quiz_session['total']
            percentage = (score / total) * 100

            print(f"\n{Fore.CYAN}═══ Quiz #{quiz_num} ═══{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Score: {score}/{total} ({percentage:.1f}%){Style.RESET_ALL}")
            print(f"{Fore.WHITE}Flashcards from this quiz:{Style.RESET_ALL}\n")

            for i, (flashcard, is_correct) in enumerate(quiz_session['results'], 1):
                result_color = Fore.GREEN if is_correct else Fore.RED
                result_symbol = "✓" if is_correct else "✗"
                print(self.create_box(flashcard.question, flashcard.answer, flashcard.topic, i, result_symbol, result_color))
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
            quiz.save_flashcards("out/" + filename + ".json")

        case 7:
            filename = input("Enter the filename to load flashcards: ")
            quiz.load_flashcards("out/" + filename + ".json")

        case 8:
            quiz.clear_quiz_history()

        case 9:
            print("Exiting the app.")
            break

        case _:
            print("Invalid choice. Please select a valid option.")
