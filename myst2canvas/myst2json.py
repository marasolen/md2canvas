import os
import re
import json
import jupytext as jp
from jupytext.cli import jupytext
from dateutil.parser import parse
import urllib.parse as parseurl
from datetime import datetime
import myst2canvas.util as ut
import markdown
from bs4 import BeautifulSoup

md = markdown.Markdown()

re_hdrtag = re.compile(r"\#{1,4}")
hdr_dict = {"#":"quiz", "##":"group", "###":"question", "####":"options"}

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

    [str]
        list of paths to images linked from this text
    
    """
    attrs = {}
    if "\n" in text:
        attrs[title_name] = text[:text.index("\n")].strip(" ")
        text = text[text.index("\n") + 1:]
    else:
        attrs[title_name] = text.strip(" ")
        return attrs, []

    if "*" in text:
        attrs[desc_name], image_paths = parse_md_text(text[:text.index("*")].strip(" \n"))
        text = text[text.index("*"):]
    else:
        attrs[desc_name], image_paths = parse_md_text(text.strip(" \n"))
        return attrs, image_paths

    for line in text.split("\n"):
        if line.startswith("*"):
            key = line[1:line.index(":")].strip(" ").replace("-", "_")
            val = line[line.index(":") + 1:].strip(" ").replace("-", "_")
            attrs[key] = parse_value(val)

    return attrs, image_paths

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

def parse_answerless_question(q_name, options):
    """
    Function for dict, takes place for question types with no answers.

    Parameters
    ----------
    q_name: str
        name of the question
    
    options: str
        metadata and answer list

    Returns
    -------
    [obj]
        parsed answers
    
    obj 
        extra attributes to add to the question
    """
    return [], {}

def parse_matching_question(q_name, options):
    """
    Parse matching question answers.

    Parameters
    ----------
    q_name: str
        name of the question
    
    options: str
        metadata and answer list

    Returns
    -------
    [obj]
        parsed answers
    
    obj 
        extra attributes to add to the question
    """
    answers = []
    extra = {}
    attrs, extra["image_paths"] = parse_attrs(options, title_name="UNUSED", desc_name="UNUSED")
    
    distractors = []
    for key, val in attrs.items():
        if key == "UNUSED":
            continue
        answer = {"answer_match_left": key}
        ans_attrs = []

        arr = val.split(";")
        answer["answer_match_right"] = arr[0].strip(" ")
        ans_attrs = arr[1:]

        for ans_attr in ans_attrs:
            ans_key = ans_attr[1:ans_attr.index(":")].strip(" ").replace("-", "_")
            ans_val = ans_attr[ans_attr.index(":") + 1:].strip(" ").replace("-", "_")
            if ans_key == "matching_answer_incorrect_matches":
                distractors += ans_val.split(",")
                continue
            answer[ans_key] = parse_value(ans_val)

        answers += [answer]

    extra["matching_answer_incorrect_matches"] = "\n".join(list(map(lambda x : x.strip(" "), distractors)))

    return answers, extra

def parse_multiple_answers_question(q_name, options):
    """
    Parse multiple answers question answers.

    Parameters
    ----------
    q_name: str
        name of the question
    
    options: str
        metadata and answer list

    Returns
    -------
    [obj]
        parsed answers
    
    obj 
        extra attributes to add to the question
    """
    answers = []
    extra = {}
    attrs, extra["image_paths"] = parse_attrs(options, title_name="UNUSED", desc_name="UNUSED")
    for key, val in attrs.items():
        if key == "UNUSED":
            continue
        answer = {"answer_text": key}
        ans_attrs = []

        if isinstance(val, str):
            arr = val.split(";")
            weight = arr[0].strip(" ")
            ans_attrs = arr[1:]
            val = parse_value(weight)

        weight = parse_weight(val)
        answer["answer_weight"] = weight

        for ans_attr in ans_attrs:
            ans_key = ans_attr[1:ans_attr.index(":")].strip(" ").replace("-", "_")
            ans_val = ans_attr[ans_attr.index(":") + 1:].strip(" ").replace("-", "_")
            answer[ans_key] = parse_value(ans_val)

        answers += [answer]

    return answers, extra

def parse_multiple_choice_question(q_name, options):
    """
    Parse multiple choice question answers.

    Parameters
    ----------
    q_name: str
        name of the question
    
    options: str
        metadata and answer list

    Returns
    -------
    [obj]
        parsed answers
    
    obj 
        extra attributes to add to the question
    """
    answers, extra = parse_multiple_answers_question(q_name, options)

    def check_weight(weight):
        if weight == -1 or (weight != 0 and weight != 100):
            print("Invalid answer weight for multiple choice question: " + str(weight))
            return False
        return True

    found_true = False
    final_answers = []
    for answer in answers:
        weight = answer["answer_weight"]
        if not check_weight(weight):
            print("WARNING: invalid weight in answer list for question " + q_name)
            continue

        if weight > 0:
            if found_true:
                print("WARNING: multiple correct answers in question " + q_name +
                ", consider changing to multiple answers questions")
                continue
            else:
                found_true = True
        
        final_answers += [answer]

    return final_answers, extra
    

def parse_numerical_question(q_name, options):
    """
    Parse numerical question answers.

    Parameters
    ----------
    q_name: str
        name of the question
    
    options: str
        metadata and answer list

    Returns
    -------
    [obj]
        parsed answers
    
    obj 
        extra attributes to add to the question
    """
    answers = []
    for line in options.split("\n"):
        if line.startswith("*"):
            v1 = 0
            v2 = 0
            answer = {"answer_text": "", "answer_weight": 100}
            text = line[1:].strip(" ")
            if "," not in text:
                if ":" in text:
                    print("WARNING: numerical answer has one value but has answer type, " +
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
                print("WARNING: numerical answer type not supported: " + answer["numerical_answer_type"])
                continue

            answers += [answer]
                    
    return answers, {}

def parse_short_answer_question(q_name, options):
    """
    Parse short answer question answers.

    Parameters
    ----------
    q_name: str
        name of the question
    
    options: str
        metadata and answer list

    Returns
    -------
    [obj]
        parsed answers
    
    obj 
        extra attributes to add to the question
    """
    answers = []
    for line in options.split("\n"):
        if line.startswith("*"):
            text = line[1:].strip(" ")
            answers += [{"answer_text": text}]
                    
    return answers, {}

def parse_true_false_question(q_name, options):
    """
    Parse true/false question answers.

    Parameters
    ----------
    q_name: str
        name of the question
    
    options: str
        metadata and answer list

    Returns
    -------
    [obj]
        parsed answers
    
    obj 
        extra attributes to add to the question
    """
    extra = {}
    attrs, extra["image_paths"] = parse_attrs(options, desc_name="answer")
    true_ans = {
        "answer_text": "True",
        "answer_weight": 0
    }
    false_ans = {
        "answer_text": "False",
        "answer_weight": 0
    }
    if "true" in attrs["answer"].lower():
        true_ans["answer_weight"] = 100
    else:
        false_ans["answer_weight"] = 100

    return [true_ans, false_ans], extra


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
    attrs, image_paths = parse_attrs(text, title_name="question_name", desc_name="question_text")
    if "question_type" not in attrs:
        print("WARNING: question does not have question-type, not including question")
        return None

    q_type = attrs["question_type"]
    if len(question_arr) == 0:
        return attrs

    options = question_arr[0][1]
    if q_type not in supp_q_types:
        print("WARNING: unsupported question type of " + q_type)
        return None

    if "warning" in supp_q_types[q_type]:
        ut.sprint("WARNING: " + supp_q_types[q_type]["warning"])
        
    attrs["answers"], extra = supp_q_types[q_type]["parser"](attrs["question_name"], options)
    extra["image_paths"] = image_paths
    attrs = {**attrs, **extra}

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
    attrs, _ = parse_attrs(text, title_name="name")
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

    src = nb_obj["cells"][-1]["source"]
    hdrs = re_hdrtag.findall(src)
    elems = re_hdrtag.split(src)[1:]
    elems = list(map(lambda el: el.strip(), elems))
    flat_tree = list(zip( hdrs, elems))
    for index, (obj_type, text) in enumerate(flat_tree):
        if hdr_dict[obj_type] == "quiz":
            attrs, image_paths = parse_attrs(text)
            attrs["image_paths"] = image_paths
            quiz["attrs"] = attrs

        elif hdr_dict[obj_type] == "group":
            rest = flat_tree[index + 1:]
            group = parse_group(text, rest)
            quiz["groups"].append(group)
        else:
            continue

    return quiz
