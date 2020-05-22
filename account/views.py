# models
from account.models import *


# rest_framework
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
# serializers
from .serializers import *

# main purpose
import cv2
from .Inference import *



class RegistrationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'Successfully registered a new user.'
            data['email'] = account.email
            data['username'] = account.username
        else:
            data = serializer.errors
        return Response(data)


class LanguageView(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class GeneralSettingView(viewsets.ModelViewSet):
    queryset = GeneralSetting.objects.all()
    serializer_class = GeneralSettingSerializer
    def get_queryset(self):
        return GeneralSetting.objects.filter(user=self.request.user)
    

class EmailSettingView(viewsets.ModelViewSet):
    queryset = EmailSetting.objects.all()
    serializer_class = EmailSettingSerializer
    def get_queryset(self):
        return EmailSetting.objects.filter(user=self.request.user)


class ScenarioView(viewsets.ReadOnlyModelViewSet):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer


class CameraView(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    def get_queryset(self):
        return Camera.objects.filter(user=self.request.user)


class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)


class ModelView(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    def get_queryset(self):
        return Model.objects.filter(user=self.request.user) | Model.objects.filter(is_public=True)


class ServerConfigView(viewsets.ModelViewSet):
    queryset = ServerConfig.objects.all()
    serializer_class = ServerConfigSerializer


class InferenceAPI(APIView):
    
    serializer_class = InferenceAPISerializer

    def post(self, request):
        serializer = InferenceAPISerializer(data=request.data)
        if serializer.is_valid():
            operation = serializer.data.get("operation")
            if operation == "INFERENCE":
                model = Model.objects.all().first()
                input_shape = model.input_shape()
                model_name = model.as_json()["model_name"]
                pre_order = "bhwd"
                inference_server = ServerConfig.objects.filter(server_name=operation).first()
                url = inference_server.full_url()
                # load image
                img = cv2.imread(os.path.join("account/img.jpg"))
                densitymap, count = ort_client(img, model_name, "float32", pre_order, input_shape, url)
                cv2.imshow("hm", densitymap)
                cv2.waitKey(0)
                return Response({"count": count})#, "densitymap": densitymap.tolist()})

        #when errors occur
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConversionAPI(APIView):
    pass