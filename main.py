#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import jinja2
import webapp2
from apiclient.discovery import build
import json
from oauth2client.appengine import OAuth2Decorator
from apiclient.http import MediaFileUpload

decorator = OAuth2Decorator(
	client_id = '847049896714.apps.googleusercontent.com',
	client_secret = 'rYYyYuYAuopEfddJT_ftWiCH',
	scope='https://www.googleapis.com/auth/calendar'
	)

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

service = build('calendar','v3')

# class MainPage(webapp2.RequestHandler):
# 	@decorator.oauth_required
#         def get(self):
#         	http = decorator.http()

# 	        events = service.events().list(calendarId='primary').execute(http=http)
# 	        for event in events['items']:
# 	            if 'dateTime' in event['start']:
# 					dateTime = event['start']['dateTime']
# 					year = dateTime[:4]
# 					month = dateTime[5:-18]
# 					date = dateTime[8:-15]	            	
					# self.response.write("dateTime")	            	
					# self.response.write(event['start']['dateTime'])
					# self.response.write("</br>")
					# self.response.write("Year ::"+year+"</br>")
					# self.response.write("Month ::"+month+"</br>")	  	
					# self.response.write("Date ::"+date+"</br>")	  		            		            		  	            		            	            	
# 	            else:
# 					dateTime2 = event['start']['date']
# 					year2 = dateTime2[:4]
# 					month2 = dateTime2[5:-3]
# 					date2 = dateTime2[8:]	            	
# 					self.response.write("date")	            	
# 					self.response.write(event['start']['date'])
# 					self.response.write("</br>")
# 					self.response.write("Year ::"+year2+"</br>")
# 					self.response.write("Month ::"+month2+"</br>")	  	
# 					self.response.write("Date ::"+date2+"</br>")	  

# 			                # x = event['start']
# 			                # y = x['dateTime']
# 			                # self.response.write("Start Date :: " + y +"</br>")
# 			                # self.response.write(event['summary'] + "</br>")
# 			                # self.response.write(event['start']['dateTime']+"</br></br></br>")
# 			        # self.response.write("Year ::  "+year+ "</br>")	  
# 			        # self.response.write("Month ::  "+month+"</br>")	 
# 			        # self.response.write("Date ::  "+date+"</br></br></br>")	    
# 			        # self.response.write(dateTime)
# 			        # self.response.write("</br></br>")	  		            	               
# 	            # if 'location' in event:
# 	            #     self.response.write("Location :: " + event['location'] + "</br>")
# 	            # if 'description' in event:
# 	            #     self.response.write("Description :: " + event['description'] + "</br>")
	        
# 			# self.response.write("</br></br></br></br>")
# 			# self.response.write(event['start'])
# 			# self.response.write(events)

class CalendarView(webapp2.RequestHandler):
	@decorator.oauth_required
	def get(self):

		http = decorator.http()
		events = service.events().list(calendarId='primary').execute(http=http)
		year = []
		month = []
		date = []
	        for event in events['items']:
	            if 'dateTime' in event['start']:
					dateTime = event['start']['dateTime']
					year.append(dateTime[:4])
					month.append(dateTime[5:-18])
					date.append(dateTime[8:-15])
					# self.response.write("dateTime")	            	
					# self.response.write(event['start']['dateTime'])
					# self.response.write("</br>")
					# self.response.write("Year ::"+year+"</br>")
					# self.response.write("Month ::"+month+"</br>")	  	
					# self.response.write("Date ::"+date+"</br>")	  						         		            		            		  	            		            	            	
	            else:
					dateTime = event['start']['date']
					year.append(dateTime[:4])
					month.append(dateTime[5:-3])
					date.append(dateTime[8:]) 	   
					# self.response.write("dateTime")	            	
					# self.response.write(event['start']['date'])
					# self.response.write("</br>")
					# self.response.write("Year ::"+year+"</br>")
					# self.response.write("Month ::"+month+"</br>")	
		# for x in year:
		# 	self.response.write("Year :: ")			
		# 	self.response.write(x)
		# 	self.response.write("</br>")
		# for y in month:
		# 	self.response.write("Month :: ")
		# 	self.response.write(y)
		# 	self.response.write("</br>")
		for z in date:
			self.response.write("Date :: ")
			self.response.write(z)
			self.response.write("</br>")


		templates = {
				'events' : events['items'],
				'year' : year,
				'month' : month,
				'date' : date,	
			}

		template = JINJA_ENVIRONMENT.get_template('course_regis.html')
		self.response.write(template.render(templates))
		


app = webapp2.WSGIApplication([
    ('/', CalendarView),
    (decorator.callback_path,decorator.callback_handler())
], debug=True)
