from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from tutorials.models import Tutorial
from tutorials.serializers import TutorialSerilizer


# Create your views here.
@csrf_exempt
def ChatApi(request,id=0):
    if request.method == 'GET':
        tutorial = Tutorial.objects.all()
        tutorial_serializer = TutorialSerilizer(tutorial,many=True)
        return JsonResponse(tutorial_serializer.data,safe=False)
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TutorialSerilizer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse("AddedSuccesfully",safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == "PUT":
        tutorial_data = JSONParser().parse(request)
        tutorial = Tutorial.objects.get(id=tutorial_data['id'])
        tutorial_serializer = TutorialSerilizer(tutorial,data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse("Update Succesfully",safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == "DELETE":
        tutorial = Tutorial.objects.get(id=id)
        tutorial.delete()
        return JsonResponse("Deleted Succesfully", safe=False)

        
