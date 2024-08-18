import openai
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer, util
import torch

def get_answer_from_documents(query, document, gpt_model):
    """
    Get an answer to a query based on the provided document using GPT model.

    Args:
    query (str): The question to be answered.
    document (str): The document content to be used as context.
    gpt_model (str): The name of the GPT model to use.

    Returns:
    str: The generated answer or an error message if generation fails.
    """
    try:
        # Construct the prompt for the GPT model
        prompt = f"Please provide a concise and specific answer to the following question based on the provided document:\nQuestion: {query}\nDocument: {document}\nAnswer:"
        
        # Make an API call to OpenAI
        response = openai.ChatCompletion.create(
            model=gpt_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150  # Limit the response length
        )
        
        # Extract and return the generated answer
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error getting answer from documents: {e}")
        return "Unable to generate an answer due to an error."

def find_page_number(query, page_texts):
    """
    Find the page number of the best matching page for the given query.

    Args:
    query (str): The query to match against page texts.
    page_texts (list): A list of tuples containing (page_number, page_text).

    Returns:
    int: The page number of the best matching page, or None if an error occurs.
    """
    try:
        # Tokenize the query and remove common question words
        query_tokens = word_tokenize(query)
        query_tokens = [token for token in query_tokens if token.lower() not in ['what', 'where', 'when', 'who', 'why', 'how']]
        query = ' '.join(query_tokens)
        
        # Load the sentence transformer model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Encode the query and page texts
        query_embedding = model.encode(query)
        page_embeddings = model.encode([page_text for page_num, page_text in page_texts])
        
        # Calculate cosine similarity between query and page embeddings
        cos_scores = util.cos_sim(query_embedding, page_embeddings)
        
        # Find the index of the highest similarity score
        max_index = torch.argmax(cos_scores)
        
        # Return the page number of the best matching page
        return page_texts[max_index][0]
    except Exception as e:
        print(f"Error finding page number: {e}")
        return None
