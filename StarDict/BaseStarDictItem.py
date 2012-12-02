# -*- coding: utf-8 -*- 


import os

class BaseStarDictItem:
	def __init__(self, pathToDict, exp):
	
		# Определяем переменную с кодировкой
		self.encoding = "utf-8"
		
		# Получаем полный путь до файла
		self.dictionaryFile = self.__PathToFileInDirByExp(pathToDict, exp)
		
		# Получаем размер файла
		self.realFileSize = os.path.getsize(self.dictionaryFile)	

	
	
	# Метод ищет в папке path первый попапвшийся файл с расширением exp 
	def __PathToFileInDirByExp(self, path, exp):
		if not os.path.exists(path):
			raise Exception('Path "%s" does not exists' % path)	
		
		end = '.%s'%(exp)
		list = [f for f in os.listdir(path) if f.endswith(end)]
		if list: 
			return os.path.join(path, list[0]) # Возвращаем первый попавшийся
		else:
			raise Exception('File does not exist: "*.%s"' % exp)	
		
	
			
			