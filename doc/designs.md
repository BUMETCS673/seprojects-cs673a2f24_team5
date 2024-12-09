## Data Collection and preprocessing

### 1. Data Collection

The data we used for this projects are obtained from Kaggle:

- livecareer: <https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset>
- IT departments: <https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset>

Our dataset, comprising over 3,300 resumes, was collected from Kaggle. The livecareer dataset provide string as well as PDF formated data with ID, Resume_str, Resume_html and Category. PDF stored in the data folder differentiated into their respective labels as folders with each resume residing inside the folder in pdf form with filename as the id defined in the csv. The IT departments dataset, available in CSV format, contains category and resume.

### 2. Preprocessing

In the preprocessing, two distinct datasets were merged into a unified structure to facilitate efficient data analysis and model training. At the end of this process, a CSV file is created with the following columns (`category`, and `resume_string`). The data in it has the following format

| category                                 | resume_string   |
|------------------------------------------|-----------------|
| A category label describing the job role | The resume text |

## System Architecture

Below is an overview of our system workflow, including how we use the combination of AI and RAG to enhance the process of resume analysis and specific system features.

### 1. Workflow Diagram

![LLM diagram](./images/LLM%20diagram.png)

#### Description of the Workflow

User Interface (UI): Users interact with the system through the UI, where they can upload prompts and then ask for resume evaluation and interview preparation.

LLM (Large Language Model): Users' prompt is filtered and delivered to the LLM. Then the LLM will expand the initial prompt into a more detailed query.

Data Source: This component represents external databases where our preprocessed resume dataset is stored.

Find Relevant Context: The system searches resumes stored in our database to find relevant context that enhances the understanding of the input query.

Send to UI: The final response, which includes corresponding resume evaluation, modification suggestions, interview simulation, etc. according to the user's needs, is sent back to the user interface for the user's review.

### 2. Backend Diagram

![Backend diagram](./images/Backend%20diagram.png)

#### Basic Functionality

- Resume evaluation
- Suggestions for improvement
- Interview question generation
- Project recommendations

## Inference and Result

### 1. Evaluation

### 2. Result
