from canvas_mock.course import Course

class Canvas():
    def __init__(self, url, token):
        self.url = url
        self.token = token

    def get_course(self, id):
        course = Course(id, self)
        self.course = course
        return course

