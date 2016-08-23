import tempfile
import shutil
import uuid
import os
from .base import BaseFilesStorage


class LocalFilesStorage(BaseFilesStorage):

    def create_destination_folder(self, related_folder_path):
#       create destiny folder if it doesn't exist
        destination_folder = os.path.join(self.base_path, related_folder_path)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        return destination_folder

    def save_file(self, file, filename, related_path):
        temp_file_path = self.save_temp_file(file, filename)
        destination_folder = self.create_destination_folder(related_path)

        file_path = os.path.join(destination_folder, filename)
        os.rename(temp_file_path, file_path)
        self.clean()
