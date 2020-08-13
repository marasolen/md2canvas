from canvas_mock.file import File
from canvas_mock.counter import Counter

class Folder():
    def __init__(self, name):
        self.name = name
        self.folders = []
        self.files = []
        self.file_counter = Counter()

    def create_folder(self, name):
        folder = Folder(name)
        self.folders.append(folder)
        return folder

    def get_folders(self):
        return self.folders

    def upload(self, media):
        f = File(self.file_counter.get_next_num(), media)
        self.files.append(f)

    def get_files(self):
        return self.files
