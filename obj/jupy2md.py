import base64
import json
import os
import re

CWD = os.path.dirname(os.path.abspath(__file__))

SPLITS = ['//', '/', "\\"]

IMG_LINK = {"Markdown": '![](./{folder}/{filename})\n',
            "HTML": '<img align="center" width="90%" src="./{folder}/{filename}" alt="{alttext}">\n',
            "Wikilinks": "[[{filename}]]\n"}

class Jupy2Md:
    IMG_FOLDER = "img_md"

    def __init__(self, filepath:str, settings:dict={}):
        """
        - filepath: str, path of the .ipynb to be converted
        - settings: dict, default={}
            - "md_text": bool, default=True, markdown text
            - "md_images": bool, default=True, images within markdown
            - "code": bool, default=True, code blocks
            - "code_output": bool, default=True, code printout
            - "code_text": bool, default=True, code text
            - "code_images": bool, default=True, code images 
            - "export": bool, default=False, export (save) file and img
            - "img_link": str, default='HTML', image linking style
            - "export_folder": str, default=None, export folder
        """
        self._initialize_attributes(filepath)
        self._retrieve_settings(settings)
        self._define_names()
        self._read_jupy()
        self.convert_to_md()
        if self.export:
            self.export_md()
    
    def _initialize_attributes(self, filepath:str):
        self.filepath = os.path.abspath(filepath)
        self.images_raw = {}

    def _retrieve_settings(self, settings:dict={}):
        self.md_text = settings.get("md_text", True)
        self.md_images = settings.get("md_images", True)
        self.code = settings.get("code", True)
        self.code_output = settings.get("code_output", True)
        self.code_text = settings.get("code_text", True)
        self.code_images = settings.get("code_images", True)
        self.export = settings.get("export", False)
        self.img_link = settings.get("img_link", "HTML")
        self.export_folder = settings.get("export_folder", None)

        self.img_link_format = IMG_LINK[self.img_link]

    def _define_names(self):
        filename_temp = self.filepath
        for split in SPLITS:
            if split in self.filepath:
                filename_temp = self.filepath.split(split)[-1]
                break
        self.filename_with_ext = filename_temp
        self.filename = filename_temp[:-len(".ipynb")]
        
    def _build_export_paths(self, export_folder=None):
        if export_folder:
            self.export_folder = os.path.abspath(export_folder)
        if self.export_folder:
            self.folder_path = os.path.join(self.export_folder, self.filename)
        else:
            self.folder_path = os.path.join(self.filepath[:-len(self.filename_with_ext)], self.filename)
            
        self.img_path = os.path.join(self.folder_path, self.IMG_FOLDER)
        
        self.md_filename = self.filename+".md"
        self.md_filepath = os.path.join(self.folder_path, self.md_filename)
        pass

    def _read_jupy(self):
        with open(self.filepath, 'r') as f:
            self.json_raw = json.load(f)
        self.language = self.json_raw["metadata"]["kernelspec"]["language"]

    @staticmethod
    def _build_codeblock(content:list[str], language:str="text") -> str:
        text = f'\n```{language}\n'
        text += ''.join(e for e in content)
        text += '\n```\n'
        return text

    def convert_to_md(self, settings=None):
        if settings:
            self._retrieve_settings(settings)
        self.text = ''
        img_k = 0
        for cell in self.json_raw['cells']:
        # code block
            if cell['cell_type'] == 'code':
                # this is the code
                if self.code:
                    self.text += self._build_codeblock(cell['source'], self.language)

                for output in cell['outputs']:  # code output
                    if self.code_text:  # text output
                        if 'text' in output:
                            self.text += self._build_codeblock(output['text'])

                    if 'data' in output:
                        if self.code_output:  # code outputs
                            if 'text/plain' in output['data']:
                                self.text += self._build_codeblock(output['data']['text/plain'])

                        # images
                        if self.code_images:
                            if 'image/png' in output['data']:
                                s = output['data']['image/png']
                                ifname = f'image{img_k}.png'
                                self.images_raw[ifname] = s
                                img_k += 1

                                self.text += self.build_img_link(ifname)
                                self.text += '\n'

            # markdown block
            elif cell['cell_type'] == 'markdown':
                # get markdown embedded images
                img_embedded_names = None
                if "attachments" in cell:
                    img_embedded_names = {im:"" for im in cell["attachments"].keys()}
                    if self.md_images:
                        for img_e_n in img_embedded_names:
                            s = cell["attachments"][img_e_n]["image/png"]
                            ifname = f'image{img_k}.png'
                            self.images_raw[ifname] = s
                            img_embedded_names[img_e_n] = ifname
                            img_k += 1

                # get content of markdown
                if self.md_text:
                    text = ''.join(e for e in cell['source'])
                    if img_embedded_names:
                        " img links are replaced here "
                        for img_e_n in img_embedded_names:
                            replacement = self.build_img_link(img_embedded_names[img_e_n]) if self.md_images else "\n"
                            pattern = re.escape(f"![{img_e_n}](attachment:{(img_e_n)})\n")
                            text = re.sub(pattern, replacement, text)

                    self.text += text + '\n'

    def build_img_link(self, ifname):
        if self.img_link == "Markdown":
            return self.img_link_format.format(folder=self.IMG_FOLDER, filename=ifname)
        if self.img_link == "HTML":
            return self.img_link_format.format(folder=self.IMG_FOLDER, filename=ifname, alttext=ifname)
        if self.img_link == "Wikilinks":
            return self.img_link_format.format(filename=ifname)

    def export_md(self, export_folder=None):
        self._build_export_paths(export_folder=export_folder)
        self.export = True

        os.makedirs(self.folder_path, exist_ok=True)
        with open(self.md_filepath, "w") as f:
            f.write(self.text)

        if self.images_raw: 
            os.makedirs(self.img_path, exist_ok=True)
            for ifname in self.images_raw:
                self._decode_save_image(ifname)
        
    def _decode_save_image(self, ifname):
        with open(os.path.join(self.img_path, ifname), 'wb') as f:
            f.write(base64.decodebytes(self.images_raw[ifname].encode('latin-1')))

if __name__ == "__main__":
    import sys
    Jupy2Md(sys.argv[1], {"export":True})