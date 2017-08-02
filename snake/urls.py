from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^crawl/',views.crawl),
    url(r'^test/',views.return_zip_file)

]
