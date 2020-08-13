from canvas_mock.counter import Counter
from canvas_mock.quiz import Quiz
from canvas_mock.folder import Folder

class Course():
    def __init__(self, id, cv):
        self.id = id
        self.cv = cv
        self.quizzes = []
        self.folders = []
        self.quiz_counter = Counter()
        print(self.quiz_counter)

    def create_quiz(self, attrs):
        quiz = Quiz(self.quiz_counter.get_next_num(), attrs)
        self.quizzes.append(quiz)
        return quiz

    def get_quiz(self, id):
        for quiz in self.quizzes:
            if quiz.id == id:
                return quiz
        quiz = Quiz(id, {})
        self.quizzes.append(quiz)
        return quiz

    def get_folders(self):
        return self.folders

    def create_folder(self, name):
        folder = Folder(name)
        self.folders.append(folder)
        return folder