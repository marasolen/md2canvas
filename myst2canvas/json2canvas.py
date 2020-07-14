import canvasapi as cv
import myst2canvas.util as ut

def edit_quiz(quiz, canvas_quiz):
    """
    Update an existing quiz.

    Parameters
    ----------
    quiz: obj
        parsed quiz data

    canvas_quiz: Quiz
        Quiz object to modify

    Returns
    -------
    None
    """
    ex_groups = {}
    ex_questions = {}

    canvas_questions = canvas_quiz.get_questions()
    for canvas_question in canvas_questions:
        ex_questions[canvas_question.question_name] = canvas_question
        group_id = canvas_question.quiz_group_id

        if group_id is not None:
            canvas_group = canvas_quiz.get_quiz_group(group_id)
            ex_groups[canvas_group.name] = canvas_group

    for group in quiz["groups"]:
        if group["questions"] is []:
            continue

        group_attrs = [group["attrs"]]
        if group["attrs"]["name"] in ex_groups:
            canvas_group = ex_groups[group["attrs"]["name"]]
            canvas_group.course_id = canvas_quiz.course_id
            canvas_group.update(canvas_group.id, group_attrs)
        elif group["attrs"]["name"].lower() != "general":
            canvas_group = canvas_quiz.create_question_group(group_attrs)

        for question in group["questions"]:
            if group["attrs"]["name"].lower() != "general":
                question["quiz_group_id"] = canvas_group.id
            
            if question["question_name"] in ex_questions:
                canvas_question = ex_questions[question["question_name"]]
                canvas_question.edit(question=question)
            else:
                canvas_quiz.create_question(question=question)

def get_course(url, token, course_id):
    """
    Retrieve Course from Canvas

    Parameters
    ----------
    url: str
        Canvas URL

    token: str
        access token

    course_id: str
        numerical ID of course

    Returns
    -------
    Course
        Course object that hosts quiz
    """
    canvas = cv.Canvas(url, token)
    return canvas.get_course(course_id)

def upload_quiz(quiz, url, token, course_id):
    """
    Upload a new quiz.

    Parameters
    ----------
    quiz: obj
        parsed quiz data

    url: str
        Canvas URL

    token: str
        access token

    course_id: str
        numerical ID of course

    Returns
    -------
    None
    """
    canvas_quiz = get_course(url, token, course_id).create_quiz(quiz["attrs"])
    edit_quiz(quiz, canvas_quiz)

def update_quiz(quiz, url, token, course_id, quiz_id):
    """
    Update an existing quiz.

    Parameters
    ----------
    quiz: obj
        parsed quiz data

    url: str
        Canvas URL

    token: str
        access token

    course_id: str
        numerical ID of course

    quiz_id: str
        numerical ID of quiz

    Returns
    -------
    None
    """
    canvas_quiz = get_course(url, token, course_id).get_quiz(quiz_id)
    canvas_quiz = canvas_quiz.edit(quiz=quiz["attrs"])
    edit_quiz(quiz, canvas_quiz)