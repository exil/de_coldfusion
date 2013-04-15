import constants
import sublime
import sublime_plugin
import urllib
import de_util
from xml.dom import minidom
from de_base import LinterBase

class test(sublime_plugin.TextCommand):
	def run(self, edit):
		view = sublime.active_window().active_view()
	
		if (".cfc" in view.file_name()):
			self.baseLinter = LinterBase(view)

			print "test"

	# def validateCloseTags(self):
	# 	selections = self.view.find_all("(\s{2,}|([^\s]))/>")

	# 	for selection in selections:
	# 		self.view.add_regions(constants.REGION_TAG, selections, "string")
	# 		self.lineUtil.setLine(selection)

	# 		if self.lineUtil.getLine() is not None:
	# 			print "Warning ln[%s]: %s tag was not closed properly" % (self.lineUtil.getLineNumber(), self.lineUtil.getTagName())

	# def validateTabs(self):
	# 	selections = self.view.find_all("(\x09)+")

	# 	for selection in selections:
	# 		self.view.add_regions(constants.REGION_TAB, selections, "string")
	# 		self.lineUtil.setLine(selection)

	# 		if self.lineUtil.getLine() is not None:
	# 			print "Warning ln[%s]: tab found" % self.lineUtil.getLineNumber()
