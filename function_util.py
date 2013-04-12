import sublime
import sublime_plugin

class FunctionUtil():
	def findFunctions(self, view):
		functionSelections = view.find_all("<cffunction ([^\n]*\n+)+(.*?)</cffunction>")

		print functionSelections
