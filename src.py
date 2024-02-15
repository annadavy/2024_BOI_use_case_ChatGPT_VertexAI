import urllib
import warnings
from pathlib import Path as p
from pprint import pprint

import pandas as pd
from langchain import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import VertexAIEmbeddings
from langchain.llms import VertexAI

warnings.filterwarnings("ignore")


def retrieve_docs(data_folder, main_url,docs):
    """
    Retrieves documents from specified URLs and extracts their first page content.

    Parameters:
    - main_url (str): The base URL to which the document paths will be appended.
    - docs (list of str): A list of document paths to be appended to the main URL for retrieval.

    Steps:
    1. Iterates over the document paths in 'docs'.
    2. Constructs the full URL for each document and retrieves it as a PDF.
    3. Loads each PDF and extracts the content of the first page.
    4. Stores the first page content of each document in a list.
    5. Concatenates the contents of all first pages into a single string.

    Returns:
    tuple: A tuple containing two elements:
        - pages (list): A list of objects representing the first page of each retrieved document.
        - context (str): A string representing the concatenated contents of the first pages of all documents.
    """
    
    pages=[]
    for doc in docs:
        pdf_url = main_url + doc
        pdf_file = str(p(data_folder, pdf_url.split("/")[-1]))

        urllib.request.urlretrieve(pdf_url, pdf_file)
        pdf_loader = PyPDFLoader(pdf_file)
        page = pdf_loader.load_and_split()
        pages.append(page[0])
        
    len_pages=len(pages)
    context = " ".join(str(p.page_content) for p in pages[:len_pages])
    
    return pages,context

def read_docs(data_folder,docs):
    pages=[]
    for doc in docs:
        pdf_file=str(data_folder) + '/' + doc
        pdf_loader = PyPDFLoader(pdf_file)
        page = pdf_loader.load_and_split()
        pages.append(page[0])

    len_pages=len(pages)
    context = " ".join(str(p.page_content) for p in pages[:len_pages])
    
    return pages,context


def generate_answer(pages, context, question):
    """
    Generates an answer to a given question based on the provided context using Vertex AI models.

    Parameters:
    - context (str): The context text which the answer should be based on.
    - question (str): The question for which the answer is sought.

    Steps:
    1. Initializes two Vertex AI models:
       - 'text-bison@001' for Large Language Model (LLM) text generation.
       - 'textembedding-gecko@001' for embeddings.
    2. Constructs a prompt template for answering questions using the provided context.
    3. Creates a QA chain using the 'text-bison@001' model with the specified prompt.
    4. Generates an answer using the QA chain based on the given context and question.

    Returns:
    str: The generated answer, or "answer not available in context" if the answer cannot be derived from the provided context.
    
    """   
    
    vertex_llm_text = VertexAI(model_name="text-bison@001")
    vertex_embeddings = VertexAIEmbeddings(model_name="textembedding-gecko@001") 
    
       
    prompt_template = """Answer the question as precise as possible using the provided context. If the answer is
                        not contained in the context, say "answer not available in context" \n\n
                        Context: \n {context}?\n
                        Question: \n {question} \n
                        Answer:
                      """

    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context","question"]
    )
    stuff_chain = load_qa_chain(vertex_llm_text, chain_type="stuff", prompt=prompt)
    stuff_answer = stuff_chain(
    {"input_documents": pages, "question": question}, return_only_outputs=True
    )
    return stuff_answer["output_text"]

