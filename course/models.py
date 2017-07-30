# -*— coding:utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from markdownx.models import MarkdownxField


class CourseManager(models.Manager):

    # 根据类目，获取course的简介，包括course的id，名字，简介，老师，用于首页展示。需要过滤掉未发布的课程
    def query_course_summary_by_category(self, category_id):
        columns = ('id', 'course_name', 'introduction',
                   'teacher', 'pub_date', 'up')
        query = self.get_queryset().filter(id=category_id).filter(
            published__exact=True).values(*columns).order_by('pub_date')
        return query

    # 根据课程id获取课程的详细介绍
    def query_course_content(self, course_id):
        query = self.get_queryset().get(id=course_id).values('content')
        return query

    def query_by_teacher(self, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        course_list = teacher.course_set.all()
        return course_list

    def query_by_time(self):
        query = self.get_queryset().order_by('pub_date')
        return query

    def query_by_keyword(self, keyword):
        query = self.get_queryset().filter(
            course_name__contains=keyword).filter(content__contains=keyword)
        return query


# 教师


@python_2_unicode_compatible
class Teacher(AbstractUser):

    # 简历
    resume = models.TextField('resume', default='没有简历，请补充')

    def __str__(self):
        return self.resume

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teacher'
        ordering = ['username']


@python_2_unicode_compatible
class Feature(models.Model):
    FEATURE_CHOICES = (
        ('PY', 'Python'),
        ('Ja', 'Java'),
        ('Js', 'Javascript'),
        ('C', 'C')
    )
    feature = models.CharField(
        choices=FEATURE_CHOICES, max_length=200, default='Java')

    def __str__(self):
        return self.feature

    # 特长，关联Feature
    teacher = models.ForeignKey(Teacher)


class CategoryManager(models.Manager):

    # 获取所有有课程的类目。页面上不显示没有课程的类目
    def get_categories_have_course(self):
        categories = []
        categories_all = self.get_queryset().all()
        for category in categories_all:
            if category.course_id is not None:
                categories.append(category)


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField('course_category', max_length=256)
    rank = models.IntegerField('rank', default=0)
    course = models.ForeignKey('Course', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'
        ordering = ['rank']

    objects = CategoryManager()


@python_2_unicode_compatible
class Course(models.Model):

    introduction = MarkdownxField('introduction')

    course_name = models.CharField(max_length=256)

    # 授课老师
    teacher = models.ForeignKey(Teacher, blank=True, null=True)
    # 课程内容
    # content = models.TextField('content')
    content = MarkdownxField()
    # 发布日期
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    # 更新时间
    update_time = models.DateTimeField(auto_now=True, null=True)
    # 是否已经发布
    published = models.BooleanField('notDraft', default=True)

    # 是否置顶，即排在最前面，当课程的置顶值一样时，则按照发布日志排序
    up = models.BooleanField('UP', default=False)

    course_time = models.DateTimeField(auto_now=True, null=True)
    # 广告图片
# =========================================================================
#     ad_image = models.ImageField(
#         upload_to='abc', height_field='50', width_field='50', max_length=150, null=True)
#
#     def image_tag(self):
#         return u'<img src="%s" width="200px" />' % self.ad_image.url
#
#     image_tag.short_description = 'image'
#
#     image_tag.allow_tags = True
# =========================================================================

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Course'
        ordering = ['pub_date']

    objects = CourseManager()
