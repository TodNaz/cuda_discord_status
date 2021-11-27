import os
from cudatext import *
from cudax_lib import get_translation
import cuda_project_man as proj
from .pypresence import Presence
import time

_   = get_translation(__file__)  # I18N

class Command:
    def __init__(self):
        self.fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_discord_status.ini')
        
        self.state_text = ini_read(self.fn_config, "rich_presence", "state_text" ,"Editing {filename}")
        self.details_text = ini_read(self.fn_config, "rich_presence", "details_text", "Workspace: {project}")
        
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
        self.fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_discord_status.ini')
        self.state_text = ini_read(self.fn_config, "rich_presence", "state_text" ,"Editing {filename}")
        self.details_text = ini_read(self.fn_config, "rich_presence", "details_text", "Workspace: {project}")
    
    def __connect_impl(self):
        self.rpc.connect()
        self.is_connect = 1
        msg_status("[Discord Rich Presence] Connect!")
    
    def connect_discord(self):
        self.__connect_impl()
    
    def connect(self):
        self.connect_discord()

    def close_session(self):
        self.rpc.close()
        self.is_connect = 0
        
    def restart(self):
        self.close_session()
        self.connect_discord()
        
    def on_app_activate(self, ed_self):
        if self.last_make:
            self.last_make = 0
            self.rpc.update(large_image=self.last_large_icon, large_text=self.last_large_text, small_image="cuda", small_text="Cuda text", state=self.last_state, details=self.last_details, start=self.last_time)
        
    def on_app_deactivate(self, ed_self):
        if self.is_connect:
            self.last_make = 1
            self.rpc.update(large_image="inactive", large_text="Not active.", small_image="cuda", small_text="Cuda text", state="Not active.", start=time.time())
        
    def on_close(self, ed_self):
        pass
        
    def on_exit(self, ed_self):
        self.dissconnect()
        
    def on_open(self, ed_self):
        self.update_presence(ed_self)
        
    def on_lexer(self, ed_self):
        self.update_presence(ed_self)
        
    def on_save(self, ed_self):
        if self.is_connect:
            self.update_presence(ed_self)
        
    def on_start(self, ed_self):
        self.connect_discord()
        
    def on_tab_change(self, ed_self):
        if self.is_connect:
            self.update_presence(ed_self)
        
    def on_change(self, ed_self):
        if self.is_connect:
            self.update_presence(ed_self)
        
    def update_presence(self, ed_self):
        proj_info = proj.global_project_info
        proj_basename = os.path.splitext(os.path.basename(proj_info['filename']))[0]
        
        if proj_basename != "":
            name_proj = proj_basename
        else:
            nodes = proj_info['nodes']
            if nodes:
                name_proj = os.path.split(nodes[0])[-1:][0]
            else:
                name_proj = "Empty"
        
        name = os.path.basename(ed_self.get_filename())
        
        if name == "":
            name = "untitled"
        
        icon = "file"
        large_text = ext
           
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
        elif name == "dub.json":
            icon = "dubb"
            large_text = "DUB package description file format"
        elif name == "package.json":
            icon = "npm"
            large_text = "NPM package description file format"
            
        self.last_large_icon = icon
        self.last_large_text = large_text
        self.last_small_icon = "cuda"
        self.last_small_text = "CudaText"
        self.last_state = "Editing " + name
        self.last_details = name_proj
        
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
        
        self.rpc.update(large_image=icon, large_text=large_text, small_image="cuda", small_text="Code editor `CudaText`", state=_state, details=_details, start = self.last_time)
