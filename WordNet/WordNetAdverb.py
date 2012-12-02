# -*- coding: utf-8 -*- 


from WordNet.BaseWordNetItem import BaseWordNetItem

# Класс для нормалзации наречий
# Класс наследуется от BaseWordNetItem

class WordNetAdverb(BaseWordNetItem):
	def __init__(self, pathToWordNetDict):
	
		# Конструктор родителя (BaseWordNetItem)
		BaseWordNetItem.__init__(self, pathToWordNetDict, 'adv.exc', 'index.adv')
		
		# У наречий есть только списки исключений(adv.exc) и итоговый список слов(index.adv).	
		# Правила замены окончаний при нормализации слова по правилам у наречий нет. 


			
