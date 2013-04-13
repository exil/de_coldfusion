import constants
import de_util
import re

class LinterBase(object):
	def __init__(self, view):
		self.view = view
		self.errors = []

	def loadPanel(self, errorArray):
		self.errors = errorArray
		self.view.window().show_quick_panel(errorArray, self.gotoLine)

	def getRegion(self, ln):
		point = self.getPoint(ln)
		return self.view.full_line(point)

	def getPoint(self, ln):
		return self.view.text_point(int(ln)-1, 0)

	def gotoLine(self, index):
		pass
		if index != -1:
			error = self.errors[index][0]
			ln = re.search("[0-9]+", error).group()
			self.view.show(self.getPoint(ln))

	def parseErrors(self, result):
		try:
			self.view.add_regions(constants.VARSCOPER_REGION, result["regions"], "string")
			self.loadPanel(result["errors"])

		except Exception as e:
			util.log("Error parsing results : " + str(e))
