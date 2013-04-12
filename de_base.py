class LinterBase(object):
	def __init__(self, view):
		self.view = view	

	def loadPanel(self, errorArray):
		self.view.window().show_quick_panel(errorArray, self.gotoLine)

	def getRegion(self, ln):
		point = self.getPoint(ln)
		return self.view.full_line(point)

	def getPoint(self, ln):
		return self.view.text_point(int(ln)-1, 0)

	def gotoLine(self, ln):
		ln = self.errorArray[ln]
		self.view.show(self.getPoint(ln))
