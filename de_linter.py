import sublime
import sublime_plugin
import constants
import de_util
import json
from de_varscoper import DeVarscoper
from de_standard import DeStandard
from de_base import LinterBase

class DeLinter(sublime_plugin.EventListener):
	def on_post_save(self, view):
		self.view = sublime.active_window().active_view()
		self.view.erase_regions(constants.DE_LINTER_REGION)

		linters = de_util.getSettings("de_linter")

		if (".cfc" in self.view.file_name()) and linters:
			result = self.__getErrorResults(linters)

			linterBase = LinterBase(self.view)
			linterBase.parseErrors(result)

### Private methods

	def __getErrorResults(self, linters):
		result = de_util.getResultObject()

		for linter, value in linters.iteritems():
			errorResult = self.__getLinterResult(linter, value)

			if errorResult is not None:
				result = de_util.mergeResults(result, errorResult)

		return result

	def __getLinterResult(self, linter, value):
		OPTION_KEYS = {
			constants.DE_VARSCOPER : DeVarscoper().getResult
			,constants.DE_STANDARD : DeStandard().getResult
		}

		if (linter in OPTION_KEYS) and (value):
			return OPTION_KEYS[linter](self.view)

		return None