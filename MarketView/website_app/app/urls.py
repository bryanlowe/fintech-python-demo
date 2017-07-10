from django.conf.urls import url
from app import views

urlpatterns = [
    # brand share view
    url(r'^brandshare', views.brand_share, name='marketview'),

    # sales growth view
    url(r'^salesgrowth', views.sales_growth, name='marketview'),

    # industry view
    url(r'^industry', views.industry, name='marketview'),

    # product trends view
    url(r'^producttrends', views.product_trends, name='marketview'),

    # pricing view
    url(r'^pricing', views.pricing, name='marketview'),

    # The home page
    url(r'^$', views.index, name='index'),
]