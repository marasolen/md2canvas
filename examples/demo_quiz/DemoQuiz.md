---
celltoolbar: Edit Metadata
jupytext:
  cell_metadata_filter: -all
  formats: ipynb,md:myst,py:percent
  notebook_metadata_filter: all,-toc,-latex_envs,-language_info
  text_representation:
    extension: .md
    format_name: myst
    format_version: '0.8'
    jupytext_version: 1.5.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

+++ {"ctype": "quiz", "title": "Demo Quiz", "allowed_attempts": 3, "scoring_policy": "keep_highest", "cant_go_back": false, "shuffle_answers": false}

# Test Canvas Quiz
A sample quiz for demonstrations. Includes a matching question, a multiple answer question, a short answer question, and a numerical question, as well as an image and LaTeX.

+++ {"ctype": "group", "name": "general"}

## Questions

+++ {"ctype": "question", "quesnum": 1, "question_type": "matching_question", "points_possible": 5}

### Question 1
Match the same letters to each other.

Left

* a
* b
* c
* d

Right

* a
* b
* c
* d
* e
* f

+++ {"ctype": "answer", "quesnum": 1}

Matchings

* 1
* 2
* 3
* 4

+++ {"ctype": "question", "quesnum": 2, "question_type": "multiple_answers_question"}

### Question 2
Choose the odd numbers.

* 1
* 2
* 3
* 4
* 5

+++ {"ctype": "answer", "quesnum": 2}

Answers
* True
* False
* True
* False
* True

+++ {"ctype": "question", "quesnum": 3, "question_type": "short_answer_question"}

### Question 3
Type one of the words from the following image.

![text](media/captcha.png)

+++ {"ctype": "answer", "quesnum": 3}

Answers
* overlooks
* inquiry

+++ {"ctype": "question", "quesnum": 4, "question_type": "numerical_question"}

### Question 4
Evaluate the expression $$\frac{\pi r^2}{2}$$ where $r = 2$?

Give your answer to three decimal places.

+++ {"ctype": "answer", "quesnum": 4}

* 6.283, 3: precision_answer
