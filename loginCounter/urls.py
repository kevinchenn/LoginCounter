from django.conf.urls import patterns, url

urlpatterns = patterns('loginCounter.views',
	url(r'^$', 'index'),
    url(r'^users/add', 'user_add'),
    url(r'^users/login', 'user_login'),
    url(r'^users/view_add', 'view_add'),
    url(r'^users/view_login', 'view_login'),
    url(r'^TESTAPI/resetFixture', 'testAPI_resetFixture'),
    url(r'^TESTAPI/unitTests', 'testAPI_unitTests'),
)
