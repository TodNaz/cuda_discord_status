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
            if len(nodes) != 0:
                name_proj = os.path.split(nodes[0])[-1:][0]
            else:
                name_proj = "Empty"
        
        name = os.path.basename(ed_self.get_filename())
        
        if name == "":
            name = "untitled"
        
        ext = os.path.splitext(ed_self.get_filename())[1][1:]
        icon = "file"
        large_text = ext
        
        if name == "dub.json":
            icon = "dubb"
            large_text = "DUB package description file format"
        elif name == "package.json":
            icon = "npm"
            large_text = "NPM package description file format"
        elif ext == "py" or ext == "pyd":
            icon = "python"
            large_text = "Python source file"
        elif ext == "d" or ext == "dd" or ext == "di":
            icon = "dlang"
            large_text = "D'lang source file"
        elif ext == "c" or ext == "h":
            icon = "clang"
            large_text = "C'lang source file"
        elif ext == "cpp" or ext == "hpp":
            icon = "cpp"
            large_text = "C++'lang source file"
        elif ext == "js":
            icon = "js"
            large_text = "JavaScript source file"
        elif ext == "ts":
            icon = "typescript"
            large_text = "TypeScript source file"
        elif ext == "rs":
            icon = "rust"
            large_text = "Rust source file"
        elif ext == "json":
            icon = "json"
            large_text = "JSON data interchange format"
        elif ext == "ini":
            icon = "ini"
            large_text = "INI configuration file format"
        elif ext == "cmd":
            icon = "bash"
            large_text = "CMD script file format"
        elif ext == "bat":
            icon = "bash"
            large_text = "Batch script file format"
        elif ext == "sh":
            icon = "bash"
            large_text = "Shell script file format"
        elif ext == "html":
            icon = "html"
            large_text = "HyperText Markup Language"
        elif ext == "css":
            icon = "css"
            large_text = "Cascading Style Sheets"
        elif ext == "vue":
            icon = "vue"
            large_text = "Vue framework file format"
        elif ext == "pl":
            icon = "perl"
            large_text = "Perl source file format"
        elif ext == "lua":
            icon = "lua"
            large_text = "Lua script file format"
        elif ext == "php":
            icon = "php"
            large_text = "PHP source file format"
        elif ext == "glsl" or ext == "vert" or ext == "frag" or ext == "geom":
            icon = "opengl"
            large_text = "GLSL shader source file format"
            
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
