import sublime
import sublime_plugin
import constants
from line import LineUtil

class DEStandards:
	def __init__(self, view):
		self.view = view
		self.lineUtil = LineUtil(view)

	def validateCloseTags(self):
		selections = self.view.find_all("(\s{2,}|([^\s]))/>")

		for selection in selections:
			self.view.add_regions(constants.REGION_TAG, selections, "string")
			self.lineUtil.setLine(selection)

			if self.lineUtil.getLine() is not None:
				print "Warning ln[%s]: %s tag was not closed properly" % (self.lineUtil.getLineNumber(), self.lineUtil.getTagName())

	def validateTabs(self):
		selections = self.view.find_all("(\x09)+")

		for selection in selections:
			self.view.add_regions(constants.REGION_TAB, selections, "string")
			self.lineUtil.setLine(selection)

			if self.lineUtil.getLine() is not None:
				print "Warning ln[%s]: tab found" % self.lineUtil.getLineNumber()
