import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pygubu.widgets.scrollbarhelper import ScrollbarHelper
# from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import csv
import math
from tkinter import messagebox



class DataPlotFrame(tk.Frame):
    COLORS = ['orange','wheat', 'springgreen', 'tomato', 'cornflowerblue', 'orchid']
    def __init__(self, x, ys, xname, ynames, title, parent, face_color = (.2,.2,.2), markersize = 3, text_color = 'white',*args, **kwargs):
        tk.Frame.__init__(self, *args,**kwargs)
        self.parent = parent
        self.markersize_val = markersize
        self.fig = plt.figure(figsize = (8,4), facecolor = face_color)
        plt.rcParams['savefig.facecolor'] = face_color
        self.canvas = FigureCanvasTkAgg(self.fig, master=self) # A tk.DrawingArea.
        self.ax = self.fig.add_subplot(111)
        # self.fig.subplots_adjust(left = 0.1 + 0.022*len(ynames), right=0.95)

        #locator and formatter for dates
        locator = mdates.AutoDateLocator(minticks=3, maxticks=14)
        formatter = mdates.ConciseDateFormatter(locator)

        if type(x[0]) == datetime.datetime:
            xdate = True
            self.ax.xaxis.set_major_locator(locator)
            self.ax.xaxis.set_major_formatter(formatter)
        else:
            xdate = False

        self.ax.set_title(title, color = text_color)
        if len(ynames) == 1:
            if type(ys[0]) == datetime.datetime:
                ydate = True
                self.ax.yaxis.set_major_locator(locator)
                self.ax.yaxis.set_major_formatter(formatter)
            else:
                ydate = False
            self.ax.plot_date(x, ys[0] , '-', marker = 'o', markersize = self.markersize_val, ydate = ydate, xdate = xdate, color = 'orange')
            self.ax.set_ylabel(ynames[0])
            self.ax.set_xlabel(xname)
        else:
            ylabel = ''
            magnitudes = []
            for y in ys:
                if type(y[0]) == datetime.datetime:
                    self.parent.error_message('Error', 'Y Data cant be of type "datetime" when plotting multiple entries.')
                    return
                max_value = max(y, key= abs)
                order = int(math.log(abs(max_value), 10))
                magnitudes.append(order)
            max_mag = max(magnitudes, key = abs)
            mag_diffs = []
            for mag in magnitudes:
                mag_diffs.append(max_mag - mag)
            for y, yname, counter, magdiff in zip(ys,ynames, range(0,len(ynames)), mag_diffs):
                if magdiff <= 1:
                    self.ax.plot_date(x, y, '-', marker = 'o', markersize = self.markersize_val, ydate = False, xdate = xdate, color = self.COLORS[counter%len(self.COLORS)], label = yname)
                    ylabel = ylabel + '\n' + yname
                else:
                    y = [val*10**magdiff for val in y]
                    self.ax.plot_date(x, y, '-', marker = 'o', markersize = self.markersize_val, ydate = False, xdate = xdate, color = self.COLORS[counter%len(self.COLORS)], label = yname + '*1e' + str(magdiff))
                    ylabel = ylabel + '\n' + yname + '*1e' + str(magdiff)
            # self.ax.set_ylabel(ylabel)
            self.ax.set_xlabel(xname)
            leg = self.ax.legend()
            frame = leg.get_frame()
            frame.set_facecolor('black')
            for text in leg.get_texts():
                text.set_color("oldlace")
        self.fig.tight_layout()
        self.ax.set_facecolor(face_color)
        for k, v in self.ax.spines.items():
            self.ax.spines[k].set_color(text_color)
        self.ax.tick_params(axis='x', colors=text_color)
        self.ax.tick_params(axis='y', colors=text_color)
        self.ax.xaxis.label.set_color(text_color)
        self.ax.yaxis.label.set_color(text_color)
        self.ax.grid(linestyle = ':', alpha = 0.5, color = text_color)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH,expand=True)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.toolbar.pack()
        self.canvas.draw()


class DataExplorerGUI(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args,**kwargs)
        #attributes like data:
        self.data = []
        self.header = None
        self.tabs = []
        self.master = master
        self.current_filename = ''
        self.data_dict = {}
        #PYGUBU AUTO CODE START
        self.main_frame = ttk.Frame(master)
        self.left_frame = ttk.Frame(self.main_frame)
        self.listbox_frame = ttk.Frame(self.left_frame)
        self.x_labelframe = ttk.Labelframe(self.listbox_frame)
        self.scrollbarhelper_2 = ScrollbarHelper(self.x_labelframe, scrolltype='vertical')
        self.x_listbox = tk.Listbox(self.scrollbarhelper_2.container)
        self.x_listbox.config(background='#4e4e4e', exportselection='false', foreground='#e2e2e2', width='30')
        self.x_listbox.pack(expand='true', fill='both', side='top')
        self.scrollbarhelper_2.add_child(self.x_listbox)
        # TODO - self.scrollbarhelper_2: code for custom option 'usemousewheel' not implemented.
        self.scrollbarhelper_2.pack(expand='true', fill='both', side='top')
        self.x_labelframe.config(height='200', text='x data', width='200')
        self.x_labelframe.pack(expand='true', fill='both', side='left')
        self.y_labelframe = ttk.Labelframe(self.listbox_frame)
        self.scrollbarhelper_3 = ScrollbarHelper(self.y_labelframe, scrolltype='vertical')
        self.y_listbox = tk.Listbox(self.scrollbarhelper_3.container)
        self.y_listbox.config(background='#4e4e4e', exportselection='false', foreground='#e2e2e2', selectmode='multiple')
        self.y_listbox.config(width='30')
        self.y_listbox.pack(expand='true', fill='both', side='top')
        self.scrollbarhelper_3.add_child(self.y_listbox)
        # TODO - self.scrollbarhelper_3: code for custom option 'usemousewheel' not implemented.
        self.scrollbarhelper_3.pack(expand='true', fill='both', side='top')
        self.y_labelframe.config(height='200', text='y data', width='200')
        self.y_labelframe.pack(expand='true', fill='both', side='right')
        self.listbox_frame.config(height='200', width='200')
        self.listbox_frame.pack(expand='true', fill='both', side='top')
        self.button_frame = ttk.Frame(self.left_frame)
        self.load_csv_button = ttk.Button(self.button_frame)
        self.load_csv_button.config(text='load csv')
        self.load_csv_button.pack(expand='true', fill='both', side='bottom')
        self.load_csv_button.configure(command=self.loadCSV)
        self.add_plot_tab_button = ttk.Button(self.button_frame)
        self.add_plot_tab_button.config(text='add plot as tab')
        self.add_plot_tab_button.pack(expand='true', fill='both', side='bottom')
        self.add_plot_tab_button.configure(command=self.addPlotTab)
        self.remove_plot_tab_button = ttk.Button(self.button_frame)
        self.remove_plot_tab_button.config(text='remove selected tab')
        self.remove_plot_tab_button.pack(expand='true', fill='both', side='bottom')
        self.remove_plot_tab_button.configure(command=self.removePlotTab)
        self.search_labelframe = ttk.Labelframe(self.button_frame)
        self.search_entry = ttk.Entry(self.search_labelframe)
        search_text_var = tk.StringVar()
        self.search_entry.config(cursor='arrow', exportselection='false', takefocus=False, textvariable=search_text_var)
        self.search_entry.pack(expand='true', fill='x', side='top')
        self.search_labelframe.config(height='200', text='search', width='200')
        self.search_labelframe.pack(anchor='n', expand='true', fill='x', side='left')
        self.button_frame.config(height='200', width='200')
        self.button_frame.pack(expand='true', fill='both', side='top')
        self.left_frame.config(height='200', width='200')
        self.left_frame.pack(expand='true', fill='both', side='left')
        self.right_frame = ttk.Frame(self.main_frame)
        self.plot_notebook = ttk.Notebook(self.right_frame)
        self.plot_notebook.config(height='500', width='800')
        self.plot_notebook.pack(anchor='w', expand='true', fill='both', side='right')
        self.right_frame.config(height='400', width='700')
        self.right_frame.pack(anchor='w', expand='true', fill='both', side='left')
        self.main_frame.config(height='200', width='200')
        self.main_frame.pack(expand='true', fill='both', side='top')
        ###PYGUBU AUTO CODE END
        self.search_text_var = search_text_var
        self.search_text_var.trace("w", lambda name, index, mode: self.update_listbox())
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        plt.close("all")
        self.master.destroy()

    def update_listbox(self):
        '''update listbox according to search term'''
        search_term = self.search_text_var.get()
        selected_items_x, selected_items_y = self.get_selected()
        print(selected_items_x)
        self.x_listbox.delete(0,tk.END)
        self.y_listbox.delete(0,tk.END)
        #search x listbox:
        for name in self.header:
            if search_term.lower() in name.lower() and not (search_term.lower() in selected_items_x):
                self.x_listbox.insert(tk.END,name)
        for item in selected_items_x:
            self.x_listbox.insert(0,item)
            self.x_listbox.selection_set(0)
        #search y listbox:
        for name in self.header:
            if search_term.lower() in name.lower() and not (search_term.lower() in selected_items_y):
                self.y_listbox.insert(tk.END,name)
        for item in selected_items_y:
            self.y_listbox.insert(0,item)
            self.y_listbox.selection_set(0)
        return True

    def get_selected(self):
        '''get selected items from listbox'''
        user_choice_x = []
        user_choice_y = []
        index_list_x = list(self.x_listbox.curselection())
        index_list_y = list(self.y_listbox.curselection())
        for i in index_list_x:
            user_choice_x.append(self.x_listbox.get(i))
        for i in index_list_y:
            user_choice_y.append(self.y_listbox.get(i))
        return user_choice_x, user_choice_y

    def loadCSV(self):
        dir = filedialog.askopenfilename(filetypes = [("Comma Separated Values","*.csv")])
        if dir == '':
            return
        if not dir:
            return
        self.current_filename = dir.split('/')[-1]
        self.data_dict = {}
        with open(dir, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter = ';', quotechar = '"')
            self.header = next(csvreader)

            self.data = []
            #init an empty list for each header name
            for i in range(0,len(self.header)):
                self.data.append([])

            #collect data for each header
            for row in csvreader:
                for i in range(0,len(self.header)):
                    value = row[i].replace(',','.')
                    if value == '':
                        value = 0
                    try:
                        value = float(value)
                    except:
                        #its a date, convert to datetime
                        #format: 2020-11-28 12:38:02"
                        value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                    self.data[i].append(value)
        for name, num in zip(self.header, range(0,len(self.header))):
            self.data_dict[name] = num
        self.x_listbox.delete(0,tk.END)
        self.y_listbox.delete(0,tk.END)
        self.x_listbox.insert(0, *self.header)
        self.y_listbox.insert(0, *self.header)

    def addPlotTab(self):
        x_selection = self.x_listbox.curselection()
        y_selection = self.y_listbox.curselection()
        if x_selection == ():
            return
        if y_selection == ():
            return
        x_selection = x_selection[0]
        xname = self.x_listbox.get(x_selection)
        x_selection = self.data_dict[xname]
        x = self.data[x_selection]
        ynames = []
        ys = []
        for sel in y_selection:
            yname = self.y_listbox.get(sel)
            ynames.append(yname)
            sel = self.data_dict[yname]
            ys.append(self.data[sel])
        if len(ynames) == 1:
            self.plot_notebook.add(DataPlotFrame(x,ys, xname, ynames, 'Data from ' + self.current_filename, self), text = ynames[0] +' over ' + xname)
        else:
            self.plot_notebook.add(DataPlotFrame(x,ys, xname, ynames, 'Data from ' + self.current_filename, self), text = 'multiple entries over ' + xname)
        last_tab = len(self.plot_notebook.tabs())-1
        self.plot_notebook.select(last_tab)

    def removePlotTab(self):
        index = self.plot_notebook.select()
        self.plot_notebook.forget(index)

    def error_message(self,title,message):
        '''generates an error message-popup with generic title and message'''
        messagebox.showerror(title,message)

if __name__ == '__main__':
    root = tk.Tk(className="data explorer RFPB2 WS20")
    # style = ttk.Style()
    #
    # style.theme_create( "darkmode", parent="alt", settings={
    #         "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
    #         "TNotebook.Tab": {
    #             "configure": {"padding": [5, 1], "background": '#000000' },
    #             "map":       {"background": [("selected", '#414141')],
    #                           "expand": [("selected", [1, 1, 1, 0])] } } } )
    #
    # style.theme_use("darkmode")
    root.tk.call('lappend', 'auto_path', './theme/awthemes')
    root.tk.call('package', 'require', 'awdark')
    style = ttk.Style()
    style.theme_use("awdark")
    gui = DataExplorerGUI(master=root)
    gui.pack(expand=True, fill='both')
    root.mainloop()
