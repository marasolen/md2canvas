from md2canvas.json2canvas import upload_quiz, update_quiz
from md2canvas.md2json import parse_quiz
import canvas_mock.canvas as cv

test_url = "test.canvas.com"
test_token = "mytoken1111222233334444"
test_course_id = "12345"

def get_parsed_sample_quiz():
    return parse_quiz("examples/sample_quiz/SampleQuiz.md")

def get_parsed_demo_quiz():
    return parse_quiz("examples/demo_quiz/DemoQuiz.md")

def test_upload_quiz():
    quiz_data = get_parsed_sample_quiz()
    course = upload_quiz(cv, quiz_data, test_url, test_token, test_course_id)
    assert course.cv.url == test_url
    assert course.cv.token == test_token
    assert course.id == test_course_id
    quiz = course.get_quiz("0")
    assert quiz.id == "0"
    assert quiz.attrs == quiz_data["attrs"]
    assert len(quiz.questions) == 11
    assert len(quiz.groups) == 1

def test_update_quiz():
    quiz_data = get_parsed_sample_quiz()
    course = upload_quiz(cv, quiz_data, test_url, test_token, test_course_id)
    assert course.cv.url == test_url
    assert course.cv.token == test_token
    assert course.id == test_course_id
    quiz = course.get_quiz("0")
    assert quiz.id == "0"
    assert quiz.attrs == quiz_data["attrs"]
    assert len(quiz.questions) == 11
    assert len(quiz.groups) == 1

    quiz_data = get_parsed_demo_quiz()
    course = update_quiz(cv, quiz_data, test_url, test_token, test_course_id, "0")
    assert course.cv.url == test_url
    assert course.cv.token == test_token
    assert course.id == test_course_id
    quiz = course.get_quiz("0")
    assert quiz.id == "0"
    assert quiz.attrs == quiz_data["attrs"]
    assert len(quiz.questions) == 4
    assert len(quiz.groups) == 0
