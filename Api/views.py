from rest_framework import status
from rest_framework.response import Response
from Api.models import *
from .serializer import MessSerializer, MessageSerializer, userSerializer
from rest_framework.decorators import api_view , permission_classes
import datetime
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allmessages(request):
    mess = message.objects.all()
    serializer = MessageSerializer(mess,many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createmessages(request):
    use = request.user
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        cur_time = datetime.datetime.now(datetime.timezone.utc)
        messag = message.message_10(use.id)
        if messag:
            for i in messag:
                up_time = i.updated_at
                ch = cur_time - up_time
                a = ch.total_seconds()
                if a >= 3600 :
                    account = message(message=serializer.data['message'],created_by=use)
                    account.save()
                    ser = MessSerializer(account)
                    return Response(ser.data,status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors,status=status.HTTP_429_TOO_MANY_REQUESTS)
        else:
            account = message(message=serializer.data['message'],created_by=use)
            account.save()
            ser = MessSerializer(account)
            return Response(ser.data,status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
def registration(request):
    if request.method == 'POST':
        serialize = userSerializer(data=request.data)
        
        data = {}

        if serialize.is_valid():
            account = serialize.save()
            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email
            token = Token.objects.get(user=account).key
            data['token'] = token 
        else:
            data = serialize.errors
        return Response(data)


@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)