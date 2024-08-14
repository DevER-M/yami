import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from datetime import datetime
import random
import time


li = ['the', 'be', 'of', 'and', 'a', 'to', 'in', 'he', 'have', 'it', 'that', 'for', 'they', 'with', 'as', 'not', 'on', 'she', 'at', 'by', 'this', 'we', 'you', 'do', 'but', 'from', 'or', 'which', 'one', 'would', 'all', 'will', 'there', 'say', 'who', 'make', 'when', 'can', 'more', 'if', 'no', 'man', 'out', 'other', 'so', 'what', 'time', 'up', 'go', 'about', 'than', 'into', 'could', 'state', 'only', 'new', 'year', 'some', 'take', 'come', 'these', 'know', 'see', 'use', 'get', 'like', 'then', 'first', 'any', 'work', 'now', 'may', 'such', 'give', 'over', 'think', 'most', 'even', 'find', 'day', 'also', 'after', 'way', 'many', 'must', 'look', 'before', 'great', 'back', 'through', 'long', 'where', 'much', 'should', 'well', 'people', 'down', 'own', 'just', 'because', 'good', 'each', 'those', 'feel', 'seem', 'how', 'high', 'too', 'place', 'little', 'world', 'very', 'still', 'nation', 'hand', 'old', 'life', 'tell', 'write', 'become', 'here', 'show', 'house', 'both', 'between']

class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.style = Style(theme='darkly')  # You can choose any theme you like
        self.root.title("Typing Test App")

        self.create_widgets()
        self.start_time=None

   
    def create_widgets(self):
        self.prompt_label = ttk.Label(self.root, text="Type the text below:", font=("Arial", 14))
        self.prompt_label.pack(padx=10,side="left",fill="both")

        self.text_display = tk.Text(self.root, font=("Arial", 12), wrap="word", height=4, width=50)
        self.text_display.pack(pady=10)
        self.text_display.tag_configure("correct", foreground="green")
        self.text_display.tag_configure("incorrect", foreground="red")
        self.text_display.insert("1.0", self.get_random_text())
        self.text_display.config(state=tk.DISABLED)

        self.input_text = ttk.Entry(self.root, font=("Arial", 12))
        self.input_text.pack(pady=10,side='left')
        self.input_text.bind("<KeyRelease>", self.update_text)

        self.results_label = ttk.Label(self.root, text="", font=("Arial", 12))
        self.results_label.pack(pady=10)

        self.restart_button = ttk.Button(self.root,command=self.restart,text="restart")
        self.restart_button.pack(pady=10,side='left')

    def get_random_text(self):
        return random.sample(li,10)
    
    def restart(self):
        self.text_display.delete('1.0','end')
        self.text_display.insert("1.0",self.get_random_text())
        self.text_display.config(state=tk.NORMAL)
        self.input_text.config(state='normal')
        self.input_text.delete('0','end')

    def update_text(self, event):
        typed_text = self.input_text.get()
        prompt_text = self.text_display.get("1.0", tk.END).strip()
        
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete("1.0", tk.END)

        # Highlight matching and non-matching text
        for i, char in enumerate(prompt_text):
            if i < len(typed_text):
                if char == typed_text[i]:
                    self.text_display.insert(tk.END, char, "correct")
                else:
                    self.text_display.insert(tk.END, char, "incorrect")
            else:
                self.text_display.insert(tk.END, char)
        
        if typed_text == prompt_text:
            if self.start_time is None:
                self.start_time = datetime.now()
            self.show_results()
            return
        
        self.text_display.config(state=tk.DISABLED)

        if self.start_time is None and len(typed_text) > 0:
            self.start_time = datetime.now()

    def show_results(self):
        elapsed_time = (datetime.now() - self.start_time).total_seconds()
        num_words = len(self.text_display.get("1.0", tk.END).strip().split())
        wpm = (num_words / elapsed_time) * 60
        
        self.results_label.config(text=f"Correct! Your typing speed is {wpm:.2f} WPM.\nTime taken: {elapsed_time:.2f} seconds.")
        self.input_text.config(state='disabled')

def main():
    root = tk.Tk()
    app = TypingTestApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()