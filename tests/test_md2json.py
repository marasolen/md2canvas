from md2canvas.md2json import parse_quiz

def test_parse_quiz():
    quiz_data = parse_quiz("examples/sample_quiz/SampleQuiz.md")
    assert len(quiz_data["groups"]) == 2
    num_questions = 0
    for group in quiz_data["groups"]:
        num_questions += len(group["questions"])
    assert num_questions == 11