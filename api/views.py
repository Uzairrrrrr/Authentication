from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  status
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from rest_framework.views import APIView
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserSignInView(APIView):
    def post(self, request):
        # serializer = UserRegistrationSerializer(data=request.data)
        # if serializer.is_valid():
        # user = serializer.save()
        email = request.data.get('email')

        # Filter User model by email
        users = User.objects.get(email=email)

        refresh = RefreshToken.for_user(users)
        access_token = str(refresh.access_token)

        response_data = {
            'refresh': str(refresh),
            'access': access_token
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIOverview(APIView):
    def get(self, request, *args, **kwargs):
        api_urls = {
            'List': '/task-list/',
            'Detail View': '/task-detail/<str:pk>/',
            'Create': '/task-create/',
            'Update': '/task-update/<str:pk>/',
            'Delete': '/task-delete/<str:pk>/',
        }
        return Response(api_urls)

class TaskListCreateView(APIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer



class TaskListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    permission_classes = [IsAuthenticated]
    def post(self, request):
        # print(request.data)
        # user = User.objects.get(id=id)
        if 'title' not in request.data:
            return Response({"msg":"Record not created"})
        title = request.data['title']
        completed = request.data['completed']
        isinstance = request.user
        task = Task.objects.create(title=title,completed=completed,user=isinstance)
        if task:
            return Response({"msg":"Record created"})
       

        # serializer = TaskSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailUpdateDeleteView(APIView):
    def get_task(self, task_id):
        try:
            return Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return None

    def get(self, request, task_id):
        task = self.get_task(task_id)
        if task:
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, task_id):
        task = self.get_task(task_id)
        if task:
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, task_id):
        task = self.get_task(task_id)
        if task:
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            response_data = {'message': 'Task Delete'}  # Your custom message
            return Response(response_data, status=status.HTTP_200_OK)  # Sending 200 OK with custom message



