from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('languages', views.LanguageView)
router.register('generalsettings', views.GeneralSettingView)
router.register('emailsettings', views.EmailSettingView)
router.register('scenario', views.ScenarioView)
router.register('camera', views.CameraView)
router.register('event', views.EventView)
router.register('model', views.ModelView)
router.register('serverconfig', views.ServerConfigView)


urlpatterns = [
    path('api/', include(router.urls)),
    path('signup/', views.RegistrationView.as_view(), name="signup"),
    #path('inference/', views.InferenceAPI.as_view()),
]
