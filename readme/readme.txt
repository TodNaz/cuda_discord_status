Plugin for CudaText.
Plugin is designed to display the user's status in the Discord. 
Everything is simple and concise. Supports the following file formats for display:

* Assembly (all existing Asm lexer variants)
* Bash/Batch script format (.bash, .bat, .cmd)
* C and C++ source file (.c, .h)
* D'lang source file (.d, .dd, .di)
* GLSL shader source file format
* Go'lang source file (.go)
* HTML and CSS file formats (.html, .css)
* JSON and Ini config formats (.json, .ini)
* JavaScript source file (.js)
* Lua script/source format (.lua)
* Markdown and reStructuredText markup (.md, .rst)
* PHP source file format (.php)
* Pascal source file (.pas)
* Perl source file (.pl)
* Python source format (.py)
* Rust source file (.rs)
* TypeScript source file (.ts)
* Vue file (.vue)
* XML file (.xml)
* YAML file (.yml)

How to make it work:
1. Download / clone the repository to the CudaText plugins folder "py".
2. Restart the editor.

How to customize the desired label in the activity:
1. Find the 'Plugins/Discord Status/Setting' panel and click on it. You will see a panel for editing the card.
or
1. Create a file `cuda_discord_status.ini` in the editor folder` settings` or edit if it exists/=. 
2. They will write using the template to a file:

```ini
[rich_presence]
state_text=
details_text=
autoconnect=false
count_time=true
inactive_status=true
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
* {edit} - Shows an asterisk if the file is not saved and is being edited, otherwise nothing.

autoconnect - boolean variable, whether it is necessary to connect to the discord automatically.
count_time - a boolean variable, whether it is necessary to count the time spent in the program and without action.
inactive_status - boolean value showing whether it is necessary to show a discard in the status of disappointment.

Author:
  TodNaz, https://github.com/Todnaz
License: MIT
