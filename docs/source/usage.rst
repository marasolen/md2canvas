.. _usage:

Installation and Usage
======================

1. Grab your canvas course ID. 

    Example: the course id is 45445 if the course URL is https://canvas.ubc.ca/courses/45445

2. Generate a new access token from Canvas

    Login to Canvas, click "Account", click "Settings", scroll down and click "New Access Token"

3. Install the package::

    pip install git+https://github.com/maracieco/md2canvas

4. Change directory to the md2canvas folder::

    cd md2canvas

5. Send a quiz to your canvas course::

    md2canvas -t <RedactedCanvasToken> -c 45445 -u https://canvas.ubc.ca examples/sample_quiz/SampleQuiz.md
