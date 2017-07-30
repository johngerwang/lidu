# -*- coding:utf-8 -*-
from django.shortcuts import render

from course.models import Course, Category


# 首页，按照发布日期，显示课程内容
def index(request):
    categories = Category.objects.get_categories_have_course()

    # 获取课程的简介
    courses_summary = Course.objects.query_course_summary_by_category()
    context = {'categories': categories, 'courses_summary': courses_summary}
    return render(request, 'index.html', context)
