class LineUtil:
	__line = None

	def __init__(self, view = None):
		self.view = view

	def setLine(self, selection):
		self.__line = self.view.full_line(selection)

	def getLine(self):
		return self.__line

	def getLineNumber(self):
		return self.view.rowcol(self.__line.begin())[0] + 1

	def getTagName(self):
		currentText =  self.view.find("cf[a-z]+\s", self.__line.begin())

		if currentText is not None:
			return self.view.substr(currentText)

		return ""