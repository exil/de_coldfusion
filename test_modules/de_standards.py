import sublime
import sublime_plugin

class DEStandards():
	def validateTags(self, view):
		selections = view.find_all("[^\s]/>")

		for selection in selections:
			view.add_regions(constants.REGION_TAG, selections, "string")
			lineNumber = (view.rowcol(selection.begin())[0] + 1)
			currentLine = view.full_line(selection)
			currentText = view.find("?icf[a-z]+\s", currentLine.begin())

			if currentText is not None:
				currentText = view.substr(currentText)
				print "warning ln[%s]: %s tag was not closed properly" % (lineNumber, text)
