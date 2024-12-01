# recommendation_generator.py

class RecommendationGenerator:
    def __init__(self):
        pass

    def merge_results(self, vector_docs, graph_results):
        combined_jobs = {}

        # Process vector similarity results
        for doc in vector_docs:
            comp = doc.metadata.get("comp", "")
            resp = doc.metadata.get("resp", "")
            job_title = f"{resp} at {comp}".strip()
            if job_title:
                combined_jobs[job_title] = combined_jobs.get(job_title, 0) + 1

        # Process graph traversal results
        # Access the context from intermediate steps
        intermediate_steps = graph_results.get('intermediate_steps', [])
        if len(intermediate_steps) > 1:
            context = intermediate_steps[1].get('context', [])
            for job in context:
                job_title = job.get('job_title', '')
                company = job.get('company', '')
                if job_title and company:
                    combined_job = f"{job_title} at {company}"
                    combined_jobs[combined_job] = combined_jobs.get(combined_job, 0) + 1

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
