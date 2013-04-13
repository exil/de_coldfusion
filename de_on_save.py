import sublime
import sublime_plugin
import constants

class OnSave(sublime_plugin.EventListener):
	def on_post_save(self, view):
		settings = sublime.load_settings("DELinter.sublime-settings")

		linters = settings.get("de_linter")

		if linters:
			window = sublime.active_window().active_view().erase_regions(constants.VARSCOPER_REGION)

			for linter in linters:
				view.run_command(linter)


