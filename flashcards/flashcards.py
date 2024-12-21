import random


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
            print(f"{i}. Question: {flashcard.question} | Answer: {flashcard.answer} | Topic: {flashcard.topic}")
        print()


    def get_topics(self):
        return set(flashcard.topic for flashcard in self.flashcards)


    def start_quiz(self):
        if not self.flashcards:
            print("No flashcards available. Add some flashcards to start the quiz!")
            return

        topics = self.get_topics()
        print("\nAvailable Topics:")
        for topic in topics:
            print(f"- {topic}")
        print("- All (to include all topics)")

        selected_topic = input("\nEnter a topic to quiz on (or type 'All' for all topics): ").strip()
        if selected_topic.lower() != "all":
            selected_flashcards = [fc for fc in self.flashcards if fc.topic.lower() == selected_topic.lower()]
            if not selected_flashcards:
                print(f"No flashcards found for the topic '{selected_topic}'.")
                return
        else:
            selected_flashcards = self.flashcards

        # Ask if the user wants to shuffle the selected flashcards
        shuffle_choice = input("Do you want to shuffle the flashcards? (yes/no): ").strip().lower()
        if shuffle_choice == "yes":
            random.shuffle(selected_flashcards)
            print("Flashcards shuffled!")

        self.history_stack = []  # Reset the history stack
        score = 0  # Initialize score

        for flashcard in selected_flashcards:
            print(f"\nQuestion: {flashcard.question}")
            user_answer = input("Your Answer: ").strip()
            if user_answer.lower() == flashcard.answer.lower():
                print("Correct!")
                score += 1
            else:
                print(f"Incorrect. The correct answer is: {flashcard.answer}")
            self.history_stack.append(flashcard)  # Push flashcard onto the stack

        print(f"\nQuiz completed! Your score: {score}/{len(selected_flashcards)}")


    def review_history(self):
        if not self.history_stack:
            print("No quiz history to review.")
            return
        print("\nFlashcard History (Last to First):")
        for i, flashcard in enumerate(reversed(self.history_stack), 1):
            print(f"{i}. Question: {flashcard.question} | Answer: {flashcard.answer} | Topic: {flashcard.topic}")
        print()


quiz = FlashcardQuiz()

while True:
    print("\nFlashcard Quiz App")
    print("1. Add a flashcard")
    print("2. Remove a flashcard")
    print("3. View flashcards")
    print("4. Start quiz")
    print("5. Review quiz history")
    print("6. Exit")

    choice = input("Choose an option (1-6): ")

    if choice == "1":
        question = input("Enter the question: ")
        answer = input("Enter the answer: ")
        topic = input("Enter the topic: ")
        quiz.add_flashcard(question, answer, topic)
    elif choice == "2":
        quiz.view_flashcards()
        try:
            index = int(input("Enter the index of the flashcard to remove (1-based): ")) - 1
            quiz.remove_flashcard(index)
        except ValueError:
            print("Invalid input. Please enter a number.")
    elif choice == "3":
        quiz.view_flashcards()
    elif choice == "4":
        quiz.start_quiz()
    elif choice == "5":
        quiz.review_history()
    elif choice == "6":
        print("Exiting the app.")
        break
    else:
        print("Invalid choice. Please select a valid option.")
