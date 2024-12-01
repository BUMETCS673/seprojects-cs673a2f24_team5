# job_recommendation_system.py

from neo4j_model import Neo4jModel
from resume_processor import ResumeProcessor
from retrieval_engine import RetrievalEngine
from recommendation_generator import RecommendationGenerator
from view import CLIView
import sys

def main():
    

    # Redirect standard output to a file
    sys.stdout = open('output.log', 'w')

    # Your code here
    print("Lots of output")


    # Setup Logging
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    # Neo4j Connection Details
    NEO4J_URI = "neo4j+ssc://7bf5a48e.databases.neo4j.io"  # Replace with your Neo4j URI
    NEO4J_USERNAME = "neo4j"             # Replace with your Neo4j username
    NEO4J_PASSWORD = "oxsK7V5_86emZlYQlvCfQHfVWS95wXz29OhtU8GAdFc"          # Replace with your Neo4j password

    # Initialize Model
    neo4j_model = Neo4jModel(
        uri=NEO4J_URI,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD
    )
    
    # Initialize Controller Components
    resume_processor = ResumeProcessor()
    retrieval_engine = RetrievalEngine(resume_processor, neo4j_model)
    recommendation_generator = RecommendationGenerator()
    
    # Initialize View
    view = CLIView()
    
    # Get Resume Input from User
    resume_text = view.get_resume_input()
    
    if not resume_text.strip():
        logger.error("No resume text provided.")
        print("Error: No resume text provided.")
        return
    
    # Perform Mixed Retrieval for 'JD' Node Label
    node_label = "JD"  # Adjust as needed; could be dynamic based on user input or other criteria
    similar_docs, graph_results = retrieval_engine.perform_mixed_retrieval(resume_text, node_label=node_label)
    
    if not similar_docs and not graph_results:
        print("No job recommendations found based on your resume.")
        return
    
    # Generate Recommendations
    try:
        recommendations = recommendation_generator.generate_recommendations(similar_docs, graph_results)
    except Exception as e:
        print("Error: Failed to generate job recommendations.")
        return
    
    # Display Recommendations
    view.display_recommendations(recommendations)

    # Close the file
    sys.stdout.close()

if __name__ == "__main__":
    main()
