import canvasapi as cv
import md2canvas.util as ut

def update_media(url, folder, media):
    """
    Add media to folder if it doesn't already exist.

    Parameters
    ----------
    url: str
        Canvas URL

    folder: obj
        Canvas course to get folder from

    quiz_id: str
        numerical ID of quiz

    Returns
    -------
    int
        ID of folder for given quiz
    """
    folder.upload(media)

    for f in folder.get_files():
        return url + "/files/" + str(f.id) + "/download?wrap=1"

    return media + "(failed to load)"

def edit_quiz(url, quiz, canvas_quiz, canvas_quiz_folder):
    """
    Update an existing quiz.

    Parameters
    ----------
    url: str
        Canvas URL

    quiz: obj
        parsed quiz data

    canvas_quiz: Quiz
        Quiz object to modify

    canvas_quiz_folder: obj
        Canvas course to get folder from

    Returns
    -------
    None
    """
    ex_groups = {}
    ex_questions = {}

    for canvas_question in canvas_quiz.get_questions():
        group_id = canvas_question.quiz_group_id

        if group_id is not None:
            canvas_group = canvas_quiz.get_quiz_group(group_id)
            ex_groups[canvas_group.name] = canvas_group

        found_question = False
        for group in quiz["groups"]:
            for question in group["questions"]:
                if question["question_name"] == canvas_question.question_name:
                    found_question = True
                    break
            if found_question:
                break
        
        if found_question:
            ex_questions[canvas_question.question_name] = canvas_question
        else:
            canvas_question.delete()
    
    for group_name, group_obj in ex_groups.items():
        group_in_use = False
        for canvas_question in canvas_quiz.get_questions():
            if canvas_question.quiz_group_id == group_obj.id:
                group_in_use = True
                break

        if not group_in_use:
            for group in quiz["groups"]:
                if group_name == group["attrs"]["name"] and len(group["questions"]) > 0:
                    group_in_use = True
                    break

        if not group_in_use:
            group_obj.delete(group_obj.id)


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
            for media in question["image_paths"]:
                new_media = update_media(url, canvas_quiz_folder, media["path"])
                question["question_text"] = question["question_text"].replace(media["name"], new_media)

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

def get_quiz_folder(course, quiz_id):
    """
    Get media folder for this quiz.

    Parameters
    ----------
    course: obj
        Canvas course to get folder from

    quiz_id: str
        numerical ID of quiz

    Returns
    -------
    int
        ID of folder for given quiz
    """
    folders = course.get_folders()
    for folder in folders:
        if folder.name.lower() == "m2c quiz media":
            for quiz_folder in folder.get_folders():
                if quiz_folder.name == quiz_id:
                    return quiz_folder
            
            quiz_folder = folder.create_folder(quiz_id)
            return quiz_folder

    gen_folder = course.create_folder("M2C Quiz Media")
    quiz_folder = gen_folder.create_folder(quiz_id)

    return quiz_folder

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
    canvas_course = get_course(url, token, course_id)
    canvas_quiz = canvas_course.create_quiz(quiz["attrs"])
    canvas_quiz_folder = get_quiz_folder(canvas_course, str(canvas_quiz.id))

    for media in quiz["attrs"]["image_paths"]:
        new_media = update_media(url, canvas_quiz_folder, media["path"])
        quiz["attrs"]["description"] = quiz["attrs"]["description"].replace(media["name"], new_media)

    canvas_quiz.edit(quiz=quiz["attrs"])
    edit_quiz(url, quiz, canvas_quiz, canvas_quiz_folder)

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
    canvas_course = get_course(url, token, course_id)
    canvas_quiz = canvas_course.get_quiz(quiz_id)
    canvas_quiz_folder = get_quiz_folder(canvas_course, str(canvas_quiz.id))
    
    for media in quiz["attrs"]["image_paths"]:
        new_media = update_media(url, canvas_quiz_folder, media["path"])
        quiz["attrs"]["description"] = quiz["attrs"]["description"].replace(media["name"], new_media)

    canvas_quiz.edit(quiz=quiz["attrs"])
    edit_quiz(url, quiz, canvas_quiz, canvas_quiz_folder)