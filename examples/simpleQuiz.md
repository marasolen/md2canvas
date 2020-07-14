---
jupytext:
  formats: ipynb,Rmd
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

# Test Canvas Quiz
A test quiz with all supported question types and some sample metadata.

Part of [this github](https://github.com/hcolclou/myst2canvas).

Here is a picture of a flower:

![flower image](media/flower.jpg)

* allowed-attempts: 3
* scoring-policy: keep-highest
* cant-go-back: False
* shuffle-answers: False

## General
### Q1
Write your name here!

* question-type: essay-question
* points-possible: 1

### Q2
Upload a file, any file (note this will not work in preview mode)!

* question-type: file-upload-question
* points-possible: 1

### Q3
Match the same numbers to each other

* question-type: matching-question
* points-possible: 1

#### Options
* 1: 1; matching-answer-incorrect-matches: 5, 6
* 2: 2; matching-answer-incorrect-matches: 7, 8
* 3: 3; matching-answer-incorrect-matches: 9
* 4: 4; matching-answer-incorrect-matches: 10

### Q4
Choose odd numbers.

* question-type: multiple-answers-question
* points-possible: 1

#### Answers
* 1: True
* 2: False
* 3: True
* 4: False
* 5: True

### Q5
What is the correct answer?

* question-type: multiple-choice-question
* points-possible: 1

#### Options
* Not this one: False
* This one: True
* Not this one either: False
* All of the above: False

### Q6
Type "something" or "nothing".

* question-type: short-answer-question
* points-possible: 1

#### Options
* something
* nothing

### Q7
Take a break!

* question-type: text-only-question

### Q8
Select true to get full marks.

* question-type: true-false-question
* points-possible: 1

#### Correct Answer
true

## Numerical Question Group
* pick-count: 1
* question-points: 3

### Q9a
What is $2 + 2$?

* question-type: numerical-question

#### Answers
* 4
* 4, 0.1
* 4, 0.1: exact-answer
* 3.9, 4.1: range-answer
* 4, 2: precision-answer

### Q9b
What is $3 + 2$?

* question-type: numerical-question

#### Answers
* 5
* 5, 0.1
* 5, 0.1: exact-answer
* 4.9, 5.1: range-answer
* 5, 2: precision-answer

### Q9c
Evaluate the following expression. $$4 + 2$$

* question-type: numerical-question

#### Answers
* 6
* 6, 0.1
* 6, 0.1: exact-answer
* 5.9, 6.1: range-answer
* 6, 2: precision-answer