import os
import tkinter as tk
from tkinter import messagebox
from pdf_loader import load_pdf
from rag_chain import create_rag_chain, answer_question
from vector_store import create_vector_store, upload_pdf

class PDFChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RAG App")
        self.root.geometry("600x600")

        # Frame for chat history
        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.scrollbar = tk.Scrollbar(self.chat_frame, orient=tk.VERTICAL)
        self.chat_text = tk.Text(self.chat_frame, wrap=tk.WORD, yscrollcommand=self.scrollbar.set, state=tk.DISABLED, font=("Helvetica", 12))
        self.scrollbar.config(command=self.chat_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame for user input
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.input_entry = tk.Entry(self.input_frame, font=("Helvetica", 14))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", self.ask_question)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.ask_question, font=("Helvetica", 12))
        self.send_button.pack(side=tk.RIGHT)

        self.upload_button = tk.Button(self.root, text="Upload PDF", command=self.upload_pdf, font=("Helvetica", 12))
        self.upload_button.pack(pady=10)

        self.pdf_path = None
        self.rag_chain = None

    def append_to_chat(self, text, role):
        self.chat_text.config(state=tk.NORMAL)
        if role == "question":
            self.chat_text.insert(tk.END, f"You: {text}\n", ("question",))
        else:
            self.chat_text.insert(tk.END, f"Bot: {text}\n", ("answer",))
        self.chat_text.tag_config("question", foreground="blue")
        self.chat_text.tag_config("answer", foreground="green")
        self.chat_text.see(tk.END)
        self.chat_text.config(state=tk.DISABLED)

    def upload_pdf(self):
        file_path = upload_pdf()
        if file_path:
            self.pdf_path = file_path
            self.append_to_chat(f"PDF loaded from: {file_path}", "answer")
            self.prepare_pdf_for_questioning(file_path)
        else:
            messagebox.showwarning("File Selection", "No file selected. Please upload a PDF.")

    def prepare_pdf_for_questioning(self, file_path):
        splits = load_pdf(file_path)
        retriever = create_vector_store(splits)
        self.rag_chain = create_rag_chain(retriever)

    def ask_question(self, event=None):
        question = self.input_entry.get().strip()
        if question:
            self.append_to_chat(question, "question")
            self.input_entry.delete(0, tk.END)
            if not self.rag_chain:
                self.append_to_chat("Please upload a PDF first.", "answer")
                return

            try:
                answer = answer_question(self.rag_chain, question)
                self.append_to_chat(answer, "answer")
            except Exception as e:
                self.append_to_chat(f"Error: {e}", "answer")
        else:
            messagebox.showwarning("Input Error", "Please enter a question.")

if __name__ == "__main__":
    os.environ['HUGGINGFACEHUB_API_TOKEN'] = 'YOUR_HUGGINGFACE_API_TOKEN'
    root = tk.Tk()
    app = PDFChatApp(root)
    root.mainloop()

