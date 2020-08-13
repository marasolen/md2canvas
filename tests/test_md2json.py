from md2canvas.md2json import parse_quiz

def test_parse_quiz():
    quiz_data = parse_quiz("examples/sample_quiz/SampleQuiz.md")
    assert quiz_data["attrs"]["title"] == "Test Canvas Quiz"
    assert quiz_data["attrs"]["allowed_attempts"] == 3
    assert quiz_data["attrs"]["scoring_policy"] == "keep_highest"
    assert quiz_data["attrs"]["cant_go_back"] == False
    assert quiz_data["attrs"]["shuffle_answers"] == False
    assert len(quiz_data["groups"]) == 2
    num_questions = 0
    for group in quiz_data["groups"]:
        assert group["attrs"]["name"] == "general" or group["attrs"]["name"] == "numerical questions"
        num_questions += len(group["questions"])
    assert num_questions == 11