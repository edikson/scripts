#!/home/stack/rally/bin/python

import os
import sys

from rally import api
import sys
from bottle import route, post, run, template, request
from rally.task.processing import plot

#import pdb
#pdb.set_trace()
rapi = api.API()
#tasks = rapi.task.list()
#for task in tasks:
#  print(task)
##  print(task.get_status())
#  print(task.task['uuid'])
#  print(str(task.task))
#  print(dir(task))
#  print(str(task.get_results()))

@route('/display/<uuid>')
def index(uuid):
  html = \
"""<HTML>
<HEAD>\
<TITLE>page</TITLE>
</HEAD>
<BODY style='margin:0; padding:0'>
<center><a href='/'>Back</a>&nbsp;&nbsp;</center>
<iframe style='border: none; width: 100%; height: 100%;' src='/task/{{uuid}}'></iframe>
</BODY>
</HTML>
"""
  #task = rapi.task.get(uuid).get_results()
  return template(html, uuid=uuid)

@route('/task/<uuid>')
def index(uuid):
  results = []
  task_results = map(
                    lambda x: {"key": x["key"],
                               "sla": x["data"]["sla"],
                               "hooks": x["data"].get("hooks", []),
                               "result": x["data"]["raw"],
                               "load_duration": x["data"]["load_duration"],
                               "full_duration": x["data"]["full_duration"]},
                    rapi.task.get(uuid).get_results())
  results.extend(task_results)
  result = plot.plot(results, include_libs=("html_static"))
  return result


@route('/')
def index():
  links = []
  tasks = rapi.task.list()
  links.append("<a href='/trends'>Trends</a><br/>")
  for task in tasks:
    links.append(template('<a href="/display/{{uuid}}">report</a> {{uuid}} {{created}} d:{{debug}}<br/>',
                 uuid=task.task['uuid'], created=task.task['created_at'], debug=str('none')))
  return "\n".join(links)

@route('/trends')
def index():
  links = []
  tasks = rapi.task.list()
  for task in tasks:
    links.append(template('<option value="{{uuid}}">{{uuid}} {{created}} d:{{debug}}</option>',
                 uuid=task.task['uuid'], created=task.task['created_at'], debug=str('none')))
  options = "\n".join(links)
  html = \
"""<HTML>
<HEAD>\
<TITLE>Trends</TITLE>
</HEAD>
<BODY style='margin:0; padding:0'>
<form action='/trends2' method='post'>
<select name='uuids' size=10 multiple>
{{options}}
</select>
<br/>
<input type='submit' name='submit' value='submit' />
</form>
</BODY>
</HTML>
"""
  return html.replace("{{options}}", options)

@post('/trends2')
def index():
  uuids = request.forms.getall('uuids')
  results = []
  for uuid in uuids:
    task_results = map(
                    lambda x: {"key": x["key"],
                               "sla": x["data"]["sla"],
                               "hooks": x["data"].get("hooks", []),
                               "result": x["data"]["raw"],
                               "load_duration": x["data"]["load_duration"],
                               "full_duration": x["data"]["full_duration"]},
                    rapi.task.get(uuid).get_results())
    results.extend(task_results)
  result = plot.trends(results)
  return result

run(host='0.0.0.0', port=8080)
