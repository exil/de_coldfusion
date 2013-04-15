import constants
import sublime
import sublime_plugin
import de_util
from de_base import LinterBase

class DeStandard():
	def getResult(self, view):
		self.view = view
		self.baseLinter = LinterBase(view)

		errorResult = de_util.getResultObject()
		options = de_util.getSettings("de_standard_options")

		for option, value in options.iteritems():
			optionResult = self.getOptionResult(option, value)

			if optionResult is not None:
				errorResult = de_util.mergeResults(errorResult, optionResult)

		return errorResult

	def checkClosingTags(self):
		return self.getErrors("(\s{2,}|([^\s]))/>", constants.STANDARD_CLOSING_TAG_MSG)

	def checkDump(self):
		return self.getErrors("<cfdump[^>]*>", constants.STANDARD_DUMP_MSG)

	def checkAbort(self):
		return self.getErrors("<cfabort[^>]*?>", constants.STANDARD_ABORT_MSG)

	def checkTab(self):
		return self.getErrors("(\x09)+",constants.STANDARD_TAB_MSG)

	def checkIndentation(self):
		pass

	def checkCFSetValidation(self):
		pass

	def getOptionResult(self, option, value):
		OPTION_KEYS = {
			constants.DE_STANDARD_CLOSING_TAB : self.checkClosingTags
			,constants.DE_STANDARD_DUMP : self.checkDump
			,constants.DE_STANDARD_ABORT : self.checkAbort
			,constants.DE_STANDARD_TAB : self.checkTab
		}

		if (option in OPTION_KEYS.iterkeys()) and (value):
			return OPTION_KEYS[option]()

		return None

	def getErrors(self, regex, errorText):
		selections = self.view.find_all(regex, sublime.IGNORECASE)
		errorResult = None

		if selections:
			errorResult = de_util.getResultObject()
			errorResult["regions"] = selections

			for selection in selections:
				lineNumber = self.baseLinter.getLineNumber(selection)
				errorCaption = "DE Standard :: %s " % (lineNumber)
				errorResult["errors"].append(de_util.returnErrorArray(errorCaption, errorText))

		return errorResult
