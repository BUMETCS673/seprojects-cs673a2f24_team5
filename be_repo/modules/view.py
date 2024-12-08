# view.py

class CLIView:
    def __init__(self):
        pass

    def get_resume_input(self):
        """
        Prompt user to input their resume text.
        """
        print("Welcome to the Job Recommendation System!")
        print("Please paste your resume text below (end input with an empty line):")
        resume_lines = []
        while True:
            try:
                line = input()
                if line.strip() == "":
                    break
                resume_lines.append(line)
            except EOFError:
                # Handle end of file (e.g., user sends EOF signal)
                break
        resume_text = "\n".join(resume_lines)
        return resume_text

    def display_recommendations(self, recommendations):
        """
        Display job recommendations to the user.
        """
        if not recommendations:
            return "No job recommendations found based on your resume."
        res = "\nRecommended Jobs for You:\n"
        for idx, job in enumerate(recommendations, start=1):
            res += f"{idx}. {job}\n"
        return res
