import tkinter as tk
import asyncio
import rx
import rx.operators as op
from rx.subject import Subject
from rx.scheduler import EventLoopScheduler
from threading import current_thread

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # https://www.delftstack.com/ja/howto/python-tkinter/how-to-set-height-and-width-of-tkinter-entry-widget/
        self.master.geometry('800x600')
        self.pack(expand=True,fill='both')
        # https://rxpy.readthedocs.io/en/latest/reference_subject.html
        self.text_subject = Subject()
        self.create_widgets()

    def create_widgets(self):
        self.text = tk.Text(self,height=1)
        # self.text.pack(expand=True,fill='x')
        self.text.pack(expand=True,fill='both')
        # http://www27.cs.kobe-u.ac.jp/~masa-n/misc/cmc/perltk/basic/bind.html
        self.text.bind('<KeyRelease>',self.on_input_text)

        self.text2 = tk.Text(self,height=1)
        # https://blog.narito.ninja/detail/100/
        self.text2.insert(tk.END,"この下に入力されます\n")
        self.text2.configure(state='disabled')
        self.text2.pack(expand=True,fill='both',ipady=0)
        self.text3 = tk.Text(self)
        # https://www.delftstack.com/ja/howto/python-tkinter/how-to-make-tkinter-text-widget-read-only/
        # self.text3.configure(state='disabled')
        self.text3.pack(expand=True,fill='both')
        print(self.text3.get('1.0',tk.END))
    
    def on_input_text(self,*args):
        print(args)
        # print(self.text.get('1.0',tk.END))
        # https://www.delftstack.com/ja/howto/python-tkinter/how-to-get-the-input-from-tkinter-text-box/
        text = self.text.get('1.0',tk.END)
        print('call on next',text)
        self.text_subject.on_next(text)

def on_next(value):
    print('receive on next',current_thread().name,value)
    # https://www.delftstack.com/ja/howto/python-tkinter/how-to-clear-tkinter-text-box-widget/
    app.text3.delete('1.0',tk.END)
    app.text3.insert(tk.END,value)

root = tk.Tk()
app = Application(master=root)
# https://rxpy.readthedocs.io/en/latest/reference_operators.html
app.text_subject.pipe(
    op.debounce(0.5),
    op.distinct_until_changed()
).subscribe(
    on_next=on_next
)
app.mainloop()

# https://pypi.org/project/aioreactive/
# https://qiita.com/Y0KUDA/items/0438169802becc6d811e