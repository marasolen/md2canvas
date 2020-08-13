import os
import jupytext as jp
from md2canvas.util import strip_cells

def test_strip_answer_cells():
    in_file = "examples/sample_quiz/SampleQuiz.md"
    out_file = "examples/sample_quiz/SampleQuizStripped.md"
    ret_obj = strip_cells(in_file, out_file, "answer")
    file_obj = jp.readf(out_file)
    assert len(ret_obj["cells"]) == 14
    assert len(file_obj["cells"]) == 14
    os.remove(out_file)

def test_strip_group_cells():
    in_file = "examples/sample_quiz/SampleQuiz.md"
    out_file = "examples/sample_quiz/SampleQuizStripped.md"
    ret_obj = strip_cells(in_file, out_file, "group")
    file_obj = jp.readf(out_file)
    assert len(ret_obj["cells"]) == 20
    assert len(file_obj["cells"]) == 20
    os.remove(out_file)
                    