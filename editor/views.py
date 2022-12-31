from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import json
import os
# Create your views here.
def editorpage(request):
  # Opening JSON file
  f = open(os.path.dirname(os.path.realpath(__file__)) + '\static\words.json', "r")

  # returns JSON object as
  # a dictionary
  data = json.load(f)

  # Iterating through the json
  # list

  # Closing file
  words=[]
  for word in data['medical']:
    words.append(word)
  dataJSON = json.dumps(words)
  f.close()

  return HttpResponse(render(request=request,template_name="editor.html",context={"data":dataJSON}))