# -*- coding: utf-8 -*- 


from struct import unpack
from StarDict.BaseStarDictItem import BaseStarDictItem


# Каждая запись внутри .idx файла состоит из 3-х полей, идущих друг за другом
# word_str;  		// Строка в формате utf-8, заканчивающаяся '\0'
# word_data_offset; // Смещение до записи в файле .dict (размер числа 32 или 64 бита)
# word_data_size;  	// Размер всей записи в файле .dict
		

class Idx(BaseStarDictItem):

	# Конструктор
	def __init__(self, pathToDict, wordCount, idxFileSize, idxOffsetBits):

		# Конструктор родителя (BaseStarDictItem)
		BaseStarDictItem.__init__(self, pathToDict, 'idx')
		
		self.idxDict = {}							# Словарь, self.idxDict = {'иностр.слово': [Смещение_до_записи_в_файле_dict, Размер_всей_записи_в_файле_dict], ...}	
		self.idxFileSize = int(idxFileSize) 		# Размер файла .idx, записанный в .ifo файле
		self.idxOffsetBytes = int(idxOffsetBits/8)	# Размер числа, содержащего внутри себя смещение до записи в файле .dict. Переводим в байты и приводим к числу
		self.wordCount = int(wordCount)				# Количество слов в ".idx" файле
		
		# Проверяем целостность словаря (информация в .ifo файле о размере .idx файла [idxfilesize] должна совпадать с его реальным размером)
		self.__CheckRealFileSize()
		
		# Заполняем словарь self.idxDict данными из файла .idx
		self.__FillIdxDict()
	
		# Проверяем целостность словаря (информация в .ifo файле о количестве слов [wordcount] должна совпадать с реальным количеством записей в .idx файле)
		self.__CheckRealWordCount()
	
	
	# Функция сверяет размер файла, записанный в .ifo файле, с ее реальным размером и в случае расхождений генерирует исключение	
	def __CheckRealFileSize(self):
		if self.realFileSize != self.idxFileSize:
			raise Exception('size of the "%s" is incorrect' %self.dictionaryFile)

			
	# Функция сверяет количестве слов, записанное в .ifo файле, с реальным количеством записей в файле .idx и в случае расхождений генерирует исключение			
	def __CheckRealWordCount(self):
		realWordCount = len(self.idxDict)
		if realWordCount != self.wordCount:
			raise Exception('word count of the "%s" is incorrect' %self.dictionaryFile)
	

	# Функция считывает из потока данных массив байтов заданной длины, затем преобазует байткод в число	
	def __getIntFromByteArray(self, sizeInt, stream):
		byteArray = stream.read(sizeInt) # Получили массив байтов, отведенных под число
		
		# Определим формат пробразования в числовой формат 
		formatCharacter = 'L' 			 # Формат означает "unsigned long" (для sizeInt = 4)
		if sizeInt == 8:
			formatCharacter = 'Q'		 # Формат означает "unsigned long long" (для sizeInt = 8)
		format = '>' + formatCharacter	 # Общий формат будет состоять из: "направление порядка байтов" + "формат числа"
		# Строка '>' - означает, что мы распаковываем байткод в число int(размера formatCharacter) от старшего бита к младшему.
		
		integer = (unpack(format, byteArray))[0] # Распаковываем массив байтов в заданном формате	
		return int(integer) 
		
		

	# Функция разделяет файл .idx на отдельные записи (запись состоит из 3-х полей) и каждую запись добавляет в словарь self.idxDict
	def __FillIdxDict(self):
		languageWord = ""
		with open(self.dictionaryFile, 'rb') as stream:
			while True:
				byte = stream.read(1) 	# Читаем один байт
				if not byte: break  	# Если байтов больше нет, то выходим из цикла
				if byte != b'\0':		# Если байт не является символом окончания строки '\0', то прибавляем его к слову
					languageWord += byte.decode("utf-8")
				else: 
					# Если дошли до '\0', то считаем, что слово закончилось и дальше идут два числа ("Смещение до записи в файле dict" и "Размер всей записи в файле dict")
					wordDataOffset = self.__getIntFromByteArray(self.idxOffsetBytes, stream) 	# Получили первое число "Смещение до записи в файле dict"
					wordDataSize = self.__getIntFromByteArray(4, stream)						# Получили второе число "Размер всей записи в файле dict"

					self.idxDict[languageWord] = [wordDataOffset, wordDataSize] # Добавим в словарь self.idxDict запись: иностранное слово + смещение + размер данных
					languageWord = "" 											# Обнуляем переменную, поскольку начинается следующая струтура
			

			
	# Функция возвращает расположение слова в файле .dict ("Смещение до записи в файле dict" и "Размер всей записи в файле dict").
	# Если такого слова в словаре нет, функция возвращает None
	def GetLocationWord(self, word):			
		try:
			return self.idxDict[word]		
		except KeyError:
			return [None, None]	
			
			