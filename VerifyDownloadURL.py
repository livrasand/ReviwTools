import sublime
import sublime_plugin
import json
import requests

class VerifyDownloadURLCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        region = sublime.Region(0, self.view.size())
        content = self.view.substr(region)

        try:
            data = json.loads(content)

            if "downloadURL" in data:
                download_url = data["downloadURL"]
                if is_valid_download_url(download_url):
                    sublime.message_dialog("La downloadURL es válida.")
                else:
                    sublime.message_dialog("La downloadURL no es válida.")
            else:
                sublime.message_dialog("No se encontró la clave 'downloadURL' en el JSON.")
        except Exception as e:
            error_message = "Error al analizar el JSON: " + str(e)
            sublime.error_message(error_message)

    def is_valid_download_url(url):
        try:
            response = requests.head(url)
            if response.status_code == 200 and "Content-Type" in response.headers and response.headers["Content-Type"] in ["application/octet-stream", "application/x-download"]:
                return True
            else:
                return False
        except Exception:
            return False
