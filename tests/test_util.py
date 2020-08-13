import os
import jupytext as jp
from md2canvas.util import strip_cells

def test_strip_cells():
    in_file = "examples/sample_quiz/SampleQuiz.md"
    out_file = "examples/sample_quiz/SampleQuizStripped.md"
    ret_obj = strip_cells(in_file, out_file, "answer")
    file_obj = jp.readf(out_file)
    assert len(ret_obj["cells"]) == len(file_obj["cells"])
    os.remove(out_file)
                    