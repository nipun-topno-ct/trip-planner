from django.shortcuts import render

import json
import openai
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def plan_trip(request):
    # Extract parameters from the request (e.g., location, time remaining)
    location = request.GET.get('location')
    time_remaining = request.GET.get('time_remaining')
    places=request.GET.get('places')

    # GPT-3 prompt based on the user's input
    prompt = f"im at {location} ,I want to explore {places},now give me a detailed plan for a trip accordingly such that I have {time_remaining} remaining and give me an order in which I have to visit them, include from,to, fare to explore ,journey_time,journey_cost,time to explore, give me the order also fare to explore give me the output only  in stringifield json format"
    print(prompt)
    print("????????\n\n")

    openai.api_type = "azure"

    openai.api_base = "https://openai-hack-3.openai.azure.com/"

    openai.api_version = "2023-07-01-preview"

    openai.api_key = "f0b2edade75a4379902455ad926ad5c1"

    message_text = [{"role":"system","content":prompt}]
    
    completion = openai.ChatCompletion.create(

        engine="openai-Hack-key3",

        messages = message_text,

        temperature=0.7,

        max_tokens=800,

        top_p=0.95,

        frequency_penalty=0,

        presence_penalty=0,

        stop=None

    )
    content = completion['choices'][0]['message']['content']
    print(content)

    return  Response(json.loads(content))