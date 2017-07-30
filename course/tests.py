from django.test import TestCase

from course.models import Teacher, Course, Feature, Category


# Create your tests here.
class CouseTester(TestCase):

    def testCourseManager_query_by_category(self):
        user_info = {'password': 'wang',
                     'is_superuser': True,
                     'username': 'wang',
                     'first_name': 'wang',
                     'last_name': 'qiang',
                     'email': 'wang@lidu.com',
                     'is_staff': True,
                     'resume': 'wang resume'}
        teacher = Teacher(**user_info)
        teacher.save()
        print teacher
        feature = Feature(feature='C')
        feature.teacher = teacher
        print feature
        feature.save()
        course_info = {'introduction': 'java course intro',
                       'course_name': 'java program',
                       'content': 'java course content',
                       'published': True,
                       'up': True
                       }
        course = Course(**course_info)
        course.teacher = teacher
        course.save()
        print course
        category = Category(name='programming', rank='1')
        category.course = course
        category.save()
        print category
        query = Course.objects.query_summary_by_category(category.id)
        print query
        print query[0].get('pub_date').strftime("%Y-%m-%d %H:%M:%S")

       # self.assertEqual()
