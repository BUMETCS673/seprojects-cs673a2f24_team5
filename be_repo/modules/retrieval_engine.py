# retrieval_engine.py

from langchain_neo4j import GraphCypherQAChain
from langchain_openai import ChatOpenAI
from langchain.chains.retrieval import create_retrieval_chain 
from langchain.chains.combine_documents import create_stuff_documents_chain
from configs.openai_key import get_openai_api_key  # New import
from langchain.prompts import PromptTemplate

class RetrievalEngine:
    def __init__(self, resume_processor, neo4j_model):
        """
        Initialize the Retrieval Engine with necessary components.
        
        Parameters:
            resume_processor (ResumeProcessor): Instance to process resumes.
            neo4j_model (Neo4jModel): Instance to interact with Neo4j.
        """
        self.resume_processor = resume_processor
        self.neo4j_model = neo4j_model

        # Initialize Language Model (already initialized in Neo4jModel)
        self.llm = self.neo4j_model.llm
        
        # Initialize GraphCypherQAChain (already initialized in Neo4jModel)
        self.graph_chain = self.neo4j_model.get_graph_chain()

        # Define the PromptTemplate with 'context' as input variable
        template="""
            You are an assistant that matches resumes to relevant job descriptions.

            Given the user's resume, find the most relevant job descriptions.

            **Entities to Extract:**
            - **Education (Edu):** Details about degrees, fields of study, institutions, start and end years, GPA.
            - **Work Experience (WE):** Positions held, companies, locations.
            - **Projects (Proj):** Project titles, descriptions, technologies used, roles.
            - **Skills (Skill):** Technical and soft skills.
            - **Certifications (Cert):** Certification names, issuing organizations, expiration dates.
            - **Soft Skills (SSkill):** Non-technical skills like leadership, communication.

            **Resume:**
            \"\"\"
            {context}
            \"\"\"
            """
        
        self.prompt_template = PromptTemplate(
            template=template,
            input_variables=["input"]
        )

        # Create a documents chain
        self.combine_docs_chain = create_stuff_documents_chain(self.llm, self.prompt_template)

    def perform_mixed_retrieval(self, resume_text, node_label="JD"):
        """
        Perform mixed retrieval using vector similarity and graph traversal.
        
        Parameters:
            resume_text (str): The user's resume text.
            node_label (str): The node label to perform retrieval on ('JD', 'JTitle', 'JKeyword').
        
        Returns:
            Tuple[List[Document], dict]: Results from vector similarity and graph traversal.
        """
        # Process resume into a Document
        doc = self.resume_processor.process_resume(resume_text)
        
        if not doc:
            return [], {}
        
        # Store the Document in the appropriate vector store
        self.neo4j_model.store_documents([doc], node_label=node_label)
        
        # Access the schema property correctly
        schema = self.neo4j_model.graph.get_schema

        # Get the retriever for the given node label
        retriever = self.neo4j_model.get_retriever(node_label=node_label)

        # Create the retrieval chain with the retriever and the combine_docs_chain
        retrieval_chain = create_retrieval_chain(
            retriever,
            self.combine_docs_chain
        )

        # Perform vector similarity search
        similar_docs_result = retrieval_chain.invoke({"input": resume_text})  # Corrected to 'context'
        similar_docs = similar_docs_result.get("output", [])
        print("similar_docs_result:", similar_docs_result)
        print("Keys in similar_docs_result:", similar_docs_result.keys())
        
        for doc in similar_docs:
            print("Document Metadata:", doc.metadata)

        query = f"Based on the following resume, recommend relevant job positions: {resume_text}"
        graph_response = self.graph_chain.invoke({"query": query, "schema": schema})
        # After graph query
        print("Graph Response:")
        print(graph_response)
       
        return similar_docs, graph_response