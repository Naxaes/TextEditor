from tkinter.filedialog import *
import subprocess
import os

WIDTH, HEIGHT = 800, 600

JAVA = 'JAVA'
TED  = 'TED'
COMPILER = TED

SOURCE_DIRECTORY = os.path.join(os.getcwd(), 'sources')
BYTE_DIRECTORY   = os.path.join(os.getcwd(), 'compiled')

TED_INTERPRETER = 'ProgrammingLanguageTED/interpreter2.py'


# '\y' Word boundary
# https://stackoverflow.com/questions/21855764/search-tkinter-text-widget-contents-using-regular-expression
JAVA_KEYWORDS = [
    'abstract', 'continue', 'for', 'new', 'switch', 'assert', 'default',
    'goto', 'package', 'synchronized', 'boolean', 'do', 'if', 'private',
    'this', 'break', 'double', 'implements', 'protected', 'throw', 'byte',
    'else', 'import', 'public', 'throws', 'case', 'enum', 'instanceof',
    'return', 'transient', 'catch', 'extends', 'int', 'short', 'try', 'char',
    'final', 'interface', 'static', 'void', 'class', 'finally', 'long',
    'strictf', 'volatile', 'const', 'float', 'native', 'super', 'while',

]
JAVA_KEYWORD_PATTERNS = {
    'abstract'    : r'\yabstract\y',
    'continue'    : r'\ycontinue\y',
    'for'         : r'\yfor\y',
    'new'         : r'\ynew\y',
    'switch'      : r'\yswitch\y',
    'assert'      : r'\yassert\y',
    'default'     : r'\ydefault\y',
    'goto'        : r'\ygoto\y',
    'package'     : r'\ypackage\y',
    'synchronized': r'\ysynchronized\y',
    'boolean'     : r'\yboolean\y',
    'do'          : r'\ydo\y',
    'if'          : r'\yif\y',
    'private'     : r'\yprivate\y',
    'this'        : r'\ythis\y',
    'break'       : r'\ybreak\y',
    'double'      : r'\ydouble\y',
    'implements'  : r'\yimplements\y',
    'protected'   : r'\yprotected\y',
    'throw'       : r'\ythrow\y',
    'byte'        : r'\ybyte\y',
    'else'        : r'\yelse\y',
    'import'      : r'\yimport\y',
    'public'      : r'\ypublic\y',
    'throws'      : r'\ythrows\y',
    'case'        : r'\ycase\y',
    'enum'        : r'\yenum\y',
    'instanceof'  : r'\yinstanceof\y',
    'return'      : r'\yreturn\y',
    'transient'   : r'\ytransient\y',
    'catch'       : r'\ycatch\y',
    'extends'     : r'\yextends\y',
    'int'         : r'\yint\y',
    'short'       : r'\yshort\y',
    'try'         : r'\ytry\y',
    'char'        : r'\ychar\y',
    'final'       : r'\yfinal\y',
    'interface'   : r'\yinterface\y',
    'static'      : r'\ystatic\y',
    'void'        : r'\yvoid\y',
    'class'       : r'\yclass\y',
    'finally'     : r'\yfinally\y',
    'long'        : r'\ylong\y',
    'strictf'     : r'\ystrictf\y',
    'volatile'    : r'\yvolatile\y',
    'const'       : r'\yconst\y',
    'float'       : r'\yfloat\y',
    'native'      : r'\ynative\y',
    'super'       : r'\ysuper\y',
    'while'       : r'\ywhile\y',
}

TED_KEYWORDS = [
    'int', 'real', 'string', 'inc', 'dec', 'sqrt', 'pow', 'print',
    'sum', 'call', 'if', 'then', 'else', 'while', 'less', 'greater',
    'not', 'equal', 'is', 'than', 'or', 'and', 'to',
]
TED_KEYWORD_PATTERNS = {
    'int'     : r'\yint\y',
    'real'    : r'\yreal\y',
    'string'  : r'\ystring\y',
    'inc'     : r'\yinc\y',
    'dec'     : r'\ydec\y',
    'sqrt'    : r'\ysqrt\y',
    'pow'     : r'\ypow\y',
    'print'   : r'\yprint\y',
    'sum'     : r'\ysum\y',
    'call'    : r'\ycall\y',
    'if'      : r'\yif\y',
    'then'    : r'\ythen\y',
    'else'    : r'\yelse\y',
    'while'   : r'\ywhile\y',
    'less'    : r'\yless\y',
    'greater' : r'\ygreater\y',
    'not'     : r'\ynot\y',
    'equal'   : r'\yequal\y',
    'is'      : r'\yis\y',
    'than'    : r'\ythan\y',
    'or'      : r'\yor\y',
    'and'     : r'\yand\y',
    'to'      : r'\yto\y',
}

KEYWORDS = {JAVA: JAVA_KEYWORDS, TED: TED_KEYWORDS}
KEYWORDS_PATTERNS = {JAVA: JAVA_KEYWORD_PATTERNS, TED: TED_KEYWORD_PATTERNS}


class FileInfo:

    def __init__(self, path, name, extension, saved=False, temp=False):
        self._path = path
        self._name = name
        self._extension = extension

        self.absolute_path = os.path.join(self._path, self._name + self._extension)
        self.saved = saved
        self.temp  = temp

    @classmethod
    def from_absolute_path(cls, absolute_path, saved=True):
        temp = absolute_path.split(os.sep)
        name, extension = os.path.splitext(temp.pop())
        path = os.sep.join(temp)

        return FileInfo(path, name, extension, saved)

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self._name

    @property
    def extension(self):
        return self._extension

    @extension.setter
    def extension(self, value):
        self._extension = value
        self.absolute_path = os.path.join(self._path, self._name + self._extension)


def new_file(event=None):
    global current_file

    current_file = temporary_file
    root.title('You have opened a new document which does not have a name yet')

    text.delete(0.0, END)

    output.config(state=NORMAL)
    output.delete(0.0, END)
    output.config(state=DISABLED)


def save_file(event=None):
    global current_file

    if current_file is temporary_file or current_file.saved:
        source = text.get(0.0, END).encode('utf-8')
        with open(current_file.absolute_path, 'w', encoding='utf-8') as text_file:
            text_file.write(source)
    else:
        save_as()


def save_as(event=None):
    global current_file

    file = asksaveasfile(mode='w', initialdir=SOURCE_DIRECTORY)
    if file is None:
        return

    source = text.get(0.0, END).encode('utf-8')
    try:
        file.write(source.strip())
    except IOError:
        print('BALAagsd')

    current_file = FileInfo.from_absolute_path(file.name)
    root.title(current_file.name)


def open_file(event=None):
    global current_file, text

    file = askopenfile(mode='r', initialdir=SOURCE_DIRECTORY)
    if file is None:
        return

    current_file = FileInfo.from_absolute_path(file.name)
    root.title(current_file.name)

    source = file.read()
    text.delete(0.0, END)
    text.insert(0.0, source)

    output.config(state=NORMAL)
    output.delete(0.0, END)
    output.config(state=DISABLED)

    remove_all_highlight()
    highlight_all()


def run_as_java_file(event=None):
    save_file()

    arguments = [
        # Compiler.
        'javac',

        # Options.
        '-d', BYTE_DIRECTORY,  # -d <directory> - class files
        '-s', BYTE_DIRECTORY,  # -s <directory> - source files
        '-h', BYTE_DIRECTORY,  # -h <directory> - native header files

        # Source files.
        current_file.absolute_path
    ]

    compile_status = subprocess.run(args=arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error = compile_status.stderr.decode('utf-8')

    if error:
        output.config(state=NORMAL)
        output.delete(0.0, END)
        output.insert(0.0, error)
        output.tag_add('error', '1.0', 'end')
        output.config(state=DISABLED)
        return


    arguments = [
        # Compiler.
        'java',

        # Options.
         '-classpath', BYTE_DIRECTORY,  # -cp <path> - search path of directories and zip/jar files

        # Source files.
        current_file.name
    ]

    result = subprocess.run(args=arguments, stdout=subprocess.PIPE)
    output.config(state=NORMAL)
    output.delete(0.0, END)
    output.insert(0.0, result.stdout.decode('utf-8'))
    output.config(state=DISABLED)


def run_as_ted_file(event=None):

    save_file()

    arguments = [
        'python3.5',
        TED_INTERPRETER,
        current_file.absolute_path
    ]
    result = subprocess.run(args=arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    error = result.stderr.decode('utf-8')
    if error:
        output.config(state=NORMAL)
        output.delete(0.0, END)
        output.insert(0.0, error)
        output.config(state=DISABLED)
    else:
        output.config(state=NORMAL)
        output.delete(0.0, END)
        output.insert(0.0, result.stdout.decode('utf-8'))
        output.config(state=DISABLED)


def run(event=None):
    if COMPILER == JAVA:
        run_as_java_file()
    elif COMPILER == TED:
        run_as_ted_file()


def switch_compiler(event=None):
    global COMPILER

    filemenu.entryconfigure(5, label='Switch compiler to {}'.format(COMPILER))

    if COMPILER == JAVA:
        COMPILER = TED
    elif COMPILER == TED:
        COMPILER = JAVA

    remove_all_highlight()
    highlight_all()


def search_and_apply_tag(pattern, tag, start='1.0', end='end'):
    while True:
        count = StringVar()
        index = text.search(pattern, start, stopindex=end, count=count, regexp=True)

        if index:
            stop = '{} + {} chars'.format(index, count.get())
            text.tag_add(tag, index, stop)
            start = stop
        else:
            break

def highlight(event=None):
    char_index = 'insert - 1 char', 'insert'
    word_index = 'insert - 1 char wordstart', 'insert wordend - 1 char'
    line_index = 'insert linestart', 'insert lineend'

    char = text.get(*char_index)
    word = text.get(*word_index).replace('\n', '')
    line = text.get(*line_index)

    # print('char = {!r}, word = {!r}, line = {!r}'.format(char, word, line))

    comment_pattern = r'//.*\n'
    search_and_apply_tag(comment_pattern, 'comment', *line_index)

    string_pattern = r'".*?"'
    search_and_apply_tag(string_pattern, 'string', *line_index)

    if word in KEYWORDS[COMPILER]:
        patterns = KEYWORDS_PATTERNS[COMPILER]
        word_pattern = patterns[word]
        search_and_apply_tag(word_pattern, 'keyword', *word_index)

    number_pattern = r'\y[0-9]+((\.)?[0-9]*)?\y'
    search_and_apply_tag(number_pattern, 'number', *word_index)


def remove_highlight(event=None):
    char_index = 'insert - 1 char', 'insert'
    word_index = 'insert - 1 char wordstart', 'insert wordend - 1 char'
    line_index = 'insert linestart', 'insert lineend'

    char = text.get(*char_index)
    word = text.get(*word_index).replace('\n', '')
    line = text.get(*line_index)

    # print('char = {!r}, word = {!r}, line = {!r}'.format(char, word, line))

    if word not in KEYWORDS[COMPILER]:
        text.tag_remove('keyword', *word_index)
    for arguments in (('number', *word_index), ('comment', *word_index), ('string', *line_index)):
        try:
            text.tag_remove(*arguments)
        except TclError:
            pass


def highlight_all(event=None):
    index = '1.0', 'end'

    number_pattern = r'\y[0-9]+((\.)?[0-9]*)?\y'
    search_and_apply_tag(number_pattern, 'number', *index)

    string_pattern = r'".*?"'
    search_and_apply_tag(string_pattern, 'string', *index)

    comment_pattern = r'//.*\n'
    search_and_apply_tag(comment_pattern, 'comment', *index)

    patterns = KEYWORDS_PATTERNS[COMPILER]
    for word in KEYWORDS[COMPILER]:
        word_pattern = patterns[word]
        search_and_apply_tag(word_pattern, 'keyword', *index)


def remove_all_highlight(event=None):
    for tag in text.tag_names():
        text.tag_remove(tag, '1.0', 'end')


temporary_file = FileInfo(SOURCE_DIRECTORY, 'temp', '.txt')
current_file = temporary_file


root = Tk()
root.title('You have opened a new document which does not have a name yet')
# root.minsize(width=WIDTH, height=HEIGHT)
# root.maxsize(width=WIDTH, height=HEIGHT)


# TEXT AREA START
text_area = Frame(root)
text_area.grid_rowconfigure(0, weight=1)
text_area.grid_columnconfigure(0, weight=1)

scrollbar_x = Scrollbar(text_area, orient=HORIZONTAL)
scrollbar_x.grid(row=1, column=0, sticky=E + W)
scrollbar_y = Scrollbar(text_area)
scrollbar_y.grid(row=0, column=1, sticky=N + S)

text = Text(text_area, wrap=NONE, bd=0, xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
text.grid(row=0, column=0, sticky=N+S+E+W)

scrollbar_x.config(command=text.xview)
scrollbar_y.config(command=text.yview)

text_area.pack(side=TOP)
# TEXT AREA END


# https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter
text.tag_configure('keyword', foreground='dark orange')
text.tag_configure('string',  foreground='dark green')
text.tag_configure('number',  foreground='dark blue')
text.tag_configure('comment', foreground='dark grey')


# Causes error when bound to root:
# https://stackoverflow.com/questions/6378556/multiple-key-event-bindings-in-tkinter-control-e-command-apple-e-etc/6379851#6379851
text.bind('<Command-o>', open_file)
text.bind('<Command-n>', new_file)
text.bind('<Command-s>', save_file)
text.bind('<Command-r>', run)

text.bind('<KeyRelease>',           highlight)
text.bind('<KeyRelease-BackSpace>', remove_highlight)


# OUTPUT AREA START
output_area = Frame(root)
output_area.grid_rowconfigure(0, weight=1)
output_area.grid_columnconfigure(0, weight=1)

scrollbar_x = Scrollbar(output_area, orient=HORIZONTAL)
scrollbar_x.grid(row=1, column=0, sticky=E + W)
scrollbar_y = Scrollbar(output_area)
scrollbar_y.grid(row=0, column=1, sticky=N + S)

output = Text(output_area, wrap=NONE, bd=0, xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set, state=DISABLED)
output.grid(row=0, column=0, sticky=N+S+E+W)

scrollbar_x.config(command=text.xview)
scrollbar_y.config(command=text.yview)

output_area.pack(side=BOTTOM)
# OUTPUT AREA END


output.tag_configure('error', foreground='red')


menubar = Menu(root)
filemenu = Menu(menubar)
filemenu.add_command(label='Create a new file where you can write text and stuff into', command=new_file, accelerator='command-n')
filemenu.add_command(label='Save the current file so you do not lose it when you exit', command=save_file, accelerator='command-s')
filemenu.add_command(label='Save the current file with a new name so you can find it later', command=save_as)
filemenu.add_command(label='Open a file by looking in your computer for it', command=open_file, accelerator='command-o')
filemenu.add_separator()
filemenu.add_command(label='Switch compiler to JAVA', command=switch_compiler)
filemenu.add_separator()
filemenu.add_command(label='Run', command=run, accelerator='command-r')
filemenu.add_command(label='Run this file with the java compiler', command=run_as_java_file)
filemenu.add_command(label='Run this file with the TED compiler', command=run_as_ted_file)
filemenu.add_separator()
filemenu.add_command(label='Quit this application so it will not run anymore', command=root.quit, accelerator='command-q')
menubar.add_cascade(label='Confusing header where options are', menu=filemenu)

root.config(menu=menubar)



root.mainloop()
