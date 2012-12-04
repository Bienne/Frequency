#!/usr/local/bin/python3
# -*- coding: utf-8 -*- 

import os

from Frequency.IniParser import IniParser
from Frequency.FrequencyDict import FrequencyDict
from StarDict.StarDict import StarDict

ConfigFileName="Settings.ini"

class Main:
	def __init__(self):
	
		self.listLanguageDict = [] 	# В этом массиве сохраним словари StarDict
		self.result = []  			# В этом массиве сохраним результат (само слово, частота, его перевод)

		try:
			# Создаем и инициализируем конфиг-парсер
			config = IniParser(ConfigFileName)	

			self.pathToBooks = config.GetValue("PathToBooks") 	 			# Считываем из ini файла переменную PathToBooks, которая содержит  путь до файлов(книг, документов и тд), из которых будут браться слова		
			self.pathResult = config.GetValue("PathToResult") 				# Считываем из ini файла переменную PathToResult, которая содержит путь для сохранения результата
			self.countWord = config.GetValue("CountWord") 	 				# Считываем из ini файла переменную CountWord, которая содержит количество первых слов частотного словаря, которые нужно получить
			self.pathToWordNetDict = config.GetValue("PathToWordNetDict") 	# Считываем из ini файла переменную PathToWordNetDict, которая содержит путь до словаря WordNet
			self.pathToStarDict = config.GetValue("PathToStarDict") 		# Считываем из ini файла переменную PathToStarDict, которая содержит путь до словарей в формате StarDict	
			
			# Отделяем пути словарей StarDict друг от друга и удаляем пробелы с начала и конца пути. Все пути заносим в список listPathToStarDict
			listPathToStarDict = [item.strip() for item in self.pathToStarDict.split(";")]

			# Для каждого из путей до словарей StarDict создаем свой языковый словарь
			for path in listPathToStarDict:
				languageDict = StarDict(path)
				self.listLanguageDict.append(languageDict) 

			# Получаем список книг, из которых будем получать слова
			self.listBooks = self.__GetAllFiles(self.pathToBooks)

			# Создаем частотный словарь		
			self.frequencyDict = FrequencyDict(self.pathToWordNetDict)			
	
			# Подготовка закончена, загружены словари StarDict и WordNet. Запускаем задачу на выполнение, то есть начинаем парсить текстовые файл, нормализовывать и считать слова			
			self.__Run()
		
		except Exception as e:
			print('Error: "%s"' %e)


	# Метод создает список файлов, расположенных в папке path	
	def __GetAllFiles(self, path):
		try:
			return [os.path.join(path, file) for file in os.listdir(path)]
		except Exception:
			raise Exception('Path "%s" does not exists' % path)		

		
	# Метод бежит по всем словарям, и возвращает перевод из ближайшего словаря. Если перевода нет ни в одном из словарей, возвращается пустая строка	
	def __GetTranslate(self, word):
		valueWord = ""
		for dict in self.listLanguageDict:
			valueWord = dict.Translate(word)
			if valueWord != "":
				return valueWord
		return valueWord
		
		
		
	# Метод запускает задачу на выполнение
	def __Run(self):					
		# Отдаем частотному словарю по одной книге	
		for book in self.listBooks:
			self.frequencyDict.ParseBook(book)		
			
		# Получаем первые countWord слов из всего получившегося списка английских слов			
		mostCommonElements = self.frequencyDict.FindMostCommonElements(self.countWord)
		
		# Получаем переводы для всех слов
		for item in mostCommonElements:
			word = item[0]
			counterWord = item[1]
			valueWord = self.__GetTranslate(word)
			self.result.append([counterWord, word, valueWord])	

		# Выведем результат 
		print(self.result)

		
		
	
if __name__ == "__main__":
	main = Main()

	

