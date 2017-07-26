# -*— coding:utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from markdownx.models import MarkdownxField


class CourseManager(models.Manager):

    def query_by_category(self, category_id):
        query = self.get_queryset().filter(category_id=category_id)
        return query

    def query_by_teacher(self, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        course_list = teacher.course_set.all()
        return course_list

    def query_by_time(self):
        query = self.get_queryset().order_by('pub_date')
        return query

    def query_by_keyword(self, keyword):
        query = self.get_queryset().filter(title__contains=keyword)
        return query

# 教师


@python_2_unicode_compatible
class Teacher(AbstractUser):

    # 简历
    resume = models.TextField('resume', default='没有简历，请补充')

    def __str__(self):
        return self.username

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


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField('course_category', max_length=256)
    rank = models.IntegerField('rank', default=0)
    course = models.ForeignKey('Course')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'course_category'
        ordering = ['rank']


@python_2_unicode_compatible
class Course(models.Model):

    introduction = models.TextField('introduction')

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
    # 浏览次数
    read_count = models.IntegerField(default=0)
    # 广告图片
    ad_image = models.ImageField(
        upload_to='abc', height_field='50', width_field='50', max_length=150, null=True)

    def image_tag(self):
        return u'<img src="%s" width="200px" />' % self.ad_image.url

    image_tag.short_description = 'image'

    image_tag.allow_tags = True

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Course'
        ordering = ['pub_date']

    objects = CourseManager()
