## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

# Added PyPDFLoader to read PDF files, which was missing.
from langchain_community.document_loaders import PyPDFLoader
from crewai.tools import tool

## Creating custom pdf reader tool
@tool("Read Financial Document")
def read_data_tool(file_path: str) -> str:
    """Tool to read data from a pdf file from a path.
    The input to this tool is a string representing the file path.
    """
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    full_report = ""
    for data in docs:
        # Clean and format the financial document data
        content = data.page_content
        
        # Remove extra whitespaces and format properly
        while "\n\n" in content:
            content = content.replace("\n\n", "\n")
            
        full_report += content + "\n"
        
    return full_report
