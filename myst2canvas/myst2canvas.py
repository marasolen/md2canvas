import re
import json
import jupytext as jp
import canvasapi as cv
from jupytext.cli import jupytext
from dateutil.parser import parse
import urllib.parse as parseurl
from datetime import datetime

re_hdrtag = re.compile(r"\#{1,4}")
hdr_dict = {"#":"quiz", "##":"group", "###":"question", "####":"options"}

def pprint(obj):
    """
    Print JSON object in an easy to read format.

    Parameters
    ----------
    obj: obj
        object to print

    Returns
    -------
    None
    """
    print(json.dumps(obj, indent=4))

def to_canvas(latex, inline = False):
    """
    Convert latex to Canvas format.

    Parameters
    ----------
    latex: str
        latex string

    inline: bool
        True if latex is inline

    Returns
    -------
    str
        converted latex
    """
    model = '<img class="equation_image" title="{0}" src="/equation_images/{1}" ' + \
            'alt="Latex: {0}" data-equation-content="{0}" />' 
    out = model.format(latex.replace("&amp;","&"), \
                       parseurl.quote(parseurl.quote(latex.replace("&amp;","&"), \
                       safe="()"), safe="()&"))
    if not inline:
        out = "</p>" + out + "<p>"
    return out

def parse_latex(text):
    """
    Parse latex from text.

    Parameters
    ----------
    text: str
        text to parse

    Returns
    -------
    str
        parsed text with Canvas latex
    """
    text = "<p>" + text + "</p>"

    begin = 0
    while text.find("$$", begin) != -1:
        start = text.find("$$", begin)
        if start - 1 >= 0 and text[start - 1] == "\\":
            begin += 2
            continue
        end = text.find("$$", start + 2)
        if end == -1:
            break
        
        latex_str = to_canvas(text[start + 2:end])
        text = text.replace(text[start:end + 2], latex_str)
        begin += len(latex_str)

    begin = 0
    while text.find("$", begin) != -1:
        start = text.find("$", begin)
        if start - 1 >= 0 and text[start - 1] == "\\":
            begin += 1
            continue
        end = text.find("$", start + 1)
        if end == -1:
            break
        
        latex_str = to_canvas(text[start + 1:end], True)
        text = text.replace(text[start:end + 1], latex_str)
        begin += len(latex_str)

    return text.replace("\\", "")

def parse_value(val):
    """
    Parse value.

    Parameters
    ----------
    val: str
        value to parse

    Returns
    -------
    int/bool/datetime/str
        parsed value
    """
    if val.isnumeric():
        return int(val)
    elif val == "True":
        return True
    elif val == "False":
        return False
    else:
        try:
            datetime = parse(val)
            return datetime
        except ValueError:
            pass

    return val
    

def parse_attrs(text, title_name="title", desc_name="description"):
    """
    Parse metadata.

    Parameters
    ----------
    text: str
        metadata

    title_name: str
        dict key for title

    desc_name: str
        dict key for description

    Returns
    -------
    obj
        parsed metadata
    """
    attrs = {}
    if "\n" in text:
        attrs[title_name] = text[:text.index("\n")].strip(" ")
        text = text[text.index("\n") + 1:]
    else:
        attrs[title_name] = text.strip(" ")
        return attrs

    if "*" in text:
        attrs[desc_name] = parse_latex(text[:text.index("*")].strip(" \n"))
        text = text[text.index("*"):]
    else:
        attrs[desc_name] = text.strip(" \n")
        return attrs

    for line in text.split("\n"):
        if line.startswith("*"):
            key = line[1:line.index(":")].strip(" ").replace("-", "_")
            val = line[line.index(":") + 1:].strip(" ").replace("-", "_")
            attrs[key] = parse_value(val)

    return attrs

def parse_weight(weight):
    """
    Convert weight to int.

    Parameters
    ----------
    weight: bool/int
        weight to convert

    Returns
    -------
    int
        converted weight
    """
    if isinstance(weight, bool):
        if weight: return 100
        else: return 0
    elif isinstance(weight, int):
        return weight
    else:
        return -1

def parse_calculated_question(options):
    """
    Parse calculated question answers.

    Parameters
    ----------
    options: str
        metadata and answer list

    Returns
    -------
    [obj]
        parsed answers
    """
    return parse_multiple_choice_question(options)

def parse_fill_in_multiple_blanks_question(options):
    """
    Parse fill in multiple blanks question answers.

    Parameters
    ----------
    options: str
        metadata and answer list

    Returns
    -------
    [obj]
        parsed answers
    """
    return []

def parse_matching_question(options):
    """
    Parse matching question answers.

    Parameters
    ----------
    options: str
        metadata and answer list

    Returns
    -------
    [obj]
        parsed answers
    """
    return []

def parse_multiple_answers_question(options):
    """
    Parse multiple answers question answers.

    Parameters
    ----------
    options: str
        metadata and answer list

    Returns
    -------
    [obj]
        parsed answers
    """
    return []

def parse_multiple_choice_question(options):
    """
    Parse multiple choice question answers.

    Parameters
    ----------
    options: str
        metadata and answer list

    Returns
    -------
    [obj]
        parsed answers
    """
    answers = []
    attrs = parse_attrs(options, title_name="UNUSED", desc_name="UNUSED")
    for key, val in attrs.items():
        if key == "UNUSED":
            continue
        answer = {"answer_text": parse_latex(key)}
        ans_attrs = []

        def check_weight(weight):
            if weight == -1 or (weight != 0 and weight != 100):
                print("Invalid answer weight for multiple choice question: " + str(val))
                return False
            return True

        if isinstance(val, str):
            arr = val.split(";")
            weight = arr[0].strip(" ")
            ans_attrs = arr[1:]
            val = parse_value(weight)

        weight = parse_weight(val)
        if not check_weight(weight):
            continue
        answer["answer_weight"] = weight

        for ans_attr in ans_attrs:
            ans_key = ans_attr[1:ans_attr.index(":")].strip(" ").replace("-", "_")
            ans_val = ans_attr[ans_attr.index(":") + 1:].strip(" ").replace("-", "_")
            answer[ans_key] = parse_value(ans_val)

        answers += [answer]

    return answers

def parse_multiple_dropdowns_question(options):
    """
    Parse multiple dropdowns question answers.

    Parameters
    ----------
    options: str
        metadata and answer list

    Returns
    -------
    [obj]
        parsed answers
    """
    return []

def parse_numerical_question(options):
    """
    Parse numerical question answers.

    Parameters
    ----------
    options: str
        metadata and answer list

    Returns
    -------
    [obj]
        parsed answers
    """
    return []

def parse_question(text, question_arr):
    """
    Parse Question.

    Parameters
    ----------
    text: str
        metadata for the question

    question_arr: [obj]
        list of the following objects in the quiz

    Returns
    -------
    obj
        parsed question
    """
    attrs = parse_attrs(text, title_name="question_name", desc_name="question_text")
    q_type = attrs["question_type"]
    if len(question_arr) == 0:
        return attrs

    options = question_arr[0][1]
    if q_type == "calculated_question":
        print("WARNING: API does not support calculated/formula questions, converting to multiple choice")
        attrs["answers"] = parse_calculated_question(options)
    elif q_type == "fill_in_multiple_blanks_question":
        attrs["answers"] = parse_fill_in_multiple_blanks_question(options)
    elif q_type == "matching_question":
        attrs["answers"] = parse_matching_question(options)
    elif q_type == "multiple_answers_question":
        attrs["answers"] = parse_multiple_answers_question(options)
    elif q_type == "multiple_choice_question":
        attrs["answers"] = parse_multiple_choice_question(options)
    elif q_type == "multiple_dropdowns_question":
        attrs["answers"] = parse_multiple_dropdowns_question(options)
    elif q_type == "numerical_question":
        attrs["answers"] = parse_numerical_question(options)
    elif q_type == "true_false_question":
        print("WARNING: API does not support true/false questions, converting to multiple choice")
        attrs["answers"] = parse_multiple_choice_question(options)
        attrs["question_type"] = "multiple_choice_question"

    return attrs

def parse_group(text, group_arr):
    """
    Parse Question Group.

    Parameters
    ----------
    text: str
        metadata for the group

    group_arr: [obj]
        list of the following objects in the quiz

    Returns
    -------
    obj
        parsed group
    """
    attrs = parse_attrs(text, title_name="name")
    group = {"attrs": attrs, "questions": []}

    for index, (obj_type, text) in enumerate(group_arr):
        if hdr_dict[obj_type] == "group":
            break
        elif hdr_dict[obj_type] == "question":
            rest = group_arr[index + 1:]
            question = parse_question(text, rest)
            group["questions"].append(question)
        else:
            continue

    return group

def parse_quiz(nb_file):
    """
    Parse quiz at given file path.

    Parameters
    ----------
    nb_file: str
        path to quiz file to parse

    Returns
    -------
    obj
        parsed quiz
    """
    if nb_file.endswith(".json"):
        pprint(nb_file)
        return json.load(nb_file)
    elif nb_file.endswith(".ipynb"):
        jupytext(args=[str(nb_file), "--to", "md:myst"])
        nb_file = nb_file.replace(".ipynb", ".md")
    nb_obj = jp.readf(nb_file)

    quiz = {"attrs": {}, "groups": []}

    src = nb_obj["cells"][-1]["source"]
    hdrs = re_hdrtag.findall(src)
    elems = re_hdrtag.split(src)[1:]
    elems = list(map(lambda el: el.strip(), elems))
    flat_tree = list(zip( hdrs, elems))
    for index, (obj_type, text) in enumerate(flat_tree):
        if hdr_dict[obj_type] == "quiz":
            attrs = parse_attrs(text)
            quiz["attrs"] = attrs

        elif hdr_dict[obj_type] == "group":
            rest = flat_tree[index + 1:]
            group = parse_group(text, rest)
            quiz["groups"].append(group)
        else:
            continue

    pprint(quiz)

    return quiz

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
