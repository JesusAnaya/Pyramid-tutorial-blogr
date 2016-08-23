import colander
from .local import LocalFilesStorage


class FileData(object):
    def __init__(self, upload_to='', storage=None):
        self.upload_to = upload_to

        if not storage:
            self.storage = LocalFilesStorage()
        else:
            self.storage = storage

    def validate_format(self, node, value):
        pass

    def serialize(self, node, value):
        if value is colander.null:
            return colander.null
        return self.storage.get_file_url(value)

    def deserialize(self, node, value):
        if value is colander.null:
            return colander.null

        self.validate_format(node, value)
        self.storage.save_file(value.file, value.filename, self.upload_to)
        return '{0}{1}'.format(self.upload_to, value.filename)

    def cstruct_children(self, node, cstruct):
        return []
