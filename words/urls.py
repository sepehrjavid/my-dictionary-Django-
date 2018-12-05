from django.urls import path, include, re_path
from .views import (
    WordsView,
    DteailView,
    CreateWordView,
    EditView,
    AddMeaningView,
    SelectMeaningAddExampleView,
    AddExamleView,
    EditMeaningView,
    SelectMeaningEditView,
    DeleteWordView,
    SelectMeaningDeleteView,
    DeleteMeaningView,
)

app_name = 'words'

urlpatterns = [
    path('', WordsView.as_view(), name = 'words_list'),
    path('createw/', CreateWordView.as_view(), name='create_view'),
    re_path(r'^meanings/(?P<pk>\d+)/$',AddExamleView.as_view(), name='addexample'),
    re_path(r'^meanings/(?P<pk>\d+)/edit$',EditMeaningView.as_view(), name='editmeaning'),
    re_path(r'^meanings/(?P<pk>\d+)/delete$',DeleteMeaningView.as_view(), name='delmeaning'),
    re_path(r'^(?P<slug>[\w-]+)/edit$', EditView.as_view(), name='edit'),
    re_path(r'^(?P<slug>[\w-]+)/addmeaning$',AddMeaningView.as_view(), name='addmeaning'),
    re_path(r'^(?P<slug>[\w-]+)/selectm$',SelectMeaningAddExampleView.as_view(), name='selectmeaning'),
    re_path(r'^(?P<slug>[\w-]+)/selectmedit$',SelectMeaningEditView.as_view(), name='selectmeaningedit'),
    re_path(r'^(?P<slug>[\w-]+)/selectmdel$',SelectMeaningDeleteView.as_view(), name='selectmeaningdel'),
    re_path(r'^(?P<slug>[\w-]+)/deletew$', DeleteWordView.as_view(), name='deleteword'),
    re_path(r'^(?P<slug>[\w-]+)/$', DteailView.as_view(), name = 'detailword'),
]
