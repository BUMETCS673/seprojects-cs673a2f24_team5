# job_recommendation_system.py

import logging

from .neo4j_model import Neo4jModel
from .recommendation_generator import RecommendationGenerator
from .resume_processor import ResumeProcessor
from .retrieval_engine import RetrievalEngine
from .view import CLIView


def job_recommend(resume_text, user_id):
    # Setup Logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    # Get Resume Input from User
    if not resume_text.strip():
        logger.error(f'No resume text provided, user_id: {user_id}.')
        return 'Error: No resume text provided.'

    # Neo4j Connection Details
    NEO4J_URI = "neo4j+ssc://7bf5a48e.databases.neo4j.io"  # Replace with your Neo4j URI
    NEO4J_USERNAME = "neo4j"  # Replace with your Neo4j username
    NEO4J_PASSWORD = "oxsK7V5_86emZlYQlvCfQHfVWS95wXz29OhtU8GAdFc"  # Replace with your Neo4j password

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

    # Perform Mixed Retrieval for 'JD' Node Label
    node_label = "JD"  # Adjust as needed; could be dynamic based on user input or other criteria
    similar_docs, graph_results = retrieval_engine.perform_mixed_retrieval(resume_text, node_label=node_label)

    if not similar_docs and not graph_results:
        return 'No job recommendations found based on your resume.'

    # Generate Recommendations
    try:
        recommendations = recommendation_generator.generate_recommendations(similar_docs, graph_results)
    except Exception as e:
        return 'Error: Failed to generate job recommendations.'

    # Display Recommendations
    return view.display_recommendations(recommendations)
