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

+++ {"ctype": "quiz", "allowed_attempts": 3, "scoring_policy": "keep_highest", "cant_go_back": false, "shuffle_answers": false}

# Test Canvas Quiz
A test quiz with all supported question types and some sample metadata.

Part of [this github](https://github.com/hcolclou/md2canvas).

Here is a picture of a flower:

![flower image](media/flower.jpg)

+++ {"ctype": "group", "name": "general"}

## Questions

+++ {"ctype": "question", "quesnum": 1, "question_type": "essay_question", "points_possible": 5}

### Question 1
Write your name here!

+++ {"ctype": "question", "quesnum": 2, "question_type": "file_upload_question"}

### Question 2
Upload a file, any file (note this will not work in preview mode)!

+++ {"ctype": "question", "quesnum": 3, "question_type": "matching_question"}

### Question 3
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

+++ {"ctype": "answer", "quesnum": 3}

Matchings

* 1
* 2
* 3
* 4

+++ {"ctype": "question", "quesnum": 4, "question_type": "multiple_answers_question"}

### Question 4
Choose the odd numbers.

* 1
* 2
* 3
* 4
* 5

+++ {"ctype": "answer", "quesnum": 4}

Answers
* True
* False
* True
* False
* True

+++ {"ctype": "question", "quesnum": 5, "question_type": "multiple_choice_question"}

### Question 5
What is the correct answer?

* Not this one
* This one
* Not this one either
* All of the above

+++ {"ctype": "answer", "quesnum": 5}

Answers
* False
* True
* False
* False

+++ {"ctype": "question", "quesnum": 6, "question_type": "short_answer_question"}

### Question 6
Type "something" or "nothing".

+++ {"ctype": "answer", "quesnum": 6}

Answers
* something
* nothing

+++ {"ctype": "question", "quesnum": 7, "question_type": "text_only_question"}

### Question 7
Take a break!

+++ {"ctype": "question", "quesnum": 8, "question_type": "true_false_question"}

### Question 8
Write true to get full marks.

+++ {"ctype": "answer", "quesnum": 8}

Answer

true

+++ {"ctype": "group", "name": "numerical questions", "pick_count": 1, "question_points": 3, "quesnum": 1}

## Choose One

+++ {"ctype": "question", "quesnum": 9, "question_type": "numerical_question"}

### Question 9a
What is $2 + 2$?

+++ {"ctype": "answer", "quesnum": 9}

* 4
* 4, 0.1
* 4, 0.1: exact_answer
* 3.9, 4.1: range_answer
* 4, 2: precision_answer

+++ {"ctype": "question", "quesnum": 10, "question_type": "numerical_question"}

### Question 9b
What is $3 + 2$?

+++ {"ctype": "answer", "quesnum": 10}

* 5
* 5, 0.1
* 5, 0.1: exact_answer
* 4.9, 5.1: range_answer
* 5, 2: precision_answer

+++ {"ctype": "question", "quesnum": 11, "question_type": "numerical_question"}

### Question 9c
Evaluate the following expression. $$4 + 2$$

+++ {"ctype": "answer", "quesnum": 11}

* 6
* 6, 0.1
* 6, 0.1: exact_answer
* 5.9, 6.1: range_answer
* 6, 2: precision_answer
