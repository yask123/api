from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from task.models import Task
from django.utils import timezone
from django.shortcuts import redirect
import json
from urllib import quote_plus as qp
from facepy import GraphAPI
from geopy.geocoders import Nominatim
import requests
# Create your views here.

def index(request):
	if request.method == 'GET':
		name = request.GET.get('name', '')
		location = request.GET.get('location')
		acc_token = request.GET.get('token')
		if location:
			geolocator = Nominatim()
			location = geolocator.geocode(location)
			location = str(location.latitude)+','+str(location.longitude)
		else:
			lat = request.GET.get('lat')
			lon = request.GET.get('lon')
			location = str(lat)+','+str(lon)

		print name,location,acc_token

		if acc_token:
			graph = GraphAPI(acc_token)
		else:
			graph = GraphAPI('CAACEdEose0cBAPJRZA8xHkMmbokHYBCUyjcKxZBohVhzJnGlm2ETlOYESQpEjG1Gj6ykTV4FMmhqMUrgFsJp0HdH4TszHwCkoMA8PS8L2MRFth3w3Wm7ucx4xMglc9ZBZAMhnyrr3XNAlH6MHZBtGmeWusWvzu4GSt4Mt9oS2KIOkWh70WhQ3ktOUC40PgChklQN31X0EgAZDZD')
	
		search=name
		search = qp(search)
		
		result = graph.get('search?type=place&q='+search+'&center='+location)
		page_id = result['data'][0]['id']

		params = 'fields=phone,likes,current_location,about,website,food_styles,description,hours,awards,price_range,location,booking_agent,is_verified,offers,public_transit,founded,products,emails,parking'
		a =  str(page_id)+'?'+params
		cache={}
		cache['facebook'] = {}
		cache['google'] = {}

 		cache['facebook'] = {'fb_page_url':'http://facebook.com/'+page_id}
 		params = params.split(',')
 		for each in params:
 			try:
 				cache['facebook'][each] = str(graph.get(a)[each])
 			except:
 				pass		

 		#Google Data
		url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+location+'&radius=5000&name='+name+'&key=AIzaSyDAERlVmOrLWdq0pHF5fK3c2cHmCSvy55I'
		print url
		r = requests.get(url)
		google_result = json.loads(r.text)		
		cache['google']=google_result

		return HttpResponse(json.dumps(cache), content_type="application/json")

	elif request.method == 'POST':
		t =  request.POST.get("task", "")
		a = Task(text=t,date=timezone.now())
		a.save()
		return redirect('/')
