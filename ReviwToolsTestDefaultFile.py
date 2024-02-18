import sublime
import sublime_plugin
import json
from urllib import request, error

class ReviwToolsTestDefaultFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            # Obtener el contenido del archivo
            region = sublime.Region(0, self.view.size())
            content = self.view.substr(region)

            # Cargar el contenido como JSON y ordenarlo por título
            data_list = json.loads(content)
            sorted_data = sorted(data_list, key=lambda x: x['title'].lower())
            sorted_content = json.dumps(sorted_data, indent=4, ensure_ascii=False)
            self.view.replace(edit, region, sorted_content)

            # Obtener el título de cada bloque y su posición
            block_positions = [
                "{} está en la posición {}".format(block['title'], i + 1)
                for i, block in enumerate(sorted_data)
            ]

            # Verificar la URL de descarga para cada bloque
            for block in sorted_data:
                url = block.get('downloadURL')
                if url:
                    try:
                        response = request.urlopen(url)
                        if response.getcode() == 200:
                            block['downloadURL_status'] = 'OK'
                        else:
                            block['downloadURL_status'] = 'Error {}'.format(response.getcode())
                    except error.URLError as e:
                        block['downloadURL_status'] = 'Error {}'.format(e.reason)

                # Verificar la imageURL para cada bloque
                image_url = block.get('imageURL')
                if image_url:
                    try:
                        response = request.urlopen(image_url)
                        if response.getcode() == 200:
                            block['imageURL_status'] = 'OK'
                        else:
                            block['imageURL_status'] = 'Error {}'.format(response.getcode())
                    except error.URLError as e:
                        block['imageURL_status'] = 'Error {}'.format(e.reason)

            # Construir el mensaje a mostrar en el panel de salida
            message = "\n".join(block_positions)
            for block in sorted_data:
                if 'downloadURL_status' in block:
                    message += "\n{} - Estado de la URL de descarga: {}".format(block['title'], block['downloadURL_status'])
                if 'imageURL_status' in block:
                    message += "\n{} - Estado de la imageURL: {}".format(block['title'], block['imageURL_status'])

            # Mostrar el mensaje en el panel de salida
            self.show_custom_panel(message)

        except json.JSONDecodeError:
            # Si hay un error al cargar el JSON, mostrar un mensaje de error
            error_message = "Error: El contenido del archivo no es JSON válido."
            sublime.error_message(error_message)

        except Exception as e:
            # Si ocurre cualquier otro tipo de error, mostrar un mensaje de error
            error_message = "Error: " + str(e)
            sublime.error_message(error_message)

    def show_custom_panel(self, message):
        # Mostrar el mensaje en el panel de salida
        output_view = self.view.window().create_output_panel("review_tools_custom_panel")
        output_view.run_command("insert", {"characters": message})
        output_view.set_read_only(True)
        self.view.window().run_command("show_panel", {"panel": "output.review_tools_custom_panel"})
