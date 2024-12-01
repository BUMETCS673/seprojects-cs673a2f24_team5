# recommendation_generator.py

class RecommendationGenerator:
    def __init__(self):
        pass

    def merge_results(self, vector_docs, graph_results):
        combined_jobs = {}

        # Process vector similarity results
        for doc in vector_docs:
            # Exclude 'id' and get all other non-empty metadata properties
            metadata = {k: v for k, v in doc.metadata.items() if k != 'id' and v}
            # Create a description string from the non-empty properties
            job_description = ', '.join(f"{k}: {v}" for k, v in metadata.items())
            if job_description:
                combined_jobs[job_description] = combined_jobs.get(job_description, 0) + 1

        # Process graph traversal results
        intermediate_steps = graph_results.get('intermediate_steps', [])
        if len(intermediate_steps) > 1:
            context = intermediate_steps[1].get('context', [])
            for job in context:
                # Exclude 'id' and get all other non-empty properties
                job_data = {k: v for k, v in job.items() if k != 'id' and v}
                # Create a description string
                job_description = ', '.join(f"{k}: {v}" for k, v in job_data.items())
                if job_description:
                    combined_jobs[job_description] = combined_jobs.get(job_description, 0) + 1

        # Include the 'result' from 'graph_results' directly
        graph_result_text = graph_results.get('result', '').strip()
        if graph_result_text:
            combined_jobs[graph_result_text] = combined_jobs.get(graph_result_text, 0) + 1

        # Convert to sorted list based on combined score
        sorted_jobs = sorted(combined_jobs.items(), key=lambda item: item[1], reverse=True)
        return [job for job, score in sorted_jobs]

    def generate_recommendations(self, vector_docs, graph_results):
        """
        Generate a ranked list of job recommendations by merging vector and graph results.

        Parameters:
            vector_docs (List[Document]): Documents from vector similarity search.
            graph_results (dict): Results from graph traversal.

        Returns:
            List[str]: Ranked list of unique job recommendations.
        """
        return self.merge_results(vector_docs, graph_results)
