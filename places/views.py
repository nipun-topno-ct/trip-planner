from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json
import random


GPT_URL = 'https://openai-hack-3.openai.azure.com/openai/deployments/openai-Hack-key3/chat/completions'
GPT_API_VERSION = '2023-07-01-preview'
GPT_API_KEY = 'f0b2edade75a4379902455ad926ad5c1'


# Create your views here.

class GetPlacesView(APIView):
    def get(self, request):
        headers = {
            'Content-Type': "application/json",
            'api-key': GPT_API_KEY
        }
        params = {
            'api-version': GPT_API_VERSION
        }
        data = '''{
    "messages": [
        {
            "role": "system",
            "content": %s
        }
    ],
    "max_tokens": 1500
}'''

        imgs = open('places/resources/place_images.json')
        imgs_data = json.load(imgs)
        imgs.close()

        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')

        poi_content = f'"What are the 7 best places to visit near the coordinates: {latitude}, {longitude}? Give the ouput in comma separated format with just the names."'
        poi_data = data % poi_content

        response = requests.post(url=GPT_URL, params=params, headers=headers, data=poi_data)
        poi = response.json()['choices'][0]['message']['content']
        print(poi)

        poi_list = poi.split(', ')
        fields = [
            '1. place: place name',
            '2. description: about the place',
            '3. opens: opening time (in this format HH:MM AM/PM)',
            '4. closes: closing time (in this format HH:MM AM/PM)',
            f'5. distance: distance this place from the coordinates: {latitude}, {longitude}',
            '6. time_spent: how much time to spend in this place',
            '7. expenditure: minimum ticket price in INR (this field should strictly be a single number)'
        ]
        details_content = '"give information about some places in stringified json format, that should be a list of object: [ { required fields }, { required fields }, ... ], where the required fields are: %s Do this for the following places: %s"'
        details_data = data % (details_content % (', '.join(fields), ', '.join(poi_list)))
        
        response = requests.post(url=GPT_URL, params=params, headers=headers, data=details_data)
        details = response.json()['choices'][0]['message']['content']
        details_store = json.loads(details)
        print(details_store)

        if not isinstance(details_store, list):
            print('Wrong output format from GPT')
            return Response(data='Wrong output format from GPT', status=500)

        for obj in details_store:
            if not isinstance(obj['distance'], str):
                obj['distance'] = f'{obj["distance"]} km'
            obj['img_url'] = 'https://media-cdn.tripadvisor.com/media/photo-s/01/5d/28/78/montego-bay.jpg'
            for entry in imgs_data:
                if obj['place'].lower() == entry['name'].lower() or obj['place'].lower().find(entry['name'].lower()) != -1 or entry['name'].lower().find(obj['place'].lower()) != -1:
                    obj['img_url'] = entry['img']
                    break

        return Response(details_store)


class GetHotspotsView(APIView):
    def get(self, request):
        hotspots = open('places/resources/hotspots.json')
        hotspots_data = json.load(hotspots)
        hotspots.close()

        ind = random.randint(0, len(hotspots_data) - 1)

        return Response(hotspots_data[ind])
