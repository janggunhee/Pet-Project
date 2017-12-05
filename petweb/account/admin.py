from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User, PetSpecies, PetBreed, Pet


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    # 어드민 화면에 표시되는 내용
    list_display = ['user_type', 'social_id', 'email', 'nickname', 'is_active', 'is_superuser', 'date_joined']
    # 클릭 링크
    list_display_links = ['email']
    # 순서 필터링 기준
    list_filter = ['is_superuser', 'is_active']
    # 유저 보기 필드셋
    fieldsets = (
        (None, {'fields': ('email', 'password', 'social_id')}),
        ('personal info', {'fields': ('nickname', )}),
        ('permissions', {'fields': ('is_active', 'is_superuser', 'user_type', )}),
    )
    # 유저 가입 필드셋
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'nickname', 'password1', 'password2')}
         ),
    )
    # 검색창
    search_fields = ('email', 'nickname')
    # 순서 매기기
    ordering = ('-date_joined', )
    # 이건 뭐지?
    filter_horizontal = ()


class PetSpeciesAdmin(BaseUserAdmin):
    list_display = ['pk', 'pet_type']
    list_display_links = ['pet_type']
    list_filter = ['pet_type']

    ordering = ('-pk', )
    filter_horizontal = ()


class PetBreedAdmin(BaseUserAdmin):
    list_display = ['pk', 'breeds_name', 'species']
    list_display_links = ['breeds_name']
    list_filter = ['breeds_name']

    ordering = ('-pk', )
    filter_horizontal = ()


class PetAdmin(BaseUserAdmin):
    list_display = ['pk', 'name', 'owner', 'species', 'breeds']
    list_display_links = ['name']
    list_filter = ['name', 'owner']

    ordering= ('-pk', )
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(PetSpecies, PetSpeciesAdmin)
admin.site.register(PetBreed, PetBreedAdmin)
admin.site.register(Pet, PetAdmin)
