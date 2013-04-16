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
			optionResult = self.__getOptionResult(option, value)

			if optionResult is not None:
				errorResult = de_util.mergeResults(errorResult, optionResult)

		return errorResult

### Private methods

	def __checkDump(self):
		return self.__getErrors(regex="<cfdump[^>]*>", errorText=constants.STANDARD_DUMP_MSG)

	def __checkAbort(self):
		return self.__getErrors(regex="<cfabort[^>]*?>", errorText=constants.STANDARD_ABORT_MSG)

	def __checkTab(self):
		return self.__getErrors(regex="(\x09)+", errorText=constants.STANDARD_TAB_MSG)

	def __checkIndentation(self):
		selections = self.view.find_all("[\s].+<cf", sublime.IGNORECASE)
		errorRegions = []

		if selections:

			for selection in selections:
				if not ((selection.size() % 4) == 0):
					errorRegions.append(selection)

		return self.__getErrors(selections=errorRegions, errorText=constants.STANDARD_INDENTATION_MSG)

	def __checkCFSetValidation(self):
		return self.__getErrors(regex="<cfset([\s]*#)|([^=\r\n]*=[\s]*#)", errorText=constants.STANDARD_CFSET_VALIDATION_MSG)

	def __checkCloseExpressionTag(self):
		expressionTags = constants.CF_EXPRESSION_TAGS.split(",")
		result = None

		if expressionTags:
			result = de_util.getResultObject()

			for tag in expressionTags:
				tagResult = self.__getErrors(regex="<" + tag + "(>|[^/]+>)|((\s{2,}|([^\s]))/>)", errorText=constants.STANDARD_CLOSING_TAG_MSG)
				if tagResult is not None:
					result = de_util.mergeResults(result, tagResult)

		return result

	def __checkReturnFormat(self):
		pass

	def __checkDeclarationBreak(self):
		#Check line break between args, variable declaration and implementation
		pass 

	def _checkEndFunctionFormat(self):
		#check cfretun or line break
		pass

	def __getOptionResult(self, option, value):
		OPTION_KEYS = {
			 constants.DE_STANDARD_DUMP : self.__checkDump
			,constants.DE_STANDARD_ABORT : self.__checkAbort
			,constants.DE_STANDARD_TAB : self.__checkTab
			,constants.DE_STANDARD_RETURN : self.__checkReturnFormat
			,constants.DE_STANDARD_INDENTATION : self.__checkIndentation
			,constants.DE_STANDARD_CLOSE_EXPRESSION_TAG : self.__checkCloseExpressionTag
			,constants.DE_STANDARD_CFSET_VALIDATION : self.__checkCFSetValidation
		}

		if (option in OPTION_KEYS.iterkeys()) and (value):
			return OPTION_KEYS[option]()

		return None

	def __getErrors(self, regex=None, errorText=None, selections=None):
		if selections is None:
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
