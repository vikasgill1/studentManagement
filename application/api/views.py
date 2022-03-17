from functools import partial
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser,AllowAny,IsAuthenticated
from rest_framework.status import *
from rest_framework.response import Response
from .serializers import AdminRegisterSerializer, ForgotPasswordSerializer, LoginSerializer, StudentRegisterSerializer
from ..models import *
class Register(APIView):
        permission_classes = (IsAdminUser,)
        def post(self,request):
            if request.user.user_type == 2:
                serializer=StudentRegisterSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"account": 'accont create successfully','data':serializer.data},status=HTTP_201_CREATED)
                return Response({"error":serializer.errors},status=HTTP_400_BAD_REQUEST)
            else:
                serializer=AdminRegisterSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"account": 'account create successfully','data':serializer.data},status=HTTP_201_CREATED)
                return Response({"error":serializer.errors},status=HTTP_400_BAD_REQUEST)

class ForgetPassword(APIView):
    permission_classes = (IsAdminUser,)
    def put(self,request):
        if request.user.user_type == 1 :
            if User.objects.filter(id=request.data.get('id')).exists():
                stu=User.objects.get(id=request.data.get('id'))
                serializer=ForgotPasswordSerializer(instance=stu,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'forgetpassword ' : 'update your password'})
                return Response({'error':serializer.errors},status=HTTP_200_OK)
            return Response({'error':'Account Not found'},status=HTTP_404_NOT_FOUND)
        elif User.objects.filter(id=request.data.get('id'),is_superuser=True).exists():
            return Response("Not allow",status=HTTP_401_UNAUTHORIZED)
        else:
            if User.objects.filter(id=request.data.get('id'),is_superuser=False).exists():
                    stu=User.objects.get(id=request.data.get('id'))
                    serializer=ForgotPasswordSerializer(instance=stu,data=request.data,partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'data':serializer.data,'account':'forget password successfully'},status=HTTP_200_OK)
                    return Response({'error':serializer.errors},status=HTTP_400_BAD_REQUEST)
            return Response({'error':'Account Not found'},status=HTTP_404_NOT_FOUND)


class LoginApiView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message':'login successfully','data':serializer.data},status=HTTP_200_OK)
        return Response({'error':serializer.errors},status=HTTP_400_BAD_REQUEST)

# +++++++++++++++++++++++++++++++==========>>>>>   STUDENT PANEL         <<<<<======++++++++++++++++++++++++++++++


class ProfileView(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request):
        stu=User.objects.get(id=request.user.id)
        serializer=StudentRegisterSerializer(stu)
        return  Response(serializer.data)



# +++++++++++++++++++++++++++++++==========>>>>>   Admin PANAL       <<<<<======++++++++++++++++++++++++++++++

class ProfileDataView(APIView):
    permission_classes=( IsAdminUser,)
    def get(self, request):
        if request.user.user_type == 1 :
            if User.objects.filter(id=request.data.get('id')).exists():
                stu=User.objects.get(id=request.data.get('id'))
                serializer=StudentRegisterSerializer(stu)
                return Response(serializer.data)
            else:
                stu=User.objects.all()
                serializer=StudentRegisterSerializer(stu,many=True)
                return Response(serializer.data)
        else:
            if User.objects.filter(id=request.data.get('id'),is_superuser=False).exists():
                stu=User.objects.get(id=request.data.get('id'),is_superuser=False)
                serializer=StudentRegisterSerializer(stu)
                return Response(serializer.data)
            elif User.objects.filter(id=request.data.get('id'),is_superuser=True).exists():
                return Response("Not allow")
            else:
                stu=User.objects.get(is_superuser=False)
                serializer=StudentRegisterSerializer(stu,many=True)
                return Response(serializer.data)


    def put(self,request):
        if request.user.user_type == 1 :
            if User.objects.filter(id=request.data.get('id')).exists():
                stu=User.objects.get(id=request.data.get('id'))
                serializer=StudentRegisterSerializer(instance=stu,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response({'error':serializer.errors},status=HTTP_200_OK)
            return Response({'error':'Account Not found'},status=HTTP_404_NOT_FOUND)
        elif User.objects.filter(id=request.data.get('id'),is_superuser=True).exists():
            return Response("Not allow",status=HTTP_401_UNAUTHORIZED)
        else:
            if User.objects.filter(id=request.data.get('id'),is_superuser=False).exists():
                    stu=User.objects.get(id=request.data.get('id'))
                    serializer=StudentRegisterSerializer(instance=stu,data=request.data,partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'data':serializer.data,'account':'update successfully'},status=HTTP_200_OK)
                    return Response({'error':serializer.errors},status=HTTP_400_BAD_REQUEST)
            return Response({'error':'Account Not found'},status=HTTP_404_NOT_FOUND)  
    def delete(self,request):
        if request.user.user_type == 1 :
            if User.objects.filter(id=request.data.get('id')).exists():
                stu=User.objects.get(id=request.data.get('id'))
                stu.delete()
                return Response({'account':'delete succesfully'},status=HTTP_200_OK)
            return Response({'error':'Account Not found'},status=HTTP_404_NOT_FOUND)
        elif User.objects.filter(id=request.data.get('id'),is_superuser=True).exists():
            return Response("Not allow",status=HTTP_401_UNAUTHORIZED)
        else:
            if User.objects.filter(id=request.data.get('id'),is_superuser=False).exists():
                stu=User.objects.filter(id=request.data.get('id'))
                stu.delete()
                return Response({'account':'delete succesfully'},status=HTTP_200_OK)
            return Response({'error':'Account Not found'},status=HTTP_404_NOT_FOUND)
