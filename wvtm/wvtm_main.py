import tkinter as tk
from tkinter import filedialog
from datetime import date, datetime
import os
from tkinter.simpledialog import askinteger, askstring


color_1 = 'green'   #primary
color_2 = 'white'   #secondary
color_text = 'white'   #text
color_white = 'white'
color_text_1 = 'black'

promt_videos_dir = 'assets/videos/'


class main_window:

    def __init__(self, master):
        self.master = master
        self.master.title("WVTM Tool")
        self.master.iconphoto(False, tk.PhotoImage(file="assets/wvtm_tool.png"))
        self.master.resizable(True, True)
        self.master.config(bg="#fff")

        self.master.protocol("WM_DELETE_WINDOW", self.closeWindow)

        main_menu = tk.Menu(self.master)
        self.master.configure(menu=main_menu)
        main_menu.add_command(label="About", command=self.About)

        
        self.viewer = tk.Toplevel()
        self.viewer.title("Word Viewer")
        self.viewer.iconphoto(False, tk.PhotoImage(file="assets/word_viewer.png"))
        self.viewer.resizable(True, True)
        self.viewer.config(bg="#fff")
        self.viewer.geometry("1280x720")
        self.viewer.bind('<Configure>', self.resize)

        #--------------variables----------------
        self.words_list = []
        self.start_time = 0
        self.start_time_set = False
        self.discard_flag = False
        self.repeat = 1
        self.repeat_counter = 1
        self.state_flag = 0 ##1-session start, 2-stop session, 3-start record, 4-stop record, 5-discard, 6-next
        self.index = 0
        self.out_file = None
        self.view_funcs = []
        self.settings_buttons = []
        self.state_buttons = {}
        self.color_lt_green = "#CAFFDD"

        #--------------output dir check----------------
        try:
            with open('values/out_dir.txt', 'r') as file:
                self.output_dir = file.readline()
        except:
            self.output_dir = os.path.dirname(os.path.realpath(__file__))

        #--------------words dir check----------------
        try:
            with open('values/words_dir.txt', 'r') as file:
                self.words_dir = file.readline()
        except:
            self.words_dir = ""

        #--------------frames----------------
        frame0 = tk.Frame(self.master, bg=color_white)
        frame0.pack(fill=tk.BOTH, side=tk.TOP)

        frame1 = tk.Frame(frame0)
        frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        frame17 = tk.Frame(frame1)
        frame17.pack(fill=tk.BOTH, side=tk.BOTTOM)

        frame16 = tk.Frame(frame1)
        frame16.pack(fill=tk.BOTH, side=tk.BOTTOM)

        frame15 = tk.Frame(frame1)
        frame15.pack(fill=tk.BOTH, side=tk.BOTTOM)

        frame14 = tk.Frame(frame1)
        frame14.pack(fill=tk.BOTH, side=tk.BOTTOM)

        frame13 = tk.Frame(frame1)
        frame13.pack(fill=tk.BOTH, side=tk.BOTTOM)

        frame12 = tk.Frame(frame1)
        frame12.pack(fill=tk.BOTH, side=tk.BOTTOM)

        frame11 = tk.Frame(frame1)
        frame11.pack(fill=tk.BOTH, side=tk.BOTTOM)



        frame2 = tk.Frame(frame0)
        frame2.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)

        frame22 = tk.Frame(frame2)
        frame22.pack(fill=tk.BOTH, side=tk.BOTTOM)

        frame21 = tk.Frame(frame2)
        frame21.pack(fill=tk.BOTH, side=tk.BOTTOM)



        status_bar = tk.Frame(self.master, bg=color_white)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)



        
        #--------------frame11----------------
        self.out_dir_btn = tk.Button(frame11, text="Output Directory", height=2, width=20, command=self.getOutDir)
        self.out_dir_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.file_loc = tk.Label(frame11, text=self.output_dir, bg=color_white)
        self.file_loc.pack(side=tk.LEFT, expand=True)
        
        #--------------frame12----------------
        self.words_dir_btn = tk.Button(frame12, text="Words Directory", height=2, width=20, command=self.getWordsDir)
        self.words_dir_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.words_file_loc = tk.Label(frame12, text=self.words_dir, bg=color_white)
        self.words_file_loc.pack(side=tk.LEFT, expand=True)
        
        #--------------frame13----------------
        self.repeat_btn = tk.Button(frame13, text="No. of repeat", height=2, width=20, command=self.setRepeat)
        self.repeat_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.repeat_label = tk.Label(frame13, text=self.repeat, bg=color_white)
        self.repeat_label.pack(side=tk.LEFT, expand=True)

        #--------------frame14----------------
        self.start_se = tk.Button(frame14, text="Start Session", height=5, width=80, bg=color_white, fg=color_text_1, command=self.startSession)
        self.start_se.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        #--------------frame15----------------
        self.start = tk.Button(frame15, text="Start", height=5, bg=color_white, fg=color_text_1, command=self.startRecord)
        self.start.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.stop = tk.Button(frame15, text="Stop", height=5, bg=color_white, fg=color_text_1, command=self.stopRecord)
        self.stop.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        #--------------frame16----------------
        self.discard_btn = tk.Button(frame16, text="Discard", height=5, bg=color_white, fg=color_text_1, command=self.discard)
        self.discard_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.next_btn = tk.Button(frame16, text="Next", height=5, bg=color_white, fg=color_text_1, command=self.next)
        self.next_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        #--------------frame17----------------
        self.stop_se = tk.Button(frame17, text="Stop Session", height=5, width=80, bg=color_white, fg=color_text_1, command=self.stopSession)
        self.stop_se.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)



        #--------------frame21----------------
        self.set_index_btn = tk.Button(frame21, text="Set Word", height=3, bg=color_white, fg=color_text_1, command=self.setWInfo)
        self.set_index_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.word_info = tk.Label(frame21, bg=color_white, fg=color_text_1)
        self.word_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        #--------------frame22----------------
        self.prv_label = tk.Label(frame22, height=5, width=20, bg=color_white, fg=color_text)
        self.prv_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=80, pady=40)

        self.curr_label_counter = tk.Label(frame22, height=2, width=60, bg=color_white, fg=color_text_1)
        self.curr_label_counter.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10)

        self.curr_label = tk.Label(frame22, height=10, width=60, bg=color_1, fg=color_text)
        self.curr_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.next_label = tk.Label(frame22, height=5, width=20, bg=color_white, fg=color_text)
        self.next_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=80, pady=40)



        #--------------status_bar----------------
        date_lbl = tk.Label(status_bar, text='', bg=color_text, fg=color_white)
        date_lbl.pack(side=tk.LEFT, expand=True)

        time_lbl = tk.Label(status_bar, text='', bg=color_text, fg=color_white)
        time_lbl.pack(side=tk.LEFT, expand=True)

        
        #######################Viewer Window######################
        viewer_frame1 = tk.Frame(self.viewer, bg=color_1)
        viewer_frame1.pack(fill=tk.Y, side=tk.LEFT, expand=False)

        viewer_frame2 = tk.Frame(self.viewer)
        viewer_frame2.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)

        self.video_playback_label = tk.Label(viewer_frame1, bg=color_1)
        self.video_playback_label.pack(fill=tk.Y, expand=True)

        self.word_lbl = tk.Label(viewer_frame2, text='word', bg=color_1, fg=color_text, font=("Helvetica", 50))
        self.word_lbl.pack(fill=tk.BOTH, expand=True)

        self.countdown_label = tk.Label(viewer_frame2, text='', bg=color_1, fg=color_text, font=("Helvetica", 40))
        self.countdown_label.pack(fill=tk.BOTH, expand=True)

        #get time and refresh
        def tick():
            today = datetime.today()
            now = datetime.now()
            # get the current local time from the PC
            local_time = now.strftime('%H:%M:%S')
            local_date = today.strftime("%B %d, %Y")
            date_lbl.config(text=local_date)
            time_lbl.config(text=local_time)
            self.filename = today.strftime("%Y_%m_%d_") + now.strftime('%H_%M_%S')
            self.timestamp = str(now)

            if self.start_time_set:
                if (datetime.now() - self.start_time).total_seconds() >= 1:
                    self.countdown_label.config(text='3')
                if (datetime.now() - self.start_time).total_seconds() >= 2:
                    self.countdown_label.config(text='2')
                if (datetime.now() - self.start_time).total_seconds() >= 3:
                    self.countdown_label.config(text='1')
                if (datetime.now() - self.start_time).total_seconds() >= 3.9:
                    self.countdown_label.config(text='0')
                    self.updateWV(bg=color_2, fg=color_text_1)
                if (datetime.now() - self.start_time).total_seconds() >= 4:
                    self.countdown_label.config(fg=color_2)
                    self.start_time_set = False

            if self.state_flag == 1: ##start session
                self.state_flag = 0
                for button in self.settings_buttons:
                    button["state"] = "disabled"
                self.state_buttons['start']["state"] = "normal"
                self.state_buttons['start'].config(bg=self.color_lt_green)
            elif self.state_flag == 2: ##stop session
                self.state_flag = 0
                for button in self.settings_buttons:
                    button["state"] = "normal"
                for button in self.state_buttons:
                    self.state_buttons[button]["state"] = "disabled"
                    self.state_buttons[button].config(bg=color_white)
            elif self.state_flag == 3: ##start record
                self.state_flag = 0
                self.state_buttons['start']["state"] = "disabled"
                self.state_buttons['start'].config(bg=color_white)
                self.state_buttons['stop']["state"] = "normal"
                self.state_buttons['stop'].config(bg=self.color_lt_green)
                self.state_buttons['discard']["state"] = "disabled"
                self.state_buttons['discard'].config(bg=color_white)
            elif self.state_flag == 4: ##stop record
                self.state_flag = 0
                self.state_buttons['stop']["state"] = "disabled"
                self.state_buttons['stop'].config(bg=color_white)
                self.state_buttons['next']["state"] = "normal"
                self.state_buttons['next'].config(bg=self.color_lt_green)
                self.state_buttons['discard']["state"] = "normal"
                self.state_buttons['discard'].config(bg=self.color_lt_green)
            elif self.state_flag == 5: ##discard previous recording
                self.state_flag = 0
                self.state_buttons['next']["state"] = "disabled"
                self.state_buttons['next'].config(bg=color_white)
                self.state_buttons['start']["state"] = "normal"
                self.state_buttons['start'].config(bg=self.color_lt_green)
            elif self.state_flag == 6: ##next word
                self.state_flag = 0
                self.state_buttons['discard']["state"] = "disabled"
                self.state_buttons['discard'].config(bg=color_white)
                self.state_buttons['next']["state"] = "disabled"
                self.state_buttons['next'].config(bg=color_white)
                self.state_buttons['start']["state"] = "normal"
                self.state_buttons['start'].config(bg=self.color_lt_green)

            # calls itself every 10 milliseconds
            # to update the time display as needed
            time_lbl.after(10, tick)

        tick()


        self.view_funcs.extend([self.updateMWV, self.updateViewWindow, self.updateWInfo])
        self.settings_buttons.extend([self.out_dir_btn, self.words_dir_btn, self.repeat_btn])
        self.state_buttons = {
            "start": self.start, 
            "stop": self.stop,
            "discard": self.discard_btn,
            "next": self.next_btn
        }

        for st_btn in self.state_buttons:
            self.state_buttons[st_btn]["state"] = "disabled"
        
        self.initWV()

        self.master.mainloop()

    #get and save output directory
    def getOutDir(self):
        self.output_dir = filedialog.askdirectory()
        with open('values/out_dir.txt', 'w') as file:
            file.writelines(self.output_dir)
        self.file_loc.config(text=self.output_dir)

    #get and save words directory
    def getWordsDir(self):
        file = filedialog.askopenfile(mode='r', filetypes=[('Words txt file', '*.txt')])
        if file == None:
            tk.messagebox.showerror('Error', 'Please select the words list text file')
            return 1
        self.words_dir = os.path.abspath(file.name)
        with open('values/words_dir.txt', 'w') as file:
            file.writelines(self.words_dir)
        self.words_file_loc.config(text=self.words_dir)
        self.initWV()
    
    #set index of the word
    def setWInfo(self):
        info = askstring('Set Word', 'Insert the index value or the word you want to start with')
        try:
            self.index = int(info) - 1
        except ValueError:
            try:
                self.index = self.words_list.index(info)
            except:
                tk.messagebox.showerror('Error', 'Could not find word')
        except:
            pass
        self.viewWord()
    
    #no. of repeat of a single word
    def setRepeat(self):
        repeat = askinteger('Repeat Count', 'Insert the no. of repeat of a single word')
        if repeat <= 0:
            tk.messagebox.showerror('Error', 'Count must be greater than 0')
        else:
            self.repeat = repeat
            self.repeat_label.config(text=str(self.repeat))
        self.viewWord()
    
    #start session
    def startSession(self):
        self.repeat_counter = 1
        try:
            self.out_file = open(self.output_dir+"/"+self.filename+ ".txt" , 'w')
        except Exception as e:
            print(e)
            tk.messagebox.showerror('Error', 'Output file access problem')
            return 1
        if self.initWV() == 1:
            tk.messagebox.showerror('Error', 'Words list not set')
            return 1
        self.updateWV(bg='blue', fg=color_white)
        try:
            self.out_file.writelines(self.timestamp+'->start_session/'+self.words_list[self.index]+'\n')
        except Exception as e:
            print(e)
            tk.messagebox.showerror('Error', 'Output file access problem')
        self.curr_label.after(1000, self.initWV)
        self.start_se.config(bg='blue', fg=color_white)
        self.start_se["state"] = "disabled"
        self.state_flag = 1
    
    #start recording
    def startRecord(self):
        self.countdown_label.config(text='4')
        self.start_time = datetime.now()
        self.start_time_set = True
        self.discard_flag = False
        try:
            self.out_file.writelines(self.timestamp+'->start_record/'+self.words_list[self.index]+'/['+str(self.repeat_counter)+'/'+str(self.repeat)+']'+'\n')
        except Exception as e:
            print(e)
            tk.messagebox.showerror('Error', 'Output file access problem')
            return 1
        self.state_flag = 3
    
    #stop recording
    def stopRecord(self):
        self.viewWord()
        self.countdown_label.config(text='')
        self.start_time_set = False
        try:
            self.out_file.writelines(self.timestamp+'->stop_record/'+self.words_list[self.index]+'/['+str(self.repeat_counter)+'/'+str(self.repeat)+']'+'\n')
        except Exception as e:
            print(e)
            tk.messagebox.showerror('Error', 'Output file access problem')
            return 1
        self.state_flag = 4

    #discard previous recording
    def discard(self):
        if self.discard_flag:
            self.index -= 1
            self.viewWord()
        self.discard_flag = True
        try:
            self.out_file.writelines(self.timestamp+'->discard_previous/'+self.words_list[self.index]+'/\n')
        except Exception as e:
            print(e)
            tk.messagebox.showerror('Error', 'Output file access problem')
            return 1
        self.state_flag = 5
    
    #next word
    def next(self):
        self.repeat_counter += 1
        if self.repeat_counter > self.repeat:
            self.repeat_counter = 1

            if len(self.words_list)-1 > self.index:
                self.index += 1
                self.viewWord()
            else:
                tk.messagebox.showinfo('Info', 'Reached end of the list')
        else:
            self.viewWord()
        try:
            self.out_file.writelines(self.timestamp+'->next_word/'+self.words_list[self.index]+'/\n')
        except Exception as e:
            print(e)
            tk.messagebox.showerror('Error', 'Output file access problem')
            return 1
        self.state_flag = 6
    
    #stop session
    def stopSession(self):
        self.repeat_counter = 1
        last_word = self.words_list[self.index]
        if len(self.words_list)-1 > self.index:
            self.index += 1
        self.updateWV(bg='black', fg=color_text)
        self.stop_se.after(1000, self.viewWord)
        try:
            self.out_file.writelines(self.timestamp+'->stop_session/'+last_word)
            self.out_file.close()
        except Exception as e:
            print(e)
            tk.messagebox.showerror('Error', 'Output file access problem')
        
        self.start_se.config(bg=color_white, fg=color_text_1)
        self.start_se["state"] = "normal"
        self.state_flag = 2
    
    #stop recording and release camera when closing window
    def closeWindow(self):
        try:
            self.out_file.close()
        except:
            pass
        self.master.destroy()

    def About(self):
            tk.messagebox.showinfo('Developers',"This application assists in sign language recording and annotation process\nDeveloped by\nSUVAJIT PATRA (CS PhD Student, RKMVERI, Belur)")

    #word viewer initiate
    def initWV(self):
        try:
            with open(self.words_dir, 'r') as file:
                self.words_list = file.readlines()
                self.words_list = [word.strip() for word in self.words_list]
        except:
            tk.messagebox.showerror('Error', 'File access error')

        if self.words_list == None:
            tk.messagebox.showerror('Error', 'Please select the words text file first')
            return 1
        elif len(self.words_list) == 0:
            tk.messagebox.showerror('Error', 'No words found')
            return 1
        
        self.viewWord()

    #view word
    def viewWord(self):
        if not self.index < 0 and not self.index > len(self.words_list) - 1:
            self.updateWV(text=self.words_list[self.index], bg=color_1)
        else:
            tk.messagebox.showerror('Error', 'Index out of bound')
            return
        
        self.curr_label_counter.config(text=str(self.repeat_counter))
        
        if self.index-1 >= 0:
            self.prv_label.config(text=self.words_list[self.index - 1], bg=color_1)
        else:
            self.prv_label.config(text='', bg=color_1)
        
        if self.repeat == 1 or self.repeat == self.repeat_counter:
            if self.index+1 <= len(self.words_list)-1:
                self.next_label.config(text=self.words_list[self.index + 1], bg=color_1)
            else:
                self.next_label.config(text='', bg=color_1)
        else:
            self.next_label.config(text=self.words_list[self.index], bg=color_1)
    

    #word viewer update
    def updateWV(self, text='', bg=color_1, fg=color_text):
        for i in self.view_funcs:
            if len(text) == 0:
                i(back=bg, front=fg)
            else:
                i(text, back=bg, front=fg)

    #update main WV
    def updateMWV(self, str='', back=color_1, front=color_text):
        if len(str) == 0:
            self.curr_label.config(bg=back, fg=front)
        else:
            self.curr_label.config(text=str, bg=back, fg=front)

    #update word info
    def updateWInfo(self, string='', back=color_1, front=color_text):
        if len(string) == 0:
            pass
        else:
            self.word_info.config(text=str(self.index+1)+'   '+string)



    
    #window size change callback
    def resize(self, window):
        if window.height > 1000 and window.width > 1800:
            self.word_lbl.config(font = ("Helvetica", 120))
            self.countdown_label.config(font = ("Helvetica", 200))
        
        if window.height < 750 and window.width < 1300:
            self.word_lbl.config(font = ("Helvetica", 40))
            self.word_lbl.config(font = ("Helvetica", 80))
    
    #update viewer
    def updateViewWindow(self, str='', back=color_1, front=color_text):
        if len(str) == 0:
            self.word_lbl.config(bg=back, fg=front)
            self.countdown_label.config(bg=back, fg=front)
            self.viewer.config(bg=back)
        else:
            self.word_lbl.config(text=str, bg=back, fg=front)
            self.countdown_label.config(bg=back, fg=front)
            self.viewer.config(bg=back)
        

if __name__ == '__main__':
    app = main_window(tk.Tk())