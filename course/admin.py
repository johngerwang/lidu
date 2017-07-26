# -*- utf:utf-8 -*-
from django.contrib import admin
from django.db import models
from markdownx.admin import MarkdownxModelAdmin
from markdownx.widgets import AdminMarkdownxWidget

from course.models import Feature, Category, Teacher, Course


class FeatureInline(admin.StackedInline):
    model = Feature

    def get_extra(self, request, obj=None, **kwargs):
        extra = 3
        if obj:
            return extra - obj.feature_set.count()
        return extra


class TeacherAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields': ['username']}),
        ('password', {'fields': ['password']}),
        ('Resume Infomation', {'fields': ['resume']})
    ]
    inlines = [FeatureInline]


admin.site.register(Teacher, TeacherAdmin)


class CategoryInline(admin.StackedInline):
    model = Category
    extra = 1

    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        if obj:
            return extra - obj.category_set.count()
        return extra


class CourseAdmin(MarkdownxModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }
    fieldsets = [
        ('Cousre Name',     {'fields': ['course_name']}),
        ('Cousre Introduction',     {'fields': ['introduction']}),
        ('Teacher Name',    {'fields': ['teacher']}),
        ('Content',         {'fields': ['content']}),
        # ('Publish Date',    {'fields': ['pub_date']}),
        ('Publish?',        {'fields': ['published']})
        # ('Advertise Image', {'fields': ['ad_image']})
    ]
    inlines = [CategoryInline]

    def save_model(self, request, obj, form, change):
        print request.user
        print obj
        print change
        print obj.teacher
        if obj.teacher is None:
            obj.teacher = request.user
        obj.save()


admin.site.register(Course, CourseAdmin)
