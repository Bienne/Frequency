#!/usr/local/bin/python3
# -*- coding: utf-8 -*- 

from StarDict.BaseStarDictItem import BaseStarDictItem
from Frequency.IniParser import IniParser

class Ifo(BaseStarDictItem):

	def __init__(self, pathToDict):
		
		# Конструктор родителя (BaseStarDictItem)
		BaseStarDictItem.__init__(self, pathToDict, 'ifo')	

		# Создаем и инициализируем парсер
		self.iniParser = IniParser(self.dictionaryFile)

		# Считаем из ifo файла параметры
		# Если хотя бы одно из обязательных полей отсутствует, вызовется исключение и словарь не будет загружен
		self.bookName = self.__getParameterValue("bookname", None) 					# Название словаря [Обязательное поле]
		self.wordCount = self.__getParameterValue("wordcount", None) 				# Количество слов в ".idx" файле [Обязательное поле]
		self.synWordCount = self.__getParameterValue("synwordcount", "") 			# Количество слов в ".syn" файле синонимов [Обязательное поле, если есть файл ".syn"]
		self.idxFileSize = self.__getParameterValue("idxfilesize", None) 			# Размер (в байтах) ".idx" файла. Если файл сжат архиватором, то здесь указывается размер исходного несжатого файла [Обязательное поле]
		self.idxOffsetBits = self.__getParameterValue("idxoffsetbits", 32) 			# Размер числа в битах(32 или 64), содержащего внутри себя смещение до записи в файле .dict. Поле пояилось начиная с версии 3.0.0, до этого оно всегда было 32 [Необязательное поле]
		self.author = self.__getParameterValue("author", "")						# Автор словаря [Необязательное поле]
		self.email = self.__getParameterValue("email", "")							# Почта [Необязательное поле]
		self.description = self.__getParameterValue("description", "")				# Описание словаря [Необязательное поле]
		self.date = self.__getParameterValue("date", "")							# Дата создания словаря [Необязательное поле]
		self.sameTypeSequence = self.__getParameterValue("sametypesequence", None)	# Маркер, определяющий форматирование словарной статьи[Обязательное поле]
		self.dictType = self.__getParameterValue("dicttype", "")					# Параметр используется некоторыми словарными плагинами, например WordNet[Необязательное поле]			
	

	def __getParameterValue(self, key, defaultValue):
		try:
			return self.iniParser.GetValue(key) 
		except:
			if defaultValue != None:
				return defaultValue
			raise Exception('\n"%s" has invalid format (missing parameter: "%s")' % (self.dictionaryFile, key))	
			
	
			
		
