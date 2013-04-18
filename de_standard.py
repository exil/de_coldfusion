import constants
import sublime
import sublime_plugin
import de_util
import de_base 

class DeStandard():
	def getResult(self, view):
		self.view = view
		self.baseLinter = de_base.LinterBase(view)

		errorResult = de_util.getResultObject()
		options = de_util.getSettings("de_standard_options")

		for option, value in options.iteritems():
			optionResult = self.__getOptionResult(option, value)

			if optionResult is not None:
				errorResult = de_util.mergeResults(errorResult, optionResult)

		return errorResult

### Private methods

	def __checkClosingTags(self):
		return self.__getErrors("(\s{2,}|([^\s]))/>", constants.STANDARD_CLOSING_TAG_MSG)

	def __checkDump(self):
		return self.__getErrors("<cfdump[^>]*>", constants.STANDARD_DUMP_MSG)

	def __checkAbort(self):
		return self.__getErrors("<cfabort[^>]*?>", constants.STANDARD_ABORT_MSG)

	def __checkTab(self):
		return self.__getErrors("(\x09)+",constants.STANDARD_TAB_MSG)

	def __checkIndentation(self):
		pass

	def __checkCFSetValidation(self):
		pass

	def __getOptionResult(self, option, value):
		OPTION_KEYS = {
			constants.DE_STANDARD_CLOSING_TAB : self.__checkClosingTags
			,constants.DE_STANDARD_DUMP : self.__checkDump
			,constants.DE_STANDARD_ABORT : self.__checkAbort
			,constants.DE_STANDARD_TAB : self.__checkTab
		}

		if (option in OPTION_KEYS.iterkeys()) and (value):
			return OPTION_KEYS[option]()

		return None

	def __getErrors(self, regex, errorText):
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
