
from rest_framework.serializers import *
from ..models import User
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler  = api_settings.JWT_ENCODE_HANDLER




class LoginSerializer(Serializer):
    email=CharField(error_messages={'required':'email key is required','blank':'email is required'})
    password=CharField(error_messages={'required':'password key is required','blank':'password is required'})
    token=CharField(read_only=True,required=False)

    def validate(self,data):
        qs=User.objects.filter(email=data.get('email'))
        if not qs.exists():
            raise ValidationError("No account with this email")

        user=qs.first()
        if user.check_password(data.get('password'))==False:
            raise ValidationError("Invalid Password")
        payload =  jwt_payload_handler(user)
        token   =  jwt_encode_handler(payload)
        data['token'] ='JWT '+str(token)
        return data

class ForgotPasswordSerializer(Serializer):
    email=CharField(error_messages={'required':'email key is required','blank':'email is required'})
    username=CharField(error_messages={'required':'email key is required','blank':'email is required'})
    password=CharField(error_messages={'required':'password key is required','blank':'password is required'})
    def validate(self,data):
        qs=User.objects.filter(email=data.get('email'))
        if not qs.exists():
            raise ValidationError("No account with this email")
        qs=User.objects.filter(username=data.get('username'))
        if not qs.exists():
            raise ValidationError('No match username')
        return data
    def update(self,instance,validated_data):
        instance.set_password(validated_data.get('password'))
        instance.save()
        
        return validated_data
        


class StudentRegisterSerializer(Serializer):
    email=EmailField(error_messages={'required':'email key is required','blank':'email is required'})
    password=CharField(write_only=True,error_messages={'required':'password key is required','blank':'password is required'})
    username=CharField(error_messages={'required':'username key is required','blank':'username is required'})
    first_name=CharField(error_messages={'required':'username key is required','blank':'username is required'})
    last_name=CharField(error_messages={'required':'username key is required','blank':'username is required'})    
    def validate(self,data):
        username=data.get('username')
        qs=User.objects.filter(username=username)
        if qs.exists():
            raise ValidationError("Username already exists")

        qs=User.objects.filter(email=data.get('email'))
        if qs.exists():
            raise ValidationError("Email already exists")
        return data

    def create(self,validated_data):
            obj=User.objects.create(email=validated_data.get('email'),username=validated_data.get('username'),last_name=validated_data.get('last_name'),first_name=validated_data.get('last_name'),user_type=3,is_staff=False)
            obj.set_password(validated_data.get('password'))
            obj.save()
            return validated_data
    def update(self, instance, validated_data):
        instance.first_name=validated_data.get('first_name')
        instance.last_name=validated_data.get('last_name')
        instance.email=validated_data.get('email')
        instance.username=validated_data.get('username')
        instance.save()
        return validated_data
       
        

class AdminRegisterSerializer(Serializer):
    email=EmailField(error_messages={'required':'email key is required','blank':'email is required'})
    password=CharField(write_only=True,error_messages={'required':'password key is required','blank':'password is required'})
    username=CharField(error_messages={'required':'username key is required','blank':'username is required'})
    first_name=CharField(error_messages={'required':'username key is required','blank':'username is required'})
    last_name=CharField(error_messages={'required':'username key is required','blank':'username is required'})
    user_type=CharField(error_messages={'required':'username key is required','blank':'username is required'})
    
    def validate(self,data):
        username=data.get('username')
        qs=User.objects.filter(username=username)
        if qs.exists():
            raise ValidationError("Username already exists")

        qs=User.objects.filter(email=data.get('email'))
        if qs.exists():
            raise ValidationError("Email already exists")
        return data

    def create(self,validated_data):
            if validated_data.get('user_type') == 3 :
                obj=User.objects.create(email=validated_data.get('email'),username=validated_data.get('username'),last_name=validated_data.get('first_name'),first_name=validated_data.get('last_name'),is_staff=False,user_type=validated_data.get('user_type'))
                obj.set_password(validated_data.get('password'))
                obj.save()
                return validated_data
            else:
                obj=User.objects.create(email=validated_data.get('email'),username=validated_data.get('username'),last_name=validated_data.get('first_name'),first_name=validated_data.get('last_name'),is_staff=True,user_type=validated_data.get('user_type'))
                obj.set_password(validated_data.get('password'))
                obj.save()
                return validated_data