from canvas_mock.counter import Counter
from canvas_mock.question_group import QuestionGroup
from canvas_mock.question import Question

class Quiz():
    def __init__(self, id, attrs):
        self.id = id
        self.attrs = attrs
        self.questions = []
        self.groups = []
        self.question_counter = Counter()
        self.question_group_counter = Counter()

    def get_questions(self):
        return self.questions

    def get_quiz_group(self, id):
        for g in self.groups:
            if g.id == id:
                return g

        group = QuestionGroup(id, {})
        self.groups.append(group)
        return group

    def create_question_group(self, attrs):
        group = QuestionGroup(self.question_counter.get_next_num(), attrs)
        self.groups.append(group)
        return group

    def create_question(self, question):
        question = Question(self.question_group_counter.get_next_num(), question)
        self.questions.append(question)
        return question

    def edit(self, quiz):
        self.attrs = quiz