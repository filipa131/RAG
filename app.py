import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from pdf_loader import load_pdf
from rag_chain import create_rag_chain, answer_question  
from vector_store import create_vector_store, upload_pdf

class PDFQuestionAnsweringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Question Answering App")
        self.root.geometry("600x400")

        self.label = tk.Label(self.root, text="Welcome to the PDF Question Answering App", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.upload_button = tk.Button(self.root, text="Upload PDF", width=20, command=self.upload_pdf)
        self.upload_button.pack(pady=10)

        self.question_button = tk.Button(self.root, text="Ask a Question", width=20, state=tk.DISABLED, command=self.ask_question)
        self.question_button.pack(pady=10)

        self.answer_label = tk.Label(self.root, text="Answer will appear here", font=("Helvetica", 12), wraplength=500)
        self.answer_label.pack(pady=20)

        self.pdf_path = None
        self.rag_chain = None

    def upload_pdf(self):
        file_path = upload_pdf()
        if file_path:
            self.pdf_path = file_path
            self.label.config(text=f"PDF loaded from: {file_path}")
            self.prepare_pdf_for_questioning(file_path)
            self.question_button.config(state=tk.NORMAL)
        else:
            self.label.config(text="No file selected. Please upload a PDF.")

    def prepare_pdf_for_questioning(self, file_path):
        splits = load_pdf(file_path)
        retriever = create_vector_store(splits)
        self.rag_chain = create_rag_chain(retriever)

    def ask_question(self):
        question = simpledialog.askstring("Input", "Enter your question:", parent=self.root)
        if question:
            answer = answer_question(self.rag_chain, question)  
            self.answer_label.config(text=f"Answer: {answer}")
        else:
            messagebox.showwarning("Input Error", "Please enter a valid question.")

if __name__ == "__main__":
    import os
    from tkinter import Tk
    os.environ['HUGGINGFACEHUB_API_TOKEN'] = 'YOUR_HUGGINGFACEHUB_API_TOKEN'
    root = Tk()
    app = PDFQuestionAnsweringApp(root)
    root.mainloop()
