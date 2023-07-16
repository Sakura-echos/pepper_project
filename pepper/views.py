from io import TextIOWrapper

from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from uuid import uuid4
from django.contrib.auth.tokens import default_token_generator

from .forms import LiteratureForm
from .models import Sample, literature
from .serializers import SampleSerializer
from django.core.paginator import Paginator
import csv
from django.core.exceptions import ValidationError

from django.db.models import Q

@api_view(['GET'])
def get_samples(request):
    page_number = request.GET.get('page', 1)
    limit = request.GET.get('limit', 3)
    publication_search_keyword = request.GET.get('publication_search', '')
    volcano_search_keyword = request.GET.get('volcano_search', '')

    samples = Sample.objects.all()

    if publication_search_keyword:
        samples = samples.filter(publication__icontains=publication_search_keyword)

    if volcano_search_keyword:
        samples = samples.filter(volcano__icontains=volcano_search_keyword)

    paginator = Paginator(samples, limit)
    page_obj = paginator.get_page(page_number)

    return render(request, 'pepper/manage_data.html', {
        'page_obj': page_obj,
        'publication_search_keyword': publication_search_keyword,
        'volcano_search_keyword': volcano_search_keyword
    })

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
        subject = 'PePPEr信息'
        message = '用户新增了一个数据'
        recipient_list = ['1127911471@qq.com']
        send_mail(subject, message, '1127911471@qq.com', recipient_list)
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
def scientific_to_decimal(value):
    if 'E-' in value:
        float_value = float(value)
        decimal_value = format(float_value, '.{}f'.format(abs(int(value.split('E-')[1]))))
        return decimal_value
    else:
        return value
def import_samples_from_csv(file):
    # Open the CSV file
    csv_file = TextIOWrapper(file, encoding='utf-8')
    reader = csv.DictReader(csv_file)
    for row in reader:
            # Create a new Sample object
            sample = Sample()

            # Set the field values from the CSV row
            sample.publication = row['publication']
            sample.volcano = row['volcano']
            sample.eruption = row['eruption']
            sample.data_doi = row['data_doi']
            sample.chemistry = row['chemistry']
            sample.bulk_sio2 = row['bulk_sio2']
            sample.bulk_na2o_k2o = row['bulk_na2o_k2o']
            sample.glass_sio2 = row['glass_sio2']
            sample.glass_na2o_k2o = row['glass_na2o_k2o']
            sample.chemistry_doi = row['chemistry_doi']
            sample.rock_experiment_type = row['rock_experiment_type']
            sample.subaerial_submarine = row['subaerial_submarine']
            sample.eff_exp = row['eff_exp']
            sample.sample_no = row['sample_no']
            sample.bulk_porosity = row['bulk_porosity']
            sample.connected_porosity = row['connected_porosity']
            sample.connectivity = row['connectivity']
            sample.permeability_k1 = scientific_to_decimal(row['permeability_k1'])
            sample.permeability_k2 = scientific_to_decimal(row['permeability_k2'])
            sample.vesicle_number_density = scientific_to_decimal(row['vesicle_number_density'])
            sample.s_polydispersivity = scientific_to_decimal(row['s_polydispersivity'])
            sample.total_crystallinity = scientific_to_decimal(row['total_crystallinity'])
            sample.phenocrystallinity = scientific_to_decimal(row['phenocrystallinity'])
            sample.microcrystallinity = scientific_to_decimal(row['microcrystallinity'])


            try:
                # Validate and save the Sample object
                sample.full_clean()
                sample.save()
            except ValidationError as e:
                # Handle validation errors
                print(f"Validation Error for row: {row}\n{e}")

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')

        if file:
            # 调用你之前编写的导入函数
            import_samples_from_csv(file)

            return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})



# 列出所有 literature 对象
def literature_list(request):
    literature_objects = literature.objects.all()
    return render(request, 'literature/list.html', {'literature_objects': literature_objects})

# 创建 literature 对象
def literature_create(request):
    if request.method == 'POST':
        form = LiteratureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('literature_list')
    else:
        form = LiteratureForm()
    return render(request, 'literature/create.html', {'form': form})

# 更新 literature 对象
def literature_update(request, pk):
    literature_object = literature.objects.get(pk=pk)
    if request.method == 'POST':
        form = LiteratureForm(request.POST, instance=literature_object)
        if form.is_valid():
            form.save()
            return redirect('literature_list')
    else:
        form = LiteratureForm(instance=literature_object)
    return render(request, 'literature/update.html', {'form': form})

# 删除 literature 对象
def literature_delete(request, pk):
    literature_object = literature.objects.get(pk=pk)
    literature_object.delete()
    return redirect('literature_list')