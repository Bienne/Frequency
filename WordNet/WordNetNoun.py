#!/usr/local/bin/python3
# -*- coding: utf-8 -*- 


from WordNet.BaseWordNetItem import BaseWordNetItem

# Класс для работы с нормализацией существительных
# Класс наследуется от BaseWordNetItem

class WordNetNoun(BaseWordNetItem):
	def __init__(self, pathToWordNetDict):
	
		# Конструктор родителя (BaseWordNetItem)
		BaseWordNetItem.__init__(self, pathToWordNetDict, 'noun.exc', 'index.noun')
		
		# Правила замены окончаний при нормализации слова по правилам. К примеру, окончание "s" заменяется на "", "ses" заменяется на "s" и тд.
		self.rule = (	
						["s"    , ""    ],
						["’s"   , ""    ],
						["’"    , ""    ],							
						["ses"  , "s"   ],
						["xes"  , "x"   ], 			
						["zes"  , "z"   ],	
						["ches" , "ch"  ], 			
						["shes" , "sh"  ],
						["men"  , "man" ], 			
						["ies"  , "y"   ]					
					)	 
					
					
	# Метод возвращает лемму сушествительного(нормализованную форму слова)
	# Этот метод есть в базовом классе BaseWordNetItem, но нормализация существительных несколько отличается от нормализации других частей речи, 
	# поэтому метод в наследнике переопределен
	def GetLemma(self, word):	
		
		word = word.strip().lower() 
		
		# Если существительное слишком короткое, то к нормализованному виду мы его не приводим	
		if len(word) <= 2:
			return None	

		# Если существительное заканчивается на "ss", то к нормализованному виду мы его не приводим	
		if word.endswith("ss"):
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
		if (lemma != None):
			return lemma

			
		# Если существительное заканчивается на "ful", значит отбрасываем "ful", нормализуем оставшееся слово, а потом суффикс приклеиваем назад.
		# Таким образом, к примеру, из слова "spoonsful" после нормализации получится "spoonful"
		suff = ""
		if word.endswith("ful"): 
				word = word[:-3]	# Отрезаем суффикс "ful"
				suff = "ful"		# Отрезаем суффикс "ful", чтобы потом приклеить назад
		
		
		# На этом шаге понимаем, что слово не является исключением и оно не нормализовано, значит начинаем нормализовывать его по правилам. 
		lemma = self._RuleNormalization(word)
		if (lemma != None):
			lemma += suff					# Не забываем добавить суффикс "ful", если он был
			self.cacheWords[word] = lemma 	# Предварительно добавим нормализованное слово в кэш
			return lemma		

		return None	
		
		
		