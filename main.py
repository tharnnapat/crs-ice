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
from google.appengine.api import rdbms
import datetime

decorator = OAuth2Decorator(
	client_id = '847049896714.apps.googleusercontent.com',
	client_secret = 'rYYyYuYAuopEfddJT_ftWiCH',
	scope='https://www.googleapis.com/auth/calendar'
	)

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

service = build('calendar','v3')

_INSTANCE_NAME="prinya-th-2013:prinya-db"

class CalendarView(webapp2.RequestHandler):
	@decorator.oauth_required
	def get(self):



		http = decorator.http()
		events = service.events().list(calendarId='primary').execute(http=http)
		year = []
		month = []
		date = []
		start_time_hour = []
		start_time_minute = []
		end_time_hour = []
		end_time_minute = []
		allday_time = []
		recurrence = []
		recurrence2 = []
		title = []

		for event in events['items']:
			dateTime = event['start']['dateTime']
			dateTime2 = event['end']['dateTime']
			title.append(event['summary'])
			if 'timeZone' in event['start']:
				if 'recurrence' in event:
					rec = event['recurrence']
					recurrence.append(rec)
					year.append(dateTime[:4])
					month.append(dateTime[5:-18])
					date.append(dateTime[8:-15]) 	   
					start_time_hour.append(00)
					start_time_minute.append(00)
					end_time_hour.append(00)
					end_time_minute.append(00)
					allday_time.append(1)
					self.response.write("IF 2")
					self.response.write("</br>")		

				else:
					recurrence.append(0)
					year.append(dateTime[:4])
					month.append(dateTime[5:-18])
					date.append(dateTime[8:-15]) 	   
					start_time_hour.append(00)
					start_time_minute.append(00)
					end_time_hour.append(00)
					end_time_minute.append(00)
					allday_time.append(1)		
					self.response.write("ELSE 2")				
					self.response.write("</br>")		
			else:
				if 'recurrence' in event:
					rec = event['recurrence']
					recurrence.append(rec)
					year.append(dateTime[:4])
					month.append(dateTime[5:-18])
					date.append(dateTime[8:-15])
					start_time_hour.append(dateTime[11:-12])
					start_time_minute.append(dateTime[14:-9])
					end_time_hour.append(dateTime2[11:-12])
					end_time_minute.append(dateTime2[14:-9])
					allday_time.append(0)
					self.response.write("IF 1")
					self.response.write("</br>")											         
				else:
					recurrence.append(0)
					year.append(dateTime[:4])
					month.append(dateTime[5:-18])
					date.append(dateTime[8:-15])
					start_time_hour.append(dateTime[11:-12])
					start_time_minute.append(dateTime[14:-9])
					end_time_hour.append(dateTime2[11:-12])
					end_time_minute.append(dateTime2[14:-9])
					allday_time.append(0)
					self.response.write("ELSE 1")					         		            		            		  	            		            	            	
					self.response.write("</br>")	


		len_event = len(year)

		for row in range(0,len(recurrence)):
			if recurrence[row] != 0:
				rec = str(recurrence[row])
				x = list(str(recurrence[row]))
				if x[28] == "'" :
					recurrence2.append(int(rec[27:-2]))
				else:			
					recurrence2.append(int(rec[27:-2]))
			else:
				recurrence2.append(int(1))

		self.response.write("RECCURRENCE 2")
		self.response.write("</br>")

		for row in range(0,len(recurrence)):
			self.response.write(recurrence2[row])
			self.response.write("</br>")

		self.response.write("ALL DAY TIME")
		for row in range(0,len(allday_time)):
			self.response.write(allday_time[row])
			self.response.write("</br>")


		self.response.write("<a href='/InsertCelendar'> Insert </a>")

		self.response.write(len_event)


		templates = {
				'events' : events['items'],
				'title' : title,	
				'year' : year,
				'month' : month,
				'date' : date,	
				'start_time_hour' : start_time_hour,	
				'start_time_minute' : start_time_minute,	
				'end_time_hour' : end_time_hour,	
				'end_time_minute' : end_time_minute,	
				'allday_time' : allday_time,	
				'recurrence2' : recurrence2,	
				'len_event' : len_event,

			}

		template = JINJA_ENVIRONMENT.get_template('course_regis.html')
		self.response.write(template.render(templates))
		
class InsertCelendar(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self):

		open_semester_year = '2013-06-27' #Insert Date on Monday
		weekly_study = 13

    	# course_code = self.request.get('');
    	# section = self.request.get('');

		course_code = 'INT-101'
		section = 1

		today = datetime.datetime.now()
		weekday = today.weekday()+2
		if weekday == 6 :
			weekday = 1 
		month_num=int(open_semester_year[5:-3])
		day_num =int(open_semester_year[8:])



		conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
		cursor = conn.cursor()
		sql ="select day,start_time,end_time,room from\
				section sec JOIN section_time sct\
				ON sec.section_id=sct.section_id\
				JOIN course cou\
				ON cou.course_id=sec.regiscourse_id\
				WHERE course_code='%s' AND section_number='%d'"%(course_code,section)

		cursor.execute(sql)
		conn.commit()
		result = cursor.fetchall()

		day = []
		full_start_time =[]
		full_end_time = []
		room = []
		section = []

		insert_day = []
		insert_day2 = []
		month_num2=[]



		for x in range(0,len(result)):
			day.append(result[x][0])
			full_start_time.append(result[x][1])		
			full_end_time.append(result[x][2])
			room.append(result[x][3])


		for x in range(0,len(result)):
			for d in range(1,8):
				self.response.write(d)
				self.response.write("</br>")	
				if d==result[x][0]:
					if month_num==1 or month_num==3 or month_num==5 or month_num==7 or month_num==8 or month_num==10 or month_num==12 :
						if day_num+d <= 31 :					
							insert_day.append(day_num+d-2)
							month_num2.append(month_num)
						else:
							insert_day.append(day_num+d-33)
							month_num2.append(month_num+1)												
										
					elif month_num==4 or month_num==6 or month_num==9 or month_num==11:
						if day_num+d <= 30 :					
							insert_day.append(day_num+d-2)
							month_num2.append(month_num)
						else:
							insert_day.append(day_num+d-32)
							month_num2.append(month_num+1)
							self.response.write(day_num)
												
					elif month_num==2:
						if day_num+d <= 28 :					
							insert_day.append(day_num+d-2)
							month_num2.append(month_num)
						else:
							insert_day.append(day_num+d-30)
							month_num2.append(month_num+1)													
		
		for x in range(0,len(insert_day)):
			insert_day2.append('2013-'+str(month_num2[x])+'-'+str(insert_day[x]))	

		# for x in range(0,len(insert_day)):
		# 	self.response.write("Insert Day 1 :: ")
		# 	self.response.write(insert_day[x])	
		# 	self.response.write("</br>")
		# 	self.response.write("Insert Day 2 :: ")
		# 	self.response.write(insert_day2[x])	
		# 	self.response.write("</br>")

		# for x in range(0,len(month_num2)):
		# 	self.response.write("Month NUM :: ")
		# 	self.response.write(month_num2[x])	
		# 	self.response.write("</br>")
		


		http = decorator.http()
		for num in range(0,len(day)):
			event = {
	            'summary' : "%s"%(room[num]),
	            'Location' : 'Thai-Nichi Institute of Technology',
	            'start' : {
	                'dateTime' : "%sT%s.000+07:00"%(insert_day2[num],full_start_time[num]),
	                'timeZone' : 'Asia/Bangkok'
	            },
	            'end':{
	                'dateTime' : "%sT%s.000+07:00"%(insert_day2[num],full_end_time[num]),
	                'timeZone' : 'Asia/Bangkok'
	            },
	            'recurrence': [
	            "RRULE:FREQ=WEEKLY;COUNT=%d"%(weekly_study),
	            ],       
			}

			insert_event = service.events().insert(calendarId='primary',body=event).execute(http=http)

		self.redirect('/')

		self.response.write("Create event success  ")

		self.response.write("<a href='/DeleteCalendar'> Delete </a>")
		self.response.write("<a href='/'> Home </a>")
class DeleteCalendar(webapp2.RequestHandler):
	@decorator.oauth_required
	def get(self):

		name_get = 'B201'


		http = decorator.http()
		events = service.events().list(calendarId='primary').execute(http=http)
		ID_events = []
		name_events = []

		for event in events['items']:
			if 'summary' in event:
				id_event = event['id']
				name_event = event['summary']
				ID_events.append(id_event)
				name_events.append(name_event)

		# for x in range(0,len(ID_events)):
		# 	self.response.write(ID_events[x])	
		# 	self.response.write("</br>")
		# 	self.response.write(name_events[x])	
		# 	self.response.write("</br>")

		for y in range(0,len(ID_events)):	
			if name_get == name_events[y]:
				http = decorator.http()
				service.events().delete(calendarId='primary', eventId=ID_events[y]).execute(http=http)

		self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', CalendarView),
    ('/InsertCelendar', InsertCelendar),
    ('/DeleteCalendar', DeleteCalendar),
    (decorator.callback_path,decorator.callback_handler())
], debug=True)
