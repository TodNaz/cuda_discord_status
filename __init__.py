import os
from cudatext import *
from cudax_lib import get_translation
import cuda_project_man as proj
from .pypresence import Presence
from threading import Thread
import time

_   = get_translation(__file__)  # I18N

def strbool(string):
    if string == "true":
        return 1
    else:
        return 0

class Command:
    def __init__(self):
        self.fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_discord_status.ini')
        self.config()
        
        self.rpc = Presence('913493054747447386')
        self.is_connect = 0
        
        self.last_large_icon = ""
        self.last_large_text = ""
        self.last_small_icon = ""
        self.last_small_text = ""
        self.last_state = ""
        self.last_details = ""
        self.last_make = 0
        self.last_time = time.time()

    def config(self):
        self.state_text = ini_read(self.fn_config, "rich_presence", "state_text" ,"Editing {filename}")
        self.details_text = ini_read(self.fn_config, "rich_presence", "details_text", "Workspace: {project}")
        self.autoconnect = strbool(ini_read(self.fn_config, "rich_presence", "autoconnect", "false"))
        self.count_time = strbool(ini_read(self.fn_config, "rich_presence", "count_time", "true"))
    
    def __connect_impl(self):
        try:
            self.rpc.connect()
            self.is_connect = 1
            app_log(LOG_CONSOLE_ADD, "[Discord Status] Connect!")
        except Exception:
            app_log(LOG_CONSOLE_ADD, "[Discord Status] Lost connect!")
    
    def connect_discord(self):
        self.__connect_impl()
    
    def connect(self):
        self.connect_discord()
        
        if not self.is_connect:
            msg_box("Failed to connect to discord!", MB_OK | MB_ICONERROR);

    def close_session(self):
        self.rpc.close()
        self.is_connect = 0
        
    def restart(self):
        self.close_session()
        self.connect_discord()
        
    def edit_card(self):
        result = dlg_input_ex(3, "Edit card", "Title of the card:", "Workspace {project}", "Details of the card:cuda", "Editing {filename}{edit}", "Do I need to count the time(true/false)","true")
        if result is None:
            return
        
        if result[2] not in ['true', 'false']:
            msg_box("Third parameter: You only had to specify `true` or `false`.", MB_OK | MB_ICONERROR)
            return
        
        ini_write(self.fn_config, "rich_presence", "state_text", result[0])
        ini_write(self.fn_config, "rich_presence", "details_text", result[1])
        ini_write(self.fn_config, "rich_presence", "count_time", result[2])
        
        self.state_text = result[0]
        self.details_text = result[1]
        self.count_time = strbool(result[2])
        
    def on_app_activate(self, ed_self):
        if self.last_make and self.is_connect:
            self.last_make = 0
            if self.count_time:
                if self.last_state == "":
                    ft = ed_self.get_prop(PROP_FONT)[0]
                    ed = ""
                    _state = self.state_text.format(filename="untitled", project="Empty", line_count=0, count_symbols=0, vers=app_exe_version(), font=ft, edit=ed)
                    _details = self.details_text.format(filename="untitled", project="Empty", line_count=0, count_symbols=0, vers=app_exe_version(), font=ft, edit=ed)
            
                self.rpc.update(large_image=self.last_large_icon, large_text=self.last_large_text, small_image="cuda", small_text="Cuda text", state=self.last_state, details=self.last_details, start=self.last_time)
            else:
                self.rpc.update(large_image=self.last_large_icon, large_text=self.last_large_text, small_image="cuda", small_text="Cuda text", state=self.last_state, details=self.last_details)
        
    def on_app_deactivate(self, ed_self):
        if self.is_connect:
            self.last_make = 1
            if self.count_time:
                self.rpc.update(large_image="inactive", large_text="Not active.", small_image="cuda", small_text="Cuda text", state="Not active.", start=time.time())
            else:
                self.rpc.update(large_image="inactive", large_text="Not active.", small_image="cuda", small_text="Cuda text", state="Not active.")
        
    def on_close(self, ed_self):
        pass
        
    def on_exit(self, ed_self):
        self.dissconnect()
        
    def on_open(self, ed_self):
        if self.is_connect:
            self.update_presence(ed_self)
        
    def on_lexer(self, ed_self):
        if self.is_connect:
            self.update_presence(ed_self)
        
    def on_save(self, ed_self):
        if self.is_connect:
            self.update_presence(ed_self)
        
    def on_start(self, ed_self):
        if self.autoconnect:
            self.connect_discord()
        
    def on_tab_change(self, ed_self):
        if self.is_connect:
            self.update_presence(ed_self)
        
    def on_change(self, ed_self):
        if self.is_connect:
            self.update_presence(ed_self)
        
    def update_presence(self, ed_self):
        proj_info = proj.global_project_info
        proj_filename = proj_info.get('filename')
        
        if proj_filename is not None:
            proj_basename = os.path.splitext(os.path.basename(proj_filename))[0]
        else:
            proj_basename = ""
        
        if proj_basename != "":
            name_proj = proj_basename
        else:
            nodes = proj_info.get('nodes')
            if nodes:
                name_proj = os.path.split(nodes[0])[-1:][0]
            else:
                name_proj = "Empty"
        
        name = os.path.basename(ed_self.get_filename())
        
        if name == "":
            name = "untitled"
        
        icon = "file"
        large_text = "Unknown type"
           
        lexer = ed_self.get_prop(PROP_LEXER_FILE, '')
        
        if lexer == "Python":
            icon = "python"
            large_text = "Python source file"
        elif lexer == "D":
            icon = "dlang"
            large_text = "D'lang source file"
        elif lexer == "C":
            icon = "clang"
            large_text = "C'lang source file"
        elif lexer == "C++":
            icon = "cpp"
            large_text = "C++'lang source file"
        elif lexer == "JavaScript":
            icon = "js"
            large_text = "JavaScript source file"
        elif lexer == "TypeScript":
            icon = "typescript"
            large_text = "TypeScript source file"
        elif lexer == "Rust":
            icon = "rust"
            large_text = "Rust source file"
        elif lexer == "JSON":
            icon = "json"
            large_text = "JSON data interchange format"
        elif lexer == "Ini files":
            icon = "ini"
            large_text = "INI configuration file format"
        elif lexer in ["Batch files", "Bash script"]:
            icon = "bash"
            large_text = "Script file format"
        elif lexer == "HTML":
            icon = "html"
            large_text = "HyperText Markup Language"
        elif lexer == "CSS":
            icon = "css"
            large_text = "Cascading Style Sheets"
        elif lexer == "Vue":
            icon = "vue"
            large_text = "Vue framework file format"
        elif lexer == "Perl":
            icon = "perl"
            large_text = "Perl source file format"
        elif lexer == "Lua":
            icon = "lua"
            large_text = "Lua script/source file format"
        elif lexer == "PHP":
            icon = "php"
            large_text = "PHP source file format"
        elif lexer == "GLSL":
            icon = "opengl"
            large_text = "GLSL shader source file format"
        elif lexer == "Pascal":
            icon = "pascal"
            large_image = "Pascal source file"
        elif name == "dub.json":
            icon = "dubb"
            large_text = "DUB package description file format"
        elif name == "package.json":
            icon = "npm"
            large_text = "NPM package description file format"
        
        if large_text == "":
            large_text = "Unknown format"
            
        lc = ed_self.get_line_count()
        cs = len(ed_self.get_text_all())
        ft = ed_self.get_prop(PROP_FONT)[0]
        ed = ""
        
        if ed_self.get_prop(PROP_MODIFIED):
            ed = "*"
            
        _state = self.state_text.format(filename=name, project=name_proj, line_count=lc, count_symbols=cs, vers=app_exe_version(), font=ft, edit=ed)
        _details = self.details_text.format(filename=name, project=name_proj, line_count=lc, count_symbols=cs, vers=app_exe_version(), font=ft, edit=ed)
        
        self.last_large_icon = icon
        self.last_large_text = large_text
        self.last_small_icon = "cuda"
        self.last_small_text = "Code editor `CudaText`"
        self.last_state = _state
        self.last_details = _details
        
        if self.count_time:
            self.rpc.update(large_image=icon, large_text=large_text, small_image="cuda", small_text="Code editor `CudaText`", state=_state, details=_details, start = self.last_time)
        else:
            self.rpc.update(large_image=icon, large_text=large_text, small_image="cuda", small_text="Code editor `CudaText`", state=_state, details=_details)
