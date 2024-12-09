import pandas as pd
import uuid
import openai
from tqdm import tqdm
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Set your OpenAI API key
client = openai.OpenAI(api_key='') 

# Set your Qdrant instance details
qdrant_url = ''# Replace with your Qdrant URL
qdrant_api_key = ''           # Replace with your Qdrant API key

qdrant_client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key,
)

collection_name = 'Resume_Analysis'

# Step 1: Read the CSV file and generate unique IDs
df = pd.read_csv('resume_10_test_with_scores.csv', delimiter=',', encoding='utf-8')  # Adjust the delimiter if needed

# Generate unique IDs
df['id'] = [str(uuid.uuid4()) for _ in range(len(df))]

# Convert DataFrame to a list of dictionaries
data = df.to_dict(orient='records')
print(data)

# Step 2: Vectorize the 'Resume' text
def get_embedding(text, model="text-embedding-ada-002"):
    response = client.embeddings.create(
        model=model,
        input=text
    )
    embedding = response.data[0].embedding
    return embedding

# Step 3: Prepare data for upload
points = []
for item in tqdm(data, desc="Processing resumes"):
    text = item['Resume']
    vector = get_embedding(text)
    point = {
        'id': item['id'],
        'vector': vector,
        'payload': {
            'Category': item.get('Category'),
            'Scores': {
                'Relevance of Job Description_Score': item.get('Relevance of Job Description_Score'),
                'Achievements and Impact_Score': item.get('Achievements and Impact_Score'),
                'Education and Certifications_Score': item.get('Education and Certifications_Score'),
                'Resume Structure and Presentation_Score': item.get('Resume Structure and Presentation_Score'),
                'Soft Skills_Score': item.get('Soft Skills_Score'),
                'Consistency and Chronology_Score': item.get('Consistency and Chronology_Score'),
                'Weighted_Score': item.get('Weighted_Score')
            },
            'Explanation': item.get('Explanation')
        }
    }
    points.append(point)


'''
# Step 4: Create or recreate the collection
embedding_size = len(points[0]['vector'])  # Typically 1536 for 'text-embedding-ada-002'

qdrant_client.recreate_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=embedding_size,
        distance=models.Distance.COSINE
    )
)
'''

# Step 5: Upload data to Qdrant
batch_size = 100
for i in tqdm(range(0, len(points), batch_size)):
    batch = points[i:i+batch_size]
    qdrant_client.upsert(
        collection_name=collection_name,
        points=batch
    )

print("Data successfully uploaded to Qdrant!")
