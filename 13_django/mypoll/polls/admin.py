# polls/admin.py
from django.contrib import admin

from . import models


# 관리자 앱에서 관리할 모델 등록 

admin.site.register(models.Question)
admin.site.register(models.Choice)