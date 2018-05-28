import tkinter as tk
from tkinter import filedialog
import os, json, sys
from num2words import num2words

window = tk.Tk()
window.geometry('500x800+500+500')
window.title('QuizCreator')
window.resizable(False, False)
window.configure(background = 'olive drab')

windowTitle = ''
widgetPositions = [20, 20]
YforAdd = 20
itera = 0
iter2 = 1
Questions = [] # stores a list of button objects
Questions_Two = [] # used to dynamically create variables, which will correspond to another button
Question_List = {}
data = {}
load_data = ''
correct_ans_int = 0

# I.E. "One" in Questions_Two is a variable and corresponds to "One" in Questions

path = path = os.path.dirname(os.path.abspath(__file__))

# Creates and Manages Widget Questions
class Widget():

    def __init__(self, name, Q):
        self.name = name
        self.questions = Q
        self.questions.append(name)

    def initialize(self, index):
        self.indexNum = index
        self.questions[self.indexNum] = tk.Button(window, text = '', command = lambda: self.reRoute(self.indexNum))
        self.questions[self.indexNum].place(x = widgetPositions[0], y = widgetPositions[1])
        self.questions[self.indexNum].config(width = 54)

        def destroy(event, var):
            global Question_List
            Question_List[self.indexNum + 1] = var.get()
            self.questions[self.indexNum].config(text = var.get().title())
            var.destroy()
            print(Question_List)

        temp = tk.Entry(window)
        temp.place(x = widgetPositions[0] + 50, y = widgetPositions[1] + 4)
        temp.bind('<Return>', lambda event, var = temp: destroy(event, temp))
        
    def reRoute(self, index):
        self.editWidget(index)

    def editWidget(self, index):  

        def on_closing():
            temporary = 'Question_' + str(self.indexNum + 1)
            data[temporary] = []
            data[temporary].append({
                'Answer_One' : Q1.get(),
                'Answer_Two' : Q2.get(),
                'Answer_Three' : Q3.get(),
                'Answer_Four' : Q4.get(),
                'Correct' : str(correct_ans_int),
            })    
            with open(path + '/' + windowTitle + '.json', 'w') as outfile:
                json.dump(data, outfile, indent = 2)
            edit.destroy()

        def modify(number, button):
            global correct_ans_int
            if button['background'] == 'green':
                button.config(background = AddWidget.cget('bg'))
            else:
                button.config(background = 'green', activebackground = 'green')
                correct_ans_int = number

        def on_open():
            newname = 'Question_' + str(self.indexNum + 1)
            if os.stat(path + '/' + windowTitle + '.json').st_size > 0:
                with open(path + '/' + windowTitle + '.json', 'r') as handle:
                    load_data = json.load(handle)
                    if newname in load_data:
                        for parse in load_data[newname]:
                            V1.set(parse['Answer_One'])
                            V2.set(parse['Answer_Two'])
                            V3.set(parse['Answer_Three'])
                            V4.set(parse['Answer_Four'])
                            modify(parse['Correct'], button_data[int(parse['Correct'])])
                    else:
                        pass
            else:
                pass

        edit = tk.Toplevel()
        edit.geometry('400x300')
        edit.title('Edit Question # ' + str(self.indexNum + 1))
        edit.resizable(False, False)
        edit.configure(background = 'chocolate')
        edit.protocol("WM_DELETE_WINDOW", on_closing)

        question_title = tk.Label(edit, text = Question_List[self.indexNum + 1].title(), relief = 'sunken', width = 50)
        instructions = tk.Label(edit, background = 'dark slate gray', text = 'Once all answers have been added, select \na correct answer with the check marks beside them.', relief = 'groove', width = 50)
        V1 = tk.StringVar()
        V2 = tk.StringVar()
        V3 = tk.StringVar()
        V4 = tk.StringVar()
        Q1 = tk.Entry(edit, width = 10, textvariable = V1)
        Q2 = tk.Entry(edit, width = 10, textvariable = V2)
        Q3 = tk.Entry(edit, width = 10, textvariable = V3)
        Q4 = tk.Entry(edit, width = 10, textvariable = V4)
        A1 = tk.Button(edit, text = u'\u2713', width = 1, command = lambda: modify(1, A1))
        A2 = tk.Button(edit, text = u'\u2713', width = 1, command = lambda: modify(2, A2))
        A3 = tk.Button(edit, text = u'\u2713', width = 1, command = lambda: modify(3, A3))
        A4 = tk.Button(edit, text = u'\u2713', width = 1, command = lambda: modify(4, A4))

        question_title.place(relx=0.5, anchor = 'n')
        instructions.place(x = 0, y = 40)
        Q1.place(x = 110, y = 100)
        Q2.place(x = 210, y = 100)
        Q3.place(x = 110, y = 130)
        Q4.place(x = 210, y = 130)
        A1.place(x = 70, y = 97)
        A2.place(x = 300, y = 97)
        A3.place(x = 70, y = 127)
        A4.place(x = 300, y = 127)

        button_data = {
            1 : A1,
            2 : A2,
            3 : A3,
            4 : A4
        }

        on_open()

# Initialize Class 
def W_init(name):
    global widgetPositions, itera
    name.initialize(itera)
    widgetPositions[1] += 30
    itera += 1
# Create Question Widgets
def create_widget():
    global Questions_Two, AddWidget, YforAdd, iter2
    dynamicName = num2words(iter2).title()
    Questions_Two.append(dynamicName)
    Questions_Two[itera] = Widget(dynamicName, Questions)
    W_init(Questions_Two[itera])
    YforAdd += 30
    iter2 += 1
    AddWidget.place_configure(y = YforAdd)
#When Done...
def finish_edits():
    pass
#Import Files
def import_file():
    global windowTitle, new
    name = filedialog.askopenfilename(initialdir = path, title = 'Select File', filetypes = (("text files","*.json"),("all files","*.*")))
    with open(name, 'r+') as newfile:
        newdata = json.load(newfile)
        windowTitle = newdata['NameOfFile'][0]
        #find way to create widget for Qs in JSON, and modify contents of widgets
    window.title('QuizCreator - ' + windowTitle)
    new.destroy()



#Create New File
def newfilecreation(item, item_2, root):
    item.destroy()
    item_2.destroy()

    def finish(entry):
        global windowTitle, window, data
        windowTitle = entry.get().title()
        window.title('QuizCreator - ' + windowTitle)
        os.mknod(path + '/' + windowTitle + '.json')
        with open(path + '/' + windowTitle + '.json', 'w') as name:
            data['NameOfFile'] = [windowTitle]
            json.dump(data, name)
        labelEntry.destroy()
        done.destroy()
        root.destroy()

    nameofFile = tk.Entry(root)
    nameofFile.place(relx = 0.5, rely = 0.5, anchor = 'center')
    labelEntry = tk.Label(root, text = 'Name of Quiz', relief = 'raised')
    labelEntry.place(x = 155, y = 100)
    done = tk.Button(root, text = 'Done', command = lambda: finish(nameofFile))
    done.place(x = 170, y = 170)


#Buttons on Main
AddWidget = tk.Button(window, text = u"\u2795", highlightbackground = 'sienna', command = create_widget)
Present = tk.Button(window, text = 'Finish', command = finish_edits)

AddWidget.place(x = 232, y = YforAdd)
Present.place(x = 232, y = 770)


#Import or Continue? First Window
new = tk.Toplevel()
new.geometry('400x300+500+500')
new.resizable(False, False)
new.configure(background = 'sienna4')
new.attributes("-topmost", True)

Import = tk.Button(new, text = 'Import File', command = import_file)
Newfile = tk.Button(new, text = 'New File',  command = lambda: newfilecreation(Newfile, Import, new))
Import.place(x = 100, y = 100)
Newfile.place(x = 200, y = 100)
window.mainloop()