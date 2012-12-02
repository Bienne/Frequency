# -*- coding: utf-8 -*- 

import os

class BaseWordNetItem:
	# Конструктор
	def __init__(self, pathWordNetDict, excFile, indexFile):
	
		self.rule = ()												# Правила замены окончаний при нормализации слова по правилам.
		
		self.wordNetExcDict = {} 									# Словарь исключений
		self.wordNetIndexDict = [] 									# Индексный массив	
		
		self.excFile = os.path.join(pathWordNetDict, excFile)		# Получим путь до файла исключений	
		self.indexFile = os.path.join(pathWordNetDict, indexFile)	# Получим путь до индексного словаря
		
		self.__ParseFile(self.excFile, self.__AppendExcDict)		# Заполним словарь исключений
		self.__ParseFile(self.indexFile, self.__AppendIndexDict)	# Заполним индексный массив 

		self.cacheWords = {}										# Немного оптимизации. Кэш для уже нормализованных слов, ключ - ненормализованное слово, значение - нормализованное слово	
		
			
			
	# Метод добавляет в словарь исключений одно значение. 
	# Файл исключений представлен в формате: [слово-исключение][пробел][лемма]	
	def __AppendExcDict(self, line):			
		# При разборе строки из файла, каждую строку разделяем на 2 слова и заносим слова в словарь(первое слово - ключ, второе - значение). При этом не забываем убрать с концов пробелы
		group = [item.strip() for item in line.replace("\n","").split(" ")]
		self.wordNetExcDict[group[0]] = group[1]

			
			
	# Метод добавляет в индексный массив одно значение.
	def __AppendIndexDict(self, line):			
		# На каждой строке берем только первое слово
		group = [item.strip() for item in line.split(" ")]
		self.wordNetIndexDict.append(group[0]) 
		

	# Метод открывает файл на чтение, читает по одной строке и вызывает для каждой строки функцию, переданную в аргументе
	def __ParseFile(self, file, contentHandler):	
		try:
			with open(file, 'r') as openFile: 
				for line in openFile:
					contentHandler(line)	# Для каждой строки вызываем обработчик контента
		except Exception as e:
			raise Exception('File does not load: "%s"' %file)	
			
			
	# Метод возвращает значение ключа в словаре. Если такого ключа в словаре нет, возвращается пустое значение. 
	# Под словарем здесь подразумевается просто структура данных 
	def _GetDictValue(self, dict, key):
		try:
			return dict[key]		
		except KeyError:
			return None
		
		
		
	# Метод проверяет слово на существование, и возвращает либо True, либо False.
	# Для того, чтобы понять, существует ли слово, проверяется индексный массив(там хранится весь список слов данной части речи).	
	def _IsDefined(self, word):
		if word in self.wordNetIndexDict:
			return True
		return False		
	
	
	
	# Метод возвращает лемму(нормализованную форму слова)			
	def GetLemma(self, word):
	
		word = word.strip().lower() 
	
		# Пустое слово возвращаем обратно
		if word == None:
			return None	

		# Пройдемся по кэшу, возможно слово уже нормализовывалось раньше и результат сохранился в кэше
		lemma = self._GetDictValue(self.cacheWords, word)
		if lemma != None:
			return lemma
			
		# Проверим, если слово уже в нормализованном виде, вернем его же
		if self._IsDefined(word):
			return word
			
			
		# Пройдемся по исключениям, если слово из исключений, вернем его нормализованную форму
		lemma = self._GetDictValue(self.wordNetExcDict, word)
		if lemma != None:
			return lemma
	
			
		# На этом шаге понимаем, что слово не является исключением и оно не нормализовано, значит начинаем нормализовывать его по правилам. 
		lemma = self._RuleNormalization(word)
		if lemma != None:
			self.cacheWords[word] = lemma 	# Предварительно добавим нормализованное слово в кэш
			return lemma		

		return None	
		
		
		
	# Нормализация слова по правилам (согласно грамматическим правилам, слово приводится к нормальной форме)
	def _RuleNormalization(self, word):
		# Бежим по всем правилам, смотрим совпадает ли окончание слова с каким либо правилом, если совпадает, то заменяем окончние.	
		for replGroup in self.rule:
			endWord = replGroup[0]			
			if word.endswith(endWord): 	
				lemma = word					# Копируем во временную переменную
				lemma = lemma.rstrip(endWord)	# Отрезаем старое окончание
				lemma += replGroup[1]			# Приклеиваем новое окончание
				if self._IsDefined(lemma):		# Проверим, что получившееся новое слово имеет право на существование, и если это так, то вернем его
					return lemma	
		return None
		