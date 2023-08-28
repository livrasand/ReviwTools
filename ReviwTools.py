import sublime
import sublime_plugin
import json

class ReviwToolsTestDefaultFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        region = sublime.Region(0, self.view.size())
        content = self.view.substr(region)

        try:
            data_list = json.loads(content)
            sorted_data = sorted(data_list, key=lambda x: x['title'].lower())
            sorted_content = json.dumps(sorted_data, indent=4, ensure_ascii=False)
            self.view.replace(edit, region, sorted_content)

            # Obtener el título de cada bloque y su posición
            block_positions = [
                "{} está en la posición {}".format(block['title'], i + 1)
                for i, block in enumerate(sorted_data)
            ]
            
            self.show_custom_panel("\n".join(block_positions))
        except Exception as e:
            error_message = "Error sorting JSON: " + str(e)
            sublime.error_message(error_message)
            self.show_copy_button(error_message)

    def show_custom_panel(self, message):
        output_view = self.view.window().create_output_panel("review_tools_custom_panel")
        output_view.run_command("insert", {"characters": message})
        output_view.set_read_only(True)
        self.view.window().run_command("show_panel", {"panel": "output.review_tools_custom_panel"})

    def show_copy_button(self, message):
        def copy_to_clipboard(text):
            sublime.set_clipboard(text)

        sublime.active_window().show_input_panel(
            "Error Message:", message, copy_to_clipboard, None, None
        )
