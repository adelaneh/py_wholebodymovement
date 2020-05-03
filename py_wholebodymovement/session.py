#!/usr/bin/env python
# coding: utf-8

class Session():
	"""Information about individual recording sessions.
	"""
	def __init__(self, name, data, activity=None, participant_id=None, date_time=None, comments=None):
		self._name 				= name
		self._data 				= data
		self._activity 			= activity
		self._participant_id 	= participant_id
		self._date_time 		= date_time
		self._comments 			= comments