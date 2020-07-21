import os
import re
import json
import jupytext as jp
from jupytext.cli import jupytext
from dateutil.parser import parse
import urllib.parse as parseurl
from datetime import datetime
import md2canvas.util as ut
import markdown
from bs4 import BeautifulSoup

md = markdown.Markdown()

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

def parse_md_text(text):
    """
    Parse markdown into HTML, also check for latex.
 
    Parameters
    ----------
    text: str
        text to parse

    Returns
    -------
    str
        parsed text with Canvas latex

    [str]
        list of paths to images linked from this text
    """
    text = md.convert(text)

    html = BeautifulSoup(text, 'html.parser')
    image_paths = []

    for image in html.find_all("img"):
        image_name = image.get("src")
        image_path = os.path.join(file_dir, image.get("src"))
        image_path = os.path.abspath(image_path)

        if os.path.islink(image_path): continue
        if not os.path.exists(image_path):
            ut.sprint("WARNING: image was not a link and does not exist on this computer: " +
                    image_path)

        image_paths += [{"name": image_name, "path": image_path}]

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

    return text.replace("\\", ""), image_paths

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
    print(weight)
    if isinstance(weight, bool):
        if weight: return 100
        else: return 0
    elif isinstance(weight, int):
        return weight
    else:
        return -1

def parse_list(text):
    """
    Parse text for list elements.

    Parameters
    ----------
    text: str
        text to parse

    Returns
    -------
    [str]
        the separated list elements
    """
    arr = []
    for line in text.split("\n"):
        if line.startswith("* "):
            arr.append(line[1:].strip(" "))

    return arr

def parse_answerless_question(q_name, index):
    """
    Function for dict, takes place for question types with no answers.

    Parameters
    ----------
    q_name: str
        name of the question
    
    index: int
        index of the question in cell array

    Returns
    -------
    [obj]
        parsed answers
    
    obj 
        extra attributes to add to the question
    """
    return [], {}

def parse_matching_question(q_name, index):
    """
    Parse matching question answers.

    Parameters
    ----------
    q_name: str
        name of the question
    
    index: int
        index of the question in cell array

    Returns
    -------
    [obj]
        parsed answers
    
    obj 
        extra attributes to add to the question
    """
    aindex = index + 1
    length_check = len(cells) <= aindex
    cell_type_check = cells[aindex]["metadata"]["ctype"] != "answer"

    if length_check or cell_type_check:
        raise Exception("WARNING: multiple answers question has no answer cell.")

    options = parse_list(cells[index]["source"])
    matches = parse_list(cells[index + 1]["source"])

    if len(options) <= len(matches):
        raise Exception("WARNING: matching question has mismatched answer numbers.")

    left = options[:len(matches)]
    right = options[len(matches):]
    
    incorrect = []
    image_paths = []
    for i, x in enumerate(right):
        if str(i + 1) not in matches:
            incorrect.append(x)

    matches = zip(left, matches)

    answers = []
    for (key, match) in matches:
        l = key
        r = right[int(match) - 1]

        answer = {"answer_match_left": l, "answer_match_right": r}
        answers.append(answer)

    extra = {"matching_answer_incorrect_matches": "\n".join(list(map(lambda x : x.strip(" "), incorrect))) }
    extra["image_paths"] = image_paths

    return answers, extra

def parse_multiple_answers_question(q_name, index):
    """
    Parse multiple answers question answers.

    Parameters
    ----------
    q_name: str
        name of the question
    
    index: int
        index of the question in cell array

    Returns
    -------
    [obj]
        parsed answers
    
    obj 
        extra attributes to add to the question
    """
    aindex = index + 1
    length_check = len(cells) <= aindex
    cell_type_check = cells[aindex]["metadata"]["ctype"] != "answer"

    if length_check or cell_type_check:
        raise Exception("WARNING: multiple answers question has no answer cell.")

    options = parse_list(cells[index]["source"])
    values = parse_list(cells[index + 1]["source"])

    if len(options) != len(values):
        raise Exception("WARNING: multiple answers/choice question has mismatched answer numbers.")

    pairs = zip(options, values)

    answers = []
    for (ans, val) in pairs:
        answer = {"answer_text": ans}

        if val.strip(" ").lower() == "true": weight = 100
        else: weight = 0
        answer["answer_weight"] = weight

        answers.append(answer)

    return answers, {}

def parse_multiple_choice_question(q_name, index):
    """
    Parse multiple choice question answers.

    Parameters
    ----------
    q_name: str
        name of the question
    
    index: int
        index of the question in cell array

    Returns
    -------
    [obj]
        parsed answers
    
    obj 
        extra attributes to add to the question
    """
    aindex = index + 1
    length_check = len(cells) <= aindex
    cell_type_check = cells[aindex]["metadata"]["ctype"] != "answer"

    if length_check or cell_type_check:
        raise Exception("WARNING: multiple choice question has no answer cell.")

    answers, extra = parse_multiple_answers_question(q_name, index)

    def check_weight(weight):
        if weight == -1 or (weight != 0 and weight != 100):
            ut.sprint("WARNING: Invalid answer weight for multiple choice question: " + str(weight))
            return False
        return True

    found_true = False
    final_answers = []
    for answer in answers:
        weight = answer["answer_weight"]
        if not check_weight(weight):
            ut.sprint("WARNING: invalid weight in answer list for question " + q_name)
            continue

        if weight > 0:
            if found_true:
                ut.sprint("WARNING: multiple correct answers in question " + q_name +
                ", consider changing to multiple answers questions")
                continue
            else:
                found_true = True
        
        final_answers += [answer]

    return final_answers, extra
    

def parse_numerical_question(q_name, index):
    """
    Parse numerical question answers.

    Parameters
    ----------
    q_name: str
        name of the question
    
    index: int
        index of the question in cell array

    Returns
    -------
    [obj]
        parsed answers
    
    obj 
        extra attributes to add to the question
    """
    aindex = index + 1
    length_check = len(cells) <= aindex
    cell_type_check = cells[aindex]["metadata"]["ctype"] != "answer"

    if length_check or cell_type_check:
        raise Exception("WARNING: numerical question has no answer cell.")

    answers = []
    for line in cells[index + 1]["source"].split("\n"):
        if line.startswith("*"):
            v1 = 0
            v2 = 0
            answer = {"answer_text": "", "answer_weight": 100}
            text = line[1:].strip(" ")
            if "," not in text:
                if ":" in text:
                    ut.sprint("WARNING: numerical answer has one value but has answer type, " +
                          "only one of these is allowed")
                v1 = float(text)
                answer["numerical_answer_type"] = "exact_answer"
            elif ":" not in text:
                ind = text.index(",")
                v1 = float(text[:ind].strip(" "))
                v2 = float(text[ind + 1:].strip(" "))
                answer["numerical_answer_type"] = "exact_answer"
            else:
                ind = text.index(":")
                vals = text[:ind]
                answer["numerical_answer_type"] = text[ind + 1:].strip(" ").replace("-", "_")
                ind = vals.index(",")
                v1 = float(vals[:ind].strip(" "))
                v2 = float(vals[ind + 1:].strip(" "))

            if answer["numerical_answer_type"] == "exact_answer":
                answer["answer_exact"] = v1
                answer["answer_error_margin"] = v2
            elif answer["numerical_answer_type"] == "range_answer":
                answer["answer_range_start"] = v1
                answer["answer_range_end"] = v2
            elif answer["numerical_answer_type"] == "precision_answer":
                answer["answer_approximate"] = v1
                answer["answer_precision"] = v2
            else:
                ut.sprint("WARNING: numerical answer type not supported: " + answer["numerical_answer_type"])
                continue

            answers += [answer]
                    
    return answers, {}

def parse_short_answer_question(q_name, index):
    """
    Parse short answer question answers.

    Parameters
    ----------
    q_name: str
        name of the question
    
    index: int
        index of the question in cell array

    Returns
    -------
    [obj]
        parsed answers
    
    obj 
        extra attributes to add to the question
    """
    aindex = index + 1
    length_check = len(cells) <= aindex
    cell_type_check = cells[aindex]["metadata"]["ctype"] != "answer"

    if length_check or cell_type_check:
        raise Exception("WARNING: short answer question has no answer cell.")

    answers = []
    for line in cells[aindex]["source"].split("\n"):
        if line.startswith("*"):
            text = line[1:].strip(" ")
            answers += [{"answer_text": text}]
                    
    return answers, {}

def parse_true_false_question(q_name, index):
    """
    Parse true/false question answers.

    Parameters
    ----------
    q_name: str
        name of the question
    
    index: int
        index of the question in cell array

    Returns
    -------
    [obj]
        parsed answers
    
    obj 
        extra attributes to add to the question
    """
    aindex = index + 1
    length_check = len(cells) <= aindex
    cell_type_check = cells[aindex]["metadata"]["ctype"] != "answer"

    if length_check or cell_type_check:
        raise Exception("WARNING: true/false question has no answer cell.")

    true_ans = {
        "answer_text": "True",
        "answer_weight": 0
    }
    false_ans = {
        "answer_text": "False",
        "answer_weight": 0
    }
    
    if "true" in cells[index + 1]["source"].lower():
        true_ans["answer_weight"] = 100
    else:
        false_ans["answer_weight"] = 100

    return [true_ans, false_ans], {}


supp_q_types = {"essay_question": {"parser": parse_answerless_question}, 
                "file_upload_question": 
                    {"parser": parse_answerless_question,
                     "warning": "File Upload questions do not work in preview mode."}, 
                "matching_question": {"parser": parse_matching_question},
                "multiple_answers_question": {"parser": parse_multiple_answers_question}, 
                "multiple_choice_question": {"parser": parse_multiple_choice_question},
                "numerical_question": {"parser": parse_numerical_question},
                "short_answer_question": {"parser": parse_short_answer_question}, 
                "text_only_question": {"parser": parse_answerless_question}, 
                "true_false_question": 
                    {"parser": parse_true_false_question,
                     "warning": "API does not support true/false questions, converting to multiple choice"}}

def parse_question(index):
    """
    Parse Question.

    Parameters
    ----------
    index: int
        index of the question in cell array

    Returns
    -------
    obj
        parsed question
    """
    question = {}
    
    for key, val, in cells[index]["metadata"].items():
        if key == "ctype":
            continue
        elif key == "quesnum":
            question["question_name"] = str(val)
        else:
            question[key] = val
            
    if "question_type" not in question:
        ut.sprint("WARNING: question does not have question-type, not including question")
        return None

    if "points_possible" not in question:
        question["points_possible"] = 1

    q_type = question["question_type"]

    if q_type not in supp_q_types:
        ut.sprint("WARNING: unsupported question type of " + q_type)
        return None

    if "warning" in supp_q_types[q_type]:
        ut.sprint("WARNING: " + supp_q_types[q_type]["warning"])
    
    try:
        question["answers"], extra = supp_q_types[q_type]["parser"](question["question_name"], index)
    except Exception as e:
        ut.sprint(str(e))
        return None

    question_text, image_paths = parse_md_text(cells[index]["source"])
    question["question_text"] = question_text
    extra["image_paths"] = image_paths
    question = {**question, **extra}

    return question

def parse_group(group_index):
    """
    Parse Question Group.

    Parameters
    ----------
    group_index: int
        index of the group in cell array

    Returns
    -------
    obj
        parsed group
    """
    group = {"attrs": {}, "questions": []}
    
    for key, val, in cells[group_index]["metadata"].items():
        if key == "ctype":
            continue
        else:
            group["attrs"][key] = val

    for index, cell in enumerate(cells):
        if index <= group_index:
            continue
        if cell["metadata"]["ctype"] == "group":
            break
        elif cell["metadata"]["ctype"] == "question":
            question = parse_question(index)
            group["questions"].append(question)

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
    global file_dir
    file_dir = os.path.dirname(os.path.abspath(nb_file))
    
    if nb_file.endswith(".json"):
        ut.pprint(nb_file)
        return json.load(nb_file)
    elif nb_file.endswith(".ipynb"):
        jupytext(args=[str(nb_file), "--to", "md:myst"])
        nb_file = nb_file.replace(".ipynb", ".md")
    nb_obj = jp.readf(nb_file)

    quiz = {"attrs": {}, "groups": []}

    global cells
    cells = nb_obj["cells"]

    start = False
    for index, cell in enumerate(cells):
        if not start and cell["metadata"]["ctype"] == "quiz":
            start = True
            desc, image_paths = parse_md_text(cell["source"])
            quiz["attrs"]["description"] = desc
            quiz["attrs"]["image_paths"] = image_paths
            for key, val, in cell["metadata"].items():
                if key == "ctype":
                    continue
                else:
                    quiz["attrs"][key] = val
        elif start and cell["metadata"]["ctype"] == "quiz":
            break
        elif start and cell["metadata"]["ctype"] == "group":
            group = parse_group(index)
            quiz["groups"].append(group)

    ut.pprint(quiz)

    return quiz
