Plugin for CudaText.
The plugin is designed to display the status in the discord. 
Everything is simple and concise. Supports the following file formats for display:
* C'lang source file (.c, .h)
* C++'lang source file (.cpp, .h)
* D'lang source file (.d, .dd, .di)
* JavaScript source file (.js)
* TypeScript source file (.ts)
* Vue file (.vue)
* HTML/CSS file format (.html, .css)
* Rust source file (.rs)
* JSON/INI config format (.json, .ini)
* Bash/Batch script format (.bash, .bat, .cmd)
* Perl source file (.pl)
* Python source format (.py)
* Lua script/source format (.lua)
* PHP source file format (.php)
* GLSL shader source file format

How to make it work:
1. Install the cudadrp plugin.
2. Clone / download the repository to a temporary folder, 
from there move the `pypresence` folder to the editor folder: `.../CudaText/py/pypresence`
3. Restart the editor.

How to customize the desired label in the activity:
1. Create a file `cudadrp.ini` in the editor folder` settings`. 
2. They will write using the template to a file:
```ini
[rich_presence]
state_text=
details_text=
```
3. In the empty fields, enter the inscriptions that you need in the activity plate. 
To display data about the current file / project and other information, write an 
attribute next to any text, for example: {filename}, which will display the name 
of the file. The following attributes are available for displaying data:
* {filename} - Insert the name of the edited file.
* {project} - Insert the name of the project editet file.
* {line_count} - Insert the line count of the edited file.
* {count_symbols} - Count the number of characters.
* {vers} - The version of the editor being used.
* {font} - Shows the currently used font
* {edit} - Shows an asterisk if the file is not saved and is being edited, otherwise nothing.

Authors:
  TodNaz, https://github.com/Todnaz
License: MIT
