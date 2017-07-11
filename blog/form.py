from django import forms

from blog.models import *

#联系方式表格
class ContactForm(forms.Form):
    name = forms.CharField(max_length=30,required=True)
    email = forms.EmailField(required=False)
    subject = forms.CharField(required=False)
    comments = forms.CharField(widget=forms.Textarea)
'''
注意力,form中的成员名称和html中name的名称要一一对应相同,记住!!!
'''
