# import sublime
import sublime_plugin
# import constants
# from de_standards import DEStandards
# from function_util import FunctionUtil

class OnSave(sublime_plugin.EventListener):
	def on_post_save(self, view):
		pass
		# def on_post_save(self, view):
		# functionUtil = FunctionUtil()


		# # functionUtil.findFunctions(view)
		# view.erase_regions(constants.REGION_TAG)
		# view.erase_regions(constants.REGION_TAB)

		# deStandards = DEStandards(view)
		# deStandards.validateCloseTags()
		# deStandards.validateTabs()
		# reload(deStandards)
	


