# PDF Question Answering App

## Overview
The **PDF Question Answering App** is a Python-based GUI application that allows users to upload a PDF document, process it, and ask questions about its content. The app uses advanced natural language processing (NLP) techniques to retrieve and generate answers based on the context provided in the uploaded PDF.

---

## Features
- **PDF Upload**: Easily upload a PDF file to the application.
- **Question Answering**: Ask questions related to the content of the uploaded PDF and receive precise answers.
- **User-Friendly Interface**: A simple GUI designed with Tkinter for easy interaction.

---

## Prerequisites

### Python Libraries
Ensure you have the following Python libraries installed:

- `os`
- `tkinter`
- `langchain`
- `langchain_community`
- `sentence-transformers`
- `Chroma`

You can install the required libraries using pip:
```bash
pip install langchain langchain-community sentence-transformers chroma
```

### Environment Variable
You need to set the environment variable `HUGGINGFACEHUB_API_TOKEN` with your Hugging Face API token:

```bash
export HUGGINGFACEHUB_API_TOKEN='your_huggingfacehub_api_token'
```

---

## File Structure
- **`app.py`**: The main application file containing the GUI logic.
- **`pdf_loader.py`**: Handles PDF loading and splitting into manageable text chunks.
- **`rag_chain.py`**: Creates a Retrieval-Augmented Generation (RAG) chain for answering questions.
- **`vector_store.py`**: Manages vector store creation and file dialog logic for PDF upload.

---

## Usage

1. **Run the Application**:
   ```bash
   python app.py
   ```

2. **Upload a PDF**:
   - Click the **Upload PDF** button.
   - Select a PDF file from your system.

3. **Ask a Question**:
   - Once the PDF is processed, click **Ask a Question**.
   - Enter your question in the prompt and receive the answer.

---

## Technologies Used
- **LangChain**: For building RAG chains and document processing.
- **Hugging Face**: To access the `google/flan-t5-base` model for generating answers.
- **Sentence Transformers**: For embedding text chunks into vectors.
- **Chroma**: As the vector database.
- **Tkinter**: For creating the graphical user interface.

---

## Demo Picture

Demonstration of the application, where a cover letter is uploaded and questions are answered based on the uploaded document:

![RAG_app](https://github.com/user-attachments/assets/5e96b8ab-62d9-4a26-80e7-b2f9c8a4576c)