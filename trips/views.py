from django.shortcuts import render

import json
import openai
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def plan_trip(request):
    request_body = json.loads(request.body)

    latitude = request_body['latitude']
    longitude = request_body['longitude']
    places = request_body['places']

    openai.api_type = "azure"
    openai.api_base = "https://openai-hack-3.openai.azure.com/"
    openai.api_version = "2023-07-01-preview"
    openai.api_key = "f0b2edade75a4379902455ad926ad5c1"

    location_prompt = f'give a random locality inside the city which is at the coordinates: {latitude}, {longitude}. Response should only contain the locality name'
    print(location_prompt)

    message_text = [
        {
            "role": "system",
            "content": location_prompt
        }
    ]
    location_response = openai.ChatCompletion.create(
        engine = "openai-Hack-key3",
        messages = message_text,
        temperature = 0.7,
        max_tokens = 800,
        top_p = 0.95,
        frequency_penalty = 0,
        presence_penalty = 0,
        stop = None
    )
    location = location_response['choices'][0]['message']['content']
    print(location)

    # GPT-3 prompt based on the user's input
    fields = [
        '1. from: initial place',
        '2. to: destination place',
        '3. fare_to_explore: average money spent to explore the destination place',
        '4. time_to_explore: how much time to be spent to explore the destination place (with time unit)',
        '5. journey_time: time taken to travel from initial place to destination place (with time unit)',
        '6. journey_cost: money spent to travel from initial place to destination place',
    ]
    trip_prompt = f"I am currently at {location}. I want to explore all of the following places: {places}, now give me a detailed plan for a trip accordingly and give me an order in which I have to visit them which is time efficient, give me the output only in stringified json format:" + " [ { required fields }, { required_fields}, ... ] where the required fields are: %s" % ', '.join(fields)
    print(trip_prompt)

    message_text = [
        {
            "role": "system",
            "content": trip_prompt
        }
    ]
    trip_plan = openai.ChatCompletion.create(
        engine = "openai-Hack-key3",
        messages = message_text,
        temperature = 0.7,
        max_tokens = 800,
        top_p = 0.95,
        frequency_penalty = 0,
        presence_penalty = 0,
        stop = None
    )
    trip_response = trip_plan['choices'][0]['message']['content']
    print(trip_response)

    return Response(json.loads(trip_response))