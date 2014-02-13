from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from loginCounter.models import User
from loginCounter.serializers import UserSerializer
 
 
@api_view(['POST'])
def user_add(request):
	"""
	Add User
	"""
	if request.content_type != 'application/json':
		return Response("Unrecognized request", status = status.HTTP_404_NOT_FOUND)
	user = User()
	errCode = user.add(request.DATA['user'], request.DATA['password'])
	data = { 'errCode': errCode }
	if (errCode == User.SUCCESS):
		newUser = User.objects.get(user=request.DATA['user'], password=request.DATA['password'])
		data['count'] = newUser.count
	return Response(data)



@api_view(['POST'])
def user_login(request):
	"""
	Login User
	"""
	if request.content_type != 'application/json':
		# fix this up at some point
		return Response("Unrecognized request", status = status.HTTP_404_NOT_FOUND)
	user = User()
	errCode = user.login(request.DATA['user'], request.DATA['password'])
	data = { 'errCode': errCode }
	if (errCode == User.SUCCESS):
		thisUser = User.objects.get(user=request.DATA['user'], password=request.DATA['password'])
		data['count'] = thisUser.count
	return Response(data)
	


@api_view(['POST'])
def testAPI_resetFixture(request):
	"""
	Reset Tables
	"""
	if request.content_type != 'application/json':
		return Response("Unrecognized request", status = status.HTTP_404_NOT_FOUND)
	if request.DATA == None:
		# should be empty
		return Response('handle this?')
	errCode = User().resetFixture()
	data = {'errCode': errCode}
	return Response(data)

@api_view(['POST'])
def testAPI_unitTests(request):
	"""
	Runs Unit Tests
	"""
	# import subprocess
	# from subprocess import Popen, PIPE
	# cmd = "python manage.py test > stdout.txt 2> stderr.txt"
	# process = subprocess.Popen(cmd, shell=True)
	

	# f = open('stdout.txt')
	# for line in f:
	# 	print line
	from unittest.case import TestCase
	import unittest
	from StringIO import StringIO
	from pprint import pprint
	from tests import UserTestCase
	stream = StringIO()
	runner = unittest.TextTestRunner(stream=stream)
	result = runner.run(unittest.makeSuite(UserTestCase))
	stream.seek(0)

	data = { 'nrFailed': len(result.failures), 'output':stream.read() , 'totalTests': result.testsRun}
	return Response(data)



