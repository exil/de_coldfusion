import sublime
import sublime_plugin
from de_varscoper import VarScoper

class OnSave(sublime_plugin.EventListener):
	def on_post_save(self, view):
		varScoper = VarScoper(view)
		varScoper.run()