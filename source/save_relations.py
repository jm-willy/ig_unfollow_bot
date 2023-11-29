import os
import pickle
import stat


class SaveRelations:

    def __init__(self):
        self.file_path = os.getcwd() + '/saved_rel.pickle'
        self.data = {
            'followers': [],
            'following': [],
            'unfollow': [],
        }
        return

    def load_data(self):
        try:
            os.chmod(self.file_path, stat.S_IRWXU)
            with open(self.file_path, 'rb') as file_1:
                self.data = pickle.load(file_1)
        except (FileNotFoundError, EOFError):
            with open(self.file_path, 'wb') as file_1:
                pickle.dump(self.data, file_1)
        return

    def save_data(self):
        try:
            os.chmod(self.file_path, stat.S_IRWXU)
            with open(self.file_path, 'wb') as file_1:
                pickle.dump(self.data, file_1)
        except (FileNotFoundError, EOFError):
            with open(self.file_path, 'wb') as file_1:
                pickle.dump(self.data, file_1)
        return

    def empty_data(self):
        self.data = {
            'followers': [],
            'following': [],
            'unfollow': [],
        }
        self.save_data()
        return

# s = SaveRelations()
# s.load_data()
# print((s.data['followers']))