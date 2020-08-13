class Question():
    def __init__(self, id, attrs):
        self.id = id
        self.attrs = attrs

    def edit(self, question):
        self.attrs = question