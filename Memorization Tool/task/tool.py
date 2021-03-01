# write your code here
from random import seed
from random import randint
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

# create the db engine

engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')

Base = declarative_base()


class MyClass(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    _question = Column(String)
    _answer = Column(String)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# seed(1)

def print_main_menu():
    print("1. Add flashcards")
    print("2. Practice flashcards")
    print("3. Exit")


def print_add_flashcard_menu():
    print("1. Add a new flashcard")
    print("2. Exit")


def rng(flashcard_list):
    for _ in range(len(flashcard_list)):
        rng_value = randint(0, len(flashcard_list) - 1)
        return rng_value


flashcards = []

j = 0

while True:
    print_main_menu()

    user_input = str(input())

    if user_input == "1":
        print_add_flashcard_menu()

        user_input = str(input())

        while True:
            if user_input == "1":
                while True:
                    print("Question:")
                    question = str(input())
                    if question == "":
                        while True:
                            print("Question:")
                            question = str(input())
                            if question != "":
                                break
                    if question != "":
                        print("Answer:")
                        answer = str(input())
                        if answer == "":
                            while True:
                                print("Answer:")
                                answer = str(input())
                                if answer != "":
                                    break

                        # append question and answer to list of tuples
                        flashcards.append(tuple((question, answer)))

                        new_data = MyClass(_question=question, _answer=answer)
                        session.add(new_data)
                        session.commit()

                        # result_list = session.query(MyClass).all()
                        # for i in range(len(result_list)):
                        #     print(result_list[i]._question)
                        #     print(result_list[i]._answer)
                        #     print(result_list[i].id)

                        # print the add flashcard menu again and ask for user input
                        print_add_flashcard_menu()
                        user_input = str(input())

                        # if the input is 1, the user can add a new card
                        if user_input == "1":
                            continue

                        # if the input is not 1 or 2, show menu again and ask for user input
                        elif user_input != "2":
                            print(user_input, "is not an option")
                            print_add_flashcard_menu()
                            user_input = str(input())

                    # if the user input is 2, FIRST break out of the question-answer loop
                    if user_input == "2":
                        break

            # then break out of the add flashcard menu
            elif user_input == "2":
                break

            # if the answer isnt 1 or 2 then print the flashcard menu again and ask for the user input
            else:
                print(user_input, "is not an option")
                print_add_flashcard_menu()
                user_input = str(input())

    # if the answer is 2 in the first menu, show off the flashcards stored in the list of tuples
    elif user_input == "2":
        result_list = session.query(MyClass).all()

        entries = session.query(MyClass).all()

        entry = entries

        if len(result_list) > 0:
            rng_number = rng(flashcards)
            for i in range(len(result_list)):
                print("Question:", result_list[i]._question)
                print('press "y" to see the answer:')
                print('press "n" to skip:')
                print('press "u" to update:')

                user_answer = str(input())

                if user_answer == "y":
                    print("Answer:", result_list[i]._answer)
                    print('press "y" if your answer is correct:')
                    print('press "n" if your answer is wrong:')
                    user_answer = str(input())

                    if user_answer == "y":
                        j += 1
                        if j == 3:
                            j = 0
                            session.delete(entry[i])
                            session.commit()
                        continue
                    elif user_answer == "n":
                        continue
                    else:
                        while user_answer != "y" and user_answer != "n":
                            print(user_answer, "is not an option")
                            print('press "y" if your answer is correct:')
                            print('press "n" if your answer is wrong:')
                            user_answer = str(input())

                elif user_answer == "n":
                    print('press "y" if your answer is correct:')
                    print('press "n" if your answer is wrong:')
                    user_answer = str(input())

                    if user_answer == "y":
                        j += 1
                        if j == 3:
                            j = 0
                            session.delete(entry[i])
                            session.commit()
                        continue


                elif user_answer == "u":
                    print('press "d" to delete the flashcard:')
                    print('press "e" to edit the flashcard:')
                    user_answer = str(input())

                    if user_answer == "d":
                        session.delete(entry[i])
                        session.commit()

                    elif user_answer == "e":
                        print('current question:', result_list[i]._question)
                        print('please write a new question:')
                        question = str(input())
                        entry[i]._question = question
                        print('current answer:', result_list[i]._answer)
                        print('please write a new answer:')
                        answer = str(input())
                        entry[i]._answer = answer
                        session.commit()

        # if there arent any flashcards in the list of tuples, let the user know
        else:
            print("There is no flashcard to practice!")

    # if the input is 3, end the program
    elif user_input == "3":
        print("Bye!")
        exit()

    # if the input isnt 1 2 or 3 then it is not an option, and go back to the beginning
    else:
        print(user_input, "is not an option")
