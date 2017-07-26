#FAQ

##需要的django库
- 使admin支持markdownd，django-markdownx，当前版本2.0.21

> https://pypi.python.org/pypi/django-markdownx/2.0.21

mac下使用sudo pip2.7 install django-markdownx安装，安装好后的使用方法参考
> https://neutronx.github.io/django-markdownx/example.html

* 注意

1. 当拖拽到markdown标记框中的图片无法显示时，很可能的原因路径问题，一般可以通过下面的方式解决
 
 ```
 setting.py
 STATIC_URL = '/static/'
 STATIC_ROOT = os.path.join(BASE_DIR, 'static')
 MEDIA_URL = '/media/'
 MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')
```
```
urls.py
urlpatterns = [
    # Examples:
    # url(r'^$', 'cms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^markdownx/', include('markdownx.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #增加这一行，使django能够找到图片路径
```
2.  文档中下面一段不知道是干嘛的,在admin的界面中，下面一段不加也未出现啥问题
```
	<form method="POST" action="">{% csrf_token %}
	    {{ form }}
	</form>
	
	{{ form.media }}
```



