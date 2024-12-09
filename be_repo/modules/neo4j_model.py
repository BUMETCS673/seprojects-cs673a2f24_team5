# neo4j_model.py
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_community.vectorstores import Neo4jVector
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from configs.openai_key import get_openai_api_key  # New import
from langchain.prompts import PromptTemplate

custom_cypher_prompt = PromptTemplate(
    input_variables=["question", "schema"],
    template="""
    You are an expert Cypher query writer for a Neo4j graph database.

    The database has the following schema:

    {schema}

    Given the user's question, generate an efficient Cypher query that:

    - Retrieves relevant job recommendations based on the user's resume.
    - Excludes the 'embedding' property to avoid exceeding context limits.
    - Limits the number of results to avoid duplicates and improve performance.
    - Returns relevant job recommendations based on the user's resume.

    Question:
    {question}

    Cypher Query:
    """
)


class Neo4jModel:
    def __init__(self, uri, username, password):

        # Initialize Neo4j Graph connection
        self.graph = Neo4jGraph(
            url=uri,
            username=username,
            password=password,
            # enhanced_schema=True,  # Optional: Provides more detailed schema information
        )

        # Initialize the embedding model with the API key
        api_key = get_openai_api_key()
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        
        # Initialize Neo4jVector for each node label
        self.vector_store_jd = Neo4jVector.from_existing_index(
            embedding=self.embeddings,
            url=uri,
            username=username,
            password=password,
            index_name="jd_embedding_index",
        )
        
        
        self.vector_store_jtitle = Neo4jVector.from_existing_index(
            embedding=self.embeddings,
            url=uri,
            username=username,
            password=password,
            index_name="jtitle_embedding_index",
        )
        
        
        self.vector_store_jkeyword = Neo4jVector.from_existing_index(
            embedding=self.embeddings,
            url=uri,
            username=username,
            password=password,
            index_name="jkeyword_embedding_index",
        )

        # Initialize Language Model for QA Chain
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=api_key)

        # Initialize GraphCypherQAChain
        self.graph_chain = GraphCypherQAChain.from_llm(
            graph=self.graph,
            llm=self.llm,
            cypher_prompt=custom_cypher_prompt,
            return_intermediate_steps=True,
            verbose=True,
            validate_cypher=True,  # Ensures correct relationship directions
            allow_dangerous_requests=True,
        )
        
    def store_documents(self, docs, node_label="JD"):
        """
        Store documents in Neo4jVector with embeddings.
        """
        # Ensure that 'docs' is a list of Document objects
        if node_label == "JD":
            self.vector_store_jd.add_documents(docs)
            
        elif node_label == "JTitle":
            self.vector_store_jtitle.add_documents(docs)
            
        elif node_label == "JKeyword":
            self.vector_store_jkeyword.add_documents(docs)
            
        else:
            
            raise ValueError(f"Invalid node_label '{node_label}'. Must be 'JD', 'JTitle', or 'JKeyword'.")
    
    def query_graph(self, cypher_query, parameters=None):
        """
        Execute a Cypher query against the Neo4j graph.
        """
        results = self.graph.query(cypher_query, parameters)
        return results
    
    def get_retriever(self, node_label="JD"):
        """
        Get a retriever from the Neo4jVector for vector similarity searches.
        """
        try:
            if node_label == "JD":
                return self.vector_store_jd.as_retriever()
            elif node_label == "JTitle":
                return self.vector_store_jtitle.as_retriever()
            elif node_label == "JKeyword":
                return self.vector_store_jkeyword.as_retriever()
            else:
                raise ValueError(f"Invalid node_label '{node_label}'. Must be 'JD', 'JTitle', or 'JKeyword'.")
        except Exception as e:
            raise e
        
    def get_graph_chain(self):
        """
        Get the GraphCypherQAChain instance.
        
        Returns:
            GraphCypherQAChain: The QA chain instance.
        """
        return self.graph_chain