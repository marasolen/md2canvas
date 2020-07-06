import canvasapi as cv

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
    for group in quiz["groups"]:
        if group["questions"] is []:
            continue
        group_attrs = [group["attrs"]]
        if group["attrs"]["name"].lower() != "general":
            canvas_group = canvas_quiz.create_question_group(group_attrs)
        for question in group["questions"]:
            if group["attrs"]["name"].lower() != "general":
                question["quiz_group_id"] = canvas_group.id
            canvas_quiz.create_question(question=question)

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