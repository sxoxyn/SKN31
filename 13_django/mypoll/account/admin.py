from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# 사용자 정의 UserAdmin 정의
## 관리자 앱에서 User의 어떤 항목(Field)들을 관리할지 정의
## UserAdmin을 상속 받아 구현하며, register()에 USerModel과 함께 전달

## Class 변수로 Field 정의
### list_display: list - 사용자 메인화면에서 사용자 목록에 보여줄 항목
### add_fieldsets: tuple - 등록 화면에 나올 항목(Field) 정의
### fieldsets: tuple - 수정 화면에 나올 항목 정의(형식: add_fieldsets와 동일)

class CustomUserAdmin(UserAdmin):
    list_display = ["username", "name", "email"]
    # ("카테고리 이름", {"fields": (Field이름, ...)})
    add_fieldsets = (
        ("인증 정보", {"fields": ("username", "password", "password2")}),
        ("개인 정보", {"fields": ("name", "email", "birthday")}),
        ("권한", {"fields": ("is_staff", "is_active")})
    )
    fieldsets = (
        ("인증 정보", {"fields": ("username", "password")}),
        ("개인 정보", {"fields": ("name", "email", "birthday")}),
        ("권한", {"fields": ("is_staff", "is_active", "is_superuser")})
    )

admin.site.register(CustomUser, CustomUserAdmin)

