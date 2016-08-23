import colander
from storage.schemas import FileData
from deform.widget import (
    TextInputWidget, TextAreaWidget, HiddenWidget, FileUploadWidget)

class MemoryFileUploadTempStore(dict):
    def preview_url(self, uuid):
        return None


tmpstore = MemoryFileUploadTempStore()
input_widget = TextInputWidget(css_class='form-control')
text_widget = TextAreaWidget(css_class='form-control body-field')
file_widget = FileUploadWidget(tmpstore, css_class='form-control')


class BlogCreateSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(), title='Title', widget=input_widget)
    slug = colander.SchemaNode(colander.String(), missing=None, title='Slug', widget=input_widget)
    body = colander.SchemaNode(colander.String(), title='Body', widget=text_widget)
    image = colander.SchemaNode(FileData(upload_to='blog/'), missing='', title='Image', widget=file_widget)


class BlogUpdateSchema(BlogCreateSchema):
    id = colander.SchemaNode(colander.Int(), missing=None, title='ID', widget=HiddenWidget())


class TestSchema(colander.Schema):
    file = colander.SchemaNode(FileData(upload_to='test/'), title='File')
