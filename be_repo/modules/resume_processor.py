# resume_processor.py

from langchain.docstore.document import Document

class ResumeProcessor:
    def __init__(self):
        """
        Initialize the Resume Processor.
        """
    
    def process_resume(self, resume_text):
        """
        Process the user's resume to create a Document object.
        
        Parameters:
            resume_text (str): The user's resume text.
        
        Returns:
            Document or None: The processed resume as a LangChain Document or None if failed.
        """
        try:
            doc = Document(page_content=resume_text, metadata={})
            return doc
        except Exception as e:
            return None
