import sublime
import sublime_plugin
from de_varscoper import VarScoper

class OnSave(sublime_plugin.EventListener):
	def on_post_save(self, view):
		settings = sublime.load_settings("CFLinter.sublime-settings")

		if settings.get("varscoper"):
			varScoper = VarScoper(view)
			varScoper.run()