import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path


def resource_path(filename):
    """Return the path to a bundled asset in both source and PyInstaller builds."""
    return str(Path(__file__).resolve().with_name(filename))

APP_BG="#F5F8F7"
CARD="#FFFFFF"
TEXT="#203238"
MUTED="#718187"
TEAL="#48A9A1"
TEAL_DARK="#348D86"
AQUA="#DDF4F1"
BLUE="#5CA9E6"
LINE="#E5ECEB"

class HydroBuddy:
    def __init__(self, root):
        self.root=root
        self.root.title("Hydro Buddy")
        self.root.geometry("410x575")
        self.root.resizable(False,False)
        self.root.configure(bg=APP_BG)

        self.running=False
        self.test_mode=False
        self.remaining=30*60

        self.interval_min=tk.IntVar(value=30)
        self.stay_sec=tk.IntVar(value=30)
        self.gender=tk.StringVar(value="Male")
        self.sound=tk.BooleanVar(value=True)
        self.water=tk.BooleanVar(value=True)
        self.move=tk.BooleanVar(value=True)

        self.male_frames=self.load_gif_frames(resource_path("mascot_male.gif"))
        self.female_frames=self.load_gif_frames(resource_path("mascot_female.gif"))
        self.preview_index=0

        self.build_ui()
        self.animate_preview()
        self.update_clock()

    def load_gif_frames(self,path):
        im=Image.open(path)
        frames=[]
        try:
            while True:
                frame=im.convert("RGBA").copy()
                frames.append(frame)
                im.seek(im.tell()+1)
        except EOFError:
            pass
        return frames

    def build_ui(self):
        tk.Label(self.root,text="HYDRO BUDDY",font=("Segoe UI",19,"bold"),
                 bg=APP_BG,fg=TEXT).pack(pady=(20,2))
        tk.Label(self.root,text="A tiny reminder to drink, breathe & move.",
                 font=("Segoe UI",9),bg=APP_BG,fg=MUTED).pack()

        self.preview=tk.Label(self.root,bg=APP_BG)
        self.preview.pack(pady=8)

        self.timer_label=tk.Label(self.root,text="30:00",font=("Segoe UI",28,"bold"),
                                  bg=APP_BG,fg=TEAL)
        self.timer_label.pack()

        settings=tk.Frame(self.root,bg=APP_BG)
        settings.pack(pady=7)
        self.add_setting(settings,"Reminder every",self.interval_min,[15,30,45,60],"minutes",0)
        self.add_setting(settings,"Popup stays",self.stay_sec,[30,45,60,90,120],"seconds",1)

        tk.Label(settings,text="Mascot",bg=APP_BG,fg=TEXT,font=("Segoe UI",9)).grid(
            row=2,column=0,padx=5,pady=5,sticky="e")
        gender_box=ttk.Combobox(settings,textvariable=self.gender,
                                values=["Male","Female"],width=8,state="readonly")
        gender_box.grid(row=2,column=1,padx=5,pady=5)
        gender_box.bind("<<ComboboxSelected>>",lambda e:self.reset_preview())

        tk.Label(self.root,text="Choose your mascot",font=("Segoe UI",8),
                 bg=APP_BG,fg="#87959A").pack()

        self.start_btn=ttk.Button(self.root,text="Start reminders",command=self.toggle)
        self.start_btn.pack(pady=(10,4))
        ttk.Button(self.root,text="🧪  Test in 1 minute",command=self.start_test).pack(pady=3)

        options=tk.Frame(self.root,bg=APP_BG); options.pack(pady=8)
        tk.Checkbutton(options,text="💧 Water",variable=self.water,bg=APP_BG,activebackground=APP_BG).grid(row=0,column=0,sticky="w")
        tk.Checkbutton(options,text="🚶 Move",variable=self.move,bg=APP_BG,activebackground=APP_BG).grid(row=1,column=0,sticky="w")
        tk.Checkbutton(options,text="🔔 Sound",variable=self.sound,bg=APP_BG,activebackground=APP_BG).grid(row=0,column=1,sticky="w",padx=20)

        tk.Label(self.root,text="The reminder appears at the bottom-right.",
                 font=("Segoe UI",8),bg=APP_BG,fg="#87959A").pack(pady=3)

    def add_setting(self,parent,label,var,values,suffix,row):
        tk.Label(parent,text=label,bg=APP_BG,fg=TEXT,font=("Segoe UI",9)).grid(
            row=row,column=0,padx=5,pady=5,sticky="e")
        combo=ttk.Combobox(parent,textvariable=var,values=values,width=7,state="readonly")
        combo.grid(row=row,column=1,padx=5,pady=5)
        tk.Label(parent,text=suffix,bg=APP_BG,fg=MUTED).grid(
            row=row,column=2,padx=5,pady=5,sticky="w")
        if label=="Reminder every":
            combo.bind("<<ComboboxSelected>>",lambda e:self.reset_interval())

    def reset_interval(self):
        self.remaining=self.interval_min.get()*60
        self.update_label()

    def reset_preview(self):
        self.preview_index=0

    def animate_preview(self):
        frames=self.female_frames if self.gender.get()=="Female" else self.male_frames
        if frames:
            im=frames[self.preview_index % len(frames)].resize((145,145),Image.Resampling.LANCZOS)
            self.preview_img=ImageTk.PhotoImage(im)
            self.preview.config(image=self.preview_img)
            self.preview_index+=1
        self.root.after(83,self.animate_preview)

    def update_label(self):
        m,s=divmod(max(0,self.remaining),60)
        self.timer_label.config(text=f"{m:02d}:{s:02d}")

    def toggle(self):
        self.running=not self.running
        self.test_mode=False
        if self.running and self.remaining<=0:
            self.remaining=self.interval_min.get()*60
        self.start_btn.config(text="Pause reminders" if self.running else "Start reminders")

    def start_test(self):
        self.running=False
        self.test_mode=True
        self.remaining=60
        self.start_btn.config(text="Start reminders")
        self.update_label()

    def update_clock(self):
        if self.test_mode or self.running:
            self.remaining-=1
            if self.remaining<=0:
                was_test=self.test_mode
                self.test_mode=False
                self.show_reminder(was_test)
                self.remaining=self.interval_min.get()*60
        self.update_label()
        self.root.after(1000,self.update_clock)

    def show_reminder(self,test=False):
        if self.sound.get():
            try: self.root.bell()
            except: pass

        messages=[]
        if self.water.get(): messages.append(("WATER","Take a few sips of water."))
        if self.move.get(): messages.append(("MOVE","Stand up & move for 2 minutes."))
        if not messages: messages=[("RESET","Take a tiny reset.")]

        popup=tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.attributes("-topmost",True)
        popup.configure(bg="#DCE5E3")
        popup.lift(); popup.focus_force()

        sw,sh=popup.winfo_screenwidth(),popup.winfo_screenheight()
        W,H=405,285
        final_x=sw-W-24
        final_y=sh-H-42
        start_y=sh+10
        popup.geometry(f"{W}x{H}+{final_x}+{start_y}")
        popup.attributes("-alpha",0.0)

        card=tk.Canvas(popup,width=W,height=H,bg="#DCE5E3",highlightthickness=0)
        card.pack(fill="both",expand=True)
        self.round_rect(card,5,5,W-5,H-5,18,fill="#DCE5E3",outline="")
        self.round_rect(card,2,2,W-8,H-8,18,fill=CARD,outline=LINE,width=1)

        # Close button
        close_bg="#F0F5F4"
        card.create_oval(W-43,14,W-15,42,fill=close_bg,outline="")
        card.create_text(W-29,28,text="×",font=("Segoe UI",16,"bold"),fill=MUTED,tags="close")
        card.tag_bind("close","<Button-1>",lambda e:popup.destroy())

        status="TEST REMINDER" if test else "HYDRO BUDDY"
        self.round_rect(card,145,15,245,38,12,fill=AQUA,outline="")
        card.create_oval(157,24,165,32,fill=TEAL,outline="")
        card.create_text(201,26.5,text=status,font=("Segoe UI",8,"bold"),fill=TEAL_DARK)

        # Animated uploaded mascot GIF
        mascot=tk.Label(popup,bg=CARD)
        mascot.place(x=112,y=43,width=180,height=112)

        frames=self.female_frames if self.gender.get()=="Female" else self.male_frames
        state={"i":0}
        def animate():
            if not popup.winfo_exists(): return
            if frames:
                im=frames[state["i"]%len(frames)].resize((112,112),Image.Resampling.LANCZOS)
                img=ImageTk.PhotoImage(im)
                mascot.configure(image=img)
                mascot.image=img
                state["i"]+=1
            popup.after(83,animate)
        animate()

        # message rows
        y=153
        for kind,text in messages[:2]:
            col=TEAL if kind=="WATER" else BLUE
            card.create_oval(43,y+3,51,y+11,fill=col,outline="")
            card.create_text(62,y,text=kind,anchor="w",font=("Segoe UI",8,"bold"),fill=MUTED)
            card.create_text(62,y+18,text=text,anchor="w",font=("Segoe UI",10,"bold"),fill=TEXT)
            y+=43

        card.create_line(42,226,W-42,226,fill=LINE)
        card.create_text(W/2,239,text="A tiny reset now = better energy later.",
                        font=("Segoe UI",8),fill=MUTED)

        # Explicit dismiss button
        self.round_rect(card, W-120, 249, W-22, 276, 10, fill=AQUA, outline="")
        card.create_text(W-71,262,text="Dismiss",font=("Segoe UI",8,"bold"),fill=TEAL_DARK,tags="dismiss")
        card.tag_bind("dismiss","<Button-1>",lambda e:popup.destroy())

        # Slide + fade entrance
        n=[0]
        def enter():
            if not popup.winfo_exists(): return
            n[0]+=1
            p=min(1,n[0]/20)
            eased=1-(1-p)**3
            yy=int(start_y+(final_y-start_y)*eased)
            popup.geometry(f"{W}x{H}+{final_x}+{yy}")
            popup.attributes("-alpha",min(1,p*1.15))
            if p<1: popup.after(25,enter)
        enter()

        popup.after(max(30,self.stay_sec.get())*1000,popup.destroy)

    def round_rect(self,canvas,x1,y1,x2,y2,r,fill,outline="",width=1):
        canvas.create_arc(x1,y1,x1+2*r,y1+2*r,start=90,extent=90,fill=fill,outline=outline,width=width)
        canvas.create_arc(x2-2*r,y1,x2,y1+2*r,start=0,extent=90,fill=fill,outline=outline,width=width)
        canvas.create_arc(x1,y2-2*r,x1+2*r,y2,start=180,extent=90,fill=fill,outline=outline,width=width)
        canvas.create_arc(x2-2*r,y2-2*r,x2,y2,start=270,extent=90,fill=fill,outline=outline,width=width)
        canvas.create_rectangle(x1+r,y1,x2-r,y2,fill=fill,outline="")
        canvas.create_rectangle(x1,y1+r,x2,y2-r,fill=fill,outline="")

if __name__=="__main__":
    root=tk.Tk()
    try: ttk.Style().theme_use("vista")
    except: pass
    HydroBuddy(root)
    root.mainloop()
