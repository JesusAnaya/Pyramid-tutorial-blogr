import shutil
import tempfile
import os


class BaseFilesStorage(object):
    settings = {}
    temp_path = ''

    def __init__(self, settings=None):
        self.settings = settings or BaseFilesStorage.settings
        self.base_path = self.settings.get('storage.base_path')
        self.base_url = self.settings.get('storage.base_url')

    def save_temp_file(self, file, filename):
        self.temp_path = tempfile.mkdtemp()
        temp_file_path = os.path.join(self.temp_path, filename)
        input_file = file

        input_file.seek(0)
        with open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)

        return temp_file_path

    def create_destination_folder(self, related_folder_path):
        pass

    def save_file(self, file, file_path):
        pass

    def get_file_url(self, related_path):
        return '{0}{1}'.format(self.base_url, related_path)

    def clean(self):
        shutil.rmtree(self.temp_path)
