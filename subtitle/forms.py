import os

from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from .models import Subtitle

CONTENT_TYPES = ['image', 'video', 'smi']
FILE_EXTENSIONS = ['.psb', '.srt', '.ssa', '.ass', '.sub', '.sami', '.smil', '.smi', '.usf', '.vtt']
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB - 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = "2621440"


class SubtitleForm(forms.ModelForm):
    class Meta:
        model = Subtitle
        fields = ("user", "type", "db_id", "title", 'language', 'run_time', 'sub_file', 'comment')

    def clean_sub_file(self):
        subfile = self.cleaned_data['sub_file']
        file_type = os.path.splitext(subfile.name)[1]

        if file_type in FILE_EXTENSIONS:
            print("extension: ", file_type)
            print("matched")
            if subfile.size > int(MAX_UPLOAD_SIZE):
                raise forms.ValidationError(
                    _(u"Max Size: %s, Your file size is too big.") % (filesizeformat(subfile.size))
                )
        else:
            raise  forms.ValidationError(
                _(u"Extension Error: %s is not valid file format") %(file_type)
            )
        return subfile
