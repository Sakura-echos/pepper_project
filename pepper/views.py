from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from uuid import uuid4
from django.contrib.auth.tokens import default_token_generator
from .models import Sample
from .serializers import SampleSerializer


@api_view(['GET'])
def get_samples(request):
    samples = Sample.objects.all()
    serializer = SampleSerializer(samples, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_sample(request, sample_id):
    try:
        sample = Sample.objects.get(id=sample_id)
        serializer = SampleSerializer(sample)
        return Response(serializer.data)
    except Sample.DoesNotExist:
        return Response({'error': 'Sample not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def create_sample(request):
    serializer = SampleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_sample(request, sample_id):
    try:
        sample = Sample.objects.get(id=sample_id)
        serializer = SampleSerializer(sample, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Sample.DoesNotExist:
        return Response({'error': 'Sample not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_sample(request, sample_id):
    try:
        sample = Sample.objects.get(id=sample_id)
        sample.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Sample.DoesNotExist:
        return Response({'error': 'Sample not found.'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING),
        'password': openapi.Schema(type=openapi.TYPE_STRING),
        'permission': openapi.Schema(type=openapi.TYPE_INTEGER, enum=[0, 1])
    }
))
@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password1 = request.data.get('password1')
    password2 = request.data.get('password2')
    permission = request.data.get('permission', 1)

    if not username or not password1 or not password2:
        return Response({'error': 'Username and both password fields are required.'}, status=status.HTTP_400_BAD_REQUEST)
    if password1 != password2:
        return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=username, password=password1)
        user.permission = permission
        user.token = default_token_generator.make_token(user)
        user.save()
        # return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return redirect('home')
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING),
        'password': openapi.Schema(type=openapi.TYPE_STRING),
    }
))
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user is not None:
            login(request, user)
            request.session['username'] = username
            return redirect('home')
    else:
        return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def logout_user(request):
    logout(request)
    return redirect('home')

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING),
    }
))
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def delete_user(request):
    username = request.data.get('username')

    if not username:
        return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
        user.delete()
        return Response({'message': 'User deleted successfully.'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'password': openapi.Schema(type=openapi.TYPE_STRING),
    }
))
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def change_password(request):
    password = request.data.get('password')

    if not password:
        return Response({'error': 'New password is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = request.user
        user.set_password(password)
        user.save()
        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Create your views here.
def home(request):
    return render(request, 'pepper/home.html')


def data_plotter(request):
    return render(request, 'pepper/data_plotter.html')


def download_data(request):
    return render(request, 'pepper/download_data.html')


def upload_new_data(request):
    return render(request, 'pepper/upload_new_data.html')


def polydispersivity_tool(request):
    return render(request, 'pepper/polydispersivity_tool.html')


def literature_finder(request):
    return render(request, 'pepper/literature_finder.html')


def manage_data(request):
    return render(request, 'pepper/manage_data.html')

