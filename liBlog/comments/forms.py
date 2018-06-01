from django import forms
from django.utils.translation import ugettext_lazy as _
from django_comments_xtd.conf import settings
from django_comments_xtd.forms import XtdCommentForm


class LiCommentForm(XtdCommentForm):
    def __init__(self, *args, **kwargs):
        super(LiCommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'] = forms.CharField(label='评论',
            widget=forms.Textarea(attrs={'placeholder': '支持MarkDown语法'}),
            max_length=settings.COMMENT_MAX_LENGTH)
        self.fields['followup'] = forms.BooleanField(
            required=False,
            label='有人回复接受邮件通知',
            widget=forms.CheckboxInput(attrs={'class': 'filled-in'}))
