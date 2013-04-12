import sublime, sublime_plugin

class WindowCommand(sublime_plugin.WindowCommand):
	ARR = ["ln 55","ln 100"]
	def run(self):
		self.window.show_quick_panel(self.ARR, self.onDone)

	def loadPanel(window, errorArr):
		window.show_quick_panel(errorArr, self.onDone)

	def printTest(self):
		print "test"

	def onDone(self, index):
		print self.ARR[index]
