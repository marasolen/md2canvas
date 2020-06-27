import re
import json
import jupytext as jp
import canvasapi as cv
from jupytext.cli import jupytext

re_hdrtag = re.compile(r"\#{1,4}")
hdr_dict = {"#":"quiz", "##":"group", "###":"question", "####":"subq"}

def parse_answers(text):
    return []

def parse_attrs(text):
    attrs = {}
    if "\n" in text:
        attrs["title"] = text[:text.index("\n")].strip(" \s")
        text = text[text.index("\n") + 1:]
    else:
        attrs["title"] = text.strip(" \s")
        return attrs

    if "*" in text:
        attrs["description"] = text[:text.index("*")].strip(" \s\n")
        text = text[text.index("*"):]
    else:
        attrs["description"] = text.strip(" \s\n")
        return attrs

    for line in text.split("\n"):
        if line.startswith("*"):
            key = line[1:line.index(":")].strip(" \s")
            val = line[line.index(":") + 1:].strip(" \s")
            attrs[key] = val

    return attrs

def parse_question(text, question_arr):
    attrs = parse_attrs(text)
    question = {"attrs": attrs, "answers": []}
    return question

def parse_group(text, group_arr):
    attrs = parse_attrs(text)
    group = {"attrs": attrs, "questions": []}

    for index, type, text in group_arr:
        if hdr_dict[type] == "group":
            break
        elif hdr_dict[type] == "question":
            rest = group_arr[index + 1:]
            question = parse_question(text, rest)
            group["questions"].append(question)
        else:
            continue

    return group

def parse_quiz(nb_file):
    if nb_file.endswith(".ipynb"):
        jupytext(args=[str(nb_file), "--to", "md:myst"])
        nb_file = nb_file.replace(".ipynb", ".md")
    nb_obj = jp.readf(nb_file)

    quiz = {"attrs": {}, "groups": []}

    src = nb_obj['cells'][-1]["source"]
    hdrs = re_hdrtag.findall(src)
    elems = re_hdrtag.split(src)[1:]
    elems = list(map(lambda el: el.strip(), elems))
    flat_tree = list(zip(range(len(hdrs)), hdrs, elems))
    for index, type, text in flat_tree:
        if hdr_dict[type] == "quiz":
            attrs = parse_attrs(text)
            quiz["attrs"] = attrs

        elif hdr_dict[type] == "group":
            rest = flat_tree[index + 1:]
            group = parse_group(text, rest)
            quiz["groups"].append(group)
        else:
            continue

    print(print(json.dumps(quiz, indent=4)))

    return quiz

def get_course(url, token, course_id):
    canvas = cv.Canvas(url, token)
    return canvas.get_course(course_id)

def edit_quiz(quiz, canvas_quiz):
    print(quiz)
    return {}

def upload_quiz(quiz, url, token, course_id):
    canvas_quiz = get_course(url, token, course_id).create_quiz(quiz["attrs"])
    return edit_quiz(quiz, canvas_quiz)

def update_quiz(quiz, url, token, course_id, quiz_id):
    canvas_quiz = get_course(url, token, course_id).get_quiz(quiz_id)
    return edit_quiz(quiz, canvas_quiz)
