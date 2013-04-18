import constants
import de_util
import re
import sublime

class LinterBase(object):
	def __init__(self, view):
		self.view = view
		self.errors = []

	def getRegion(self, ln):
		point = self.getPoint(ln)
		return self.view.full_line(point)

	def getPoint(self, ln):
		return self.view.text_point(int(ln)-1, 0)

	def getLineNumber(self, region):
		line = self.view.full_line(region)
		lineNumber = self.view.rowcol(line.begin())[0] + 1

		return lineNumber

	def gotoLine(self, index):
		if index != -1:
			error = self.errors[index][0]
			ln = re.search("[0-9]+", error).group()
			self.view.show(self.getPoint(ln))

	def loadPanel(self, errorArray):
		self.errors = errorArray
		self.view.window().show_quick_panel(self.errors, self.gotoLine)

	def parseErrors(self, result):
		try:
			if result:
<<<<<<< HEAD
				self.view.add_regions(constants.DE_LINTER_REGION, result["regions"], "string", sublime.DRAW_OUTLINED)
=======
				self.view.add_regions(constants.DE_LINTER_REGION, result["regions"], "string", "", sublime.DRAW_OUTLINED)
>>>>>>> Update highlight

				if de_util.getSettings("show_drop_down"):
					result["errors"].sort(key=lambda tup: tup[0]) 

					self.loadPanel(result["errors"])

		except Exception as e:
			de_util.log("Error parsing results : " + str(e))
