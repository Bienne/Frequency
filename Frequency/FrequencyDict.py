#!/usr/local/bin/python3
# -*- coding: utf-8 -*- 


import re
import os
from collections import Counter

from WordNet.Lemmatizer import Lemmatizer

# Простое слово, например "over", можно найти, используя выражение "([a-zA-Z]+)" - здесь ищется одна или более букв английского алфавита.
# Составное слово, к примеру "commander-in-chief", найти несколько сложнее, нам нужно искать идущие друг за другом 
# подвыражения вида "commander-", "in-", после которых идет слово "chief".
# Регулярное выражение примет вид "(([a-zA-Z]+-?)*[a-zA-Z]+)".
# Если в выражении присутсвует промежуточное подвыражение, оно тоже включается в результат. Так, в наш результат попадает не только слово 
# "commander-in-chief", но также и все найденные подвыражения, Чтобы их исключить, добавим в начале подвыражеения '?:' стразу после открывающейся круглой скобки.		
# Тогда регулярное выражение примет вид "((?:[a-zA-Z]+-?)*[a-zA-Z]+)".
# Нам еще осталось включить в выражения слова с апострофом вида "didn't".		
# Для этого заменим в первом подвыражении "-?" на "[-']?".
# Все, на этом закончим улучшения регулярного выражения, его можно было бы улучшать и дальше, но остановимся на таком: 
# "((?:[a-zA-Z]+[-']?)*[a-zA-Z]+)"
		
		
class FrequencyDict:
	def __init__(self, pathToWordNetDict):
		
		# Определяем регулярное выражение для поиска английских слов
		self.wordPattern = re.compile("((?:[a-zA-Z]+[-']?)*[a-zA-Z]+)")
		
		# Частотный словарь(использум класс collections.Counter для поддержки подсчёта уникальных элементов в последовательностях) 		
		self.frequencyDict = Counter()

		# Создаем нормализатор английских слов
		self.lemmatizer = Lemmatizer(pathToWordNetDict)
		

		
	# Метод парсит файл, получает из нее слова
	def ParseBook(self, file):
		if file.endswith(".txt"): 
			self.__ParseTxtFile(file, self.__FindWordsFromContent)
		elif file.endswith(".pdf"):
			self.__ParsePdfFile(file, self.__FindWordsFromContent)					
		else:
			print('Warning: The file format is not supported: "%s"' %file)
			
			
	# Метод парсит файл в формате txt
	def __ParseTxtFile(self, txtFile, contentHandler):
		try:
			with open(txtFile, 'rU') as file:		
				for line in file:			# Читаем файл построчно
					contentHandler(line)	# Для каждой строки вызываем обработчик контента
		except Exception as e:
			print('Error parsing "%s"' % txtFile, e)	
			
			
	# Метод парсит файл в формате pdf
	def __ParsePdfFile(self, pdfFile, contentHandler):
		pass # пока не реализовано...
						

	# Метод находит в строке слова согласно своим правилам, нормализует их и затем добавляет в частотный словарь
	def __FindWordsFromContent(self, content):
		result = self.wordPattern.findall(content) 	# В строке найдем список английских слов				
		for word in result:
			word = word.lower()						# Приводим слово к нижнему регистру	
			lemma = self.lemmatizer.GetLemma(word) 	# Нормализуем слово
			if (lemma != ""):
				self.frequencyDict[lemma] += 1		# Добавляем в счетчик частотного словаря нормализованное слово
			else:
				self.frequencyDict[word] += 1		# Добавляем в счетчик частотного словаря не нормализованное слово	
	
	
	
	# Метод отдает первые countWord слов частотного словаря, отсортированные по ключу и значению
	def FindMostCommonElements(self, countWord):
		dict = list(self.frequencyDict.items())
		dict.sort(key=lambda t: t[0])
		dict.sort(key=lambda t: t[1], reverse = True)
		return dict[0 : int(countWord)]

		
		
		