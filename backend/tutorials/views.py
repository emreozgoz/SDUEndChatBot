import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .chatbot import ChatBot
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from tutorials.models import Tutorial
from tutorials.serializers import TutorialSerilizer

# Create your views here.
@csrf_exempt
def ChatApi(request, id=0):
    if request.method == 'GET':
        tutorial = Tutorial.objects.all()
        tutorial_serializer = TutorialSerilizer(tutorial, many=True)
        return JsonResponse(tutorial_serializer.data, safe=False)
    elif request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['question']
        chatbot = ChatBot()
        response = chatbot.run(content)
        #content yollanacak ai kısmına
        tutorial_data = JSONParser().parse(request)
        tutorial_data['answer'] = response
        tutorial_serializer = TutorialSerilizer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_data, safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == "PUT":
        tutorial_data = JSONParser().parse(request)
        tutorial = Tutorial.objects.get(id=tutorial_data['id'])
        tutorial_serializer = TutorialSerilizer(tutorial, data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse("Update Succesfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == "DELETE":
        tutorial = Tutorial.objects.get(id=id)
        tutorial.delete()
        return JsonResponse("Deleted Succesfully", safe=False)
