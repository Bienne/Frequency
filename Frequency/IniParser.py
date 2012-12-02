#!/usr/local/bin/python3
# -*- coding: utf-8 -*- 


import re

class IniParser:
	def __init__(self, file):
		self.file = file
		self.IniDict = {}
		self.__FillIniDict(file)

		
	def GetValue(self, key):
		try:
			return self.IniDict[key]		
		except KeyError:
			raise Exception('"%s" does not exists' % key)
	
	
	def __FillIniDict(self, file):
		keyValRegEx = re.compile( r"^\s*(.+?)\s*=\s*(.+?)\s*$" )
		for line in self.__ReadFileAsListLine(file):
			result = keyValRegEx.search(line)
			if result:
				self.IniDict[result.group(1)] = result.group(2)				
		
		
	def __ReadFileAsListLine(self, file):	
		try:
			with open(file, 'r') as file: 
				return file.readlines()
				
		except Exception as e:
			print(e) 