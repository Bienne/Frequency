#!/usr/local/bin/python3
# -*- coding: utf-8 -*- 


from WordNet.BaseWordNetItem import BaseWordNetItem

# Класс для нормализации глаголов
# Класс наследуется от BaseWordNetItem

class WordNetVerb(BaseWordNetItem):
	def __init__(self, pathToWordNetDict):
	
		# Конструктор родителя (BaseWordNetItem)
		BaseWordNetItem.__init__(self, pathToWordNetDict, 'verb.exc', 'index.verb')


		# Правила замены окончаний при нормализации слова по правилам. К примеру, окончание "s" заменяется на "" , "ies" на и "y" тд.
		self.rule = (	
						["s"   , ""  ],
						["ies" , "y" ],
						["es"  , "e" ], 			
						["es"  , ""  ],	
						["ed"  , "e" ], 			
						["ed"  , ""  ],	
						["ing" , "e" ], 			
						["ing" , ""  ]	
					)

		# Метод получения нормализованной формы слова GetLemma(word) определен в базовом классе BaseWordNetItem