from sentence_transformers import util
import torch

def hybrid_search(query, collection, embedding_model):
    """
    Perform a hybrid search combining dense and sparse retrieval methods.

    Args:
    query (str): The search query.
    collection: The ChromaDB collection to search in.
    embedding_model: The model used to create embeddings.

    Returns:
    tuple: Three lists containing combined results, metadatas, and ids.
           Returns empty lists if an error occurs.
    """
    try:
        # Create an embedding for the query
        query_embedding = embedding_model.encode(query).tolist()  # Convert numpy array to list
        
        # Perform dense retrieval (using embeddings)
        dense_results = collection.query(query_embeddings=[query_embedding], n_results=10)
        
        # Perform sparse retrieval (using text)
        sparse_results = collection.query(query_texts=[query], n_results=10)
        
        # Combine results from both methods
        combined_results = dense_results['documents'] + sparse_results['documents']
        combined_metadatas = dense_results['metadatas'] + sparse_results['metadatas']
        combined_ids = dense_results['ids'] + sparse_results['ids']
        
        return combined_results, combined_metadatas, combined_ids
    except Exception as e:
        print(f"Error performing hybrid search: {e}")
        return [], [], []

def re_rank_documents(query, documents, gpt_model):
    """
    Re-rank documents based on their relevance to the query using GPT model.

    Args:
    query (str): The search query.
    documents (list): List of documents to re-rank.
    gpt_model (str): The name of the GPT model to use.

    Returns:
    str: The most relevant document after re-ranking.
         Returns the first document or an empty string if an error occurs.
    """
    import openai
    try:
        ranked_documents = []
        for doc in documents:
            # Create a prompt for the GPT model to rank document relevance
            prompt = f"Rank the relevance of the following document to the query:\nQuery: {query}\nDocument: {doc}\nRelevance (0-10):"
            
            # Make an API call to OpenAI
            response = openai.ChatCompletion.create(
                model=gpt_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1  # We only need a single number as response
            )
            
            # Extract the relevance score from the response
            relevance_score = int(response.choices[0].message['content'].strip())
            ranked_documents.append((doc, relevance_score))
        
        # Sort documents based on relevance score in descending order
        ranked_documents.sort(key=lambda x: x[1], reverse=True)
        
        # Return the most relevant document
        return ranked_documents[0][0]
    except Exception as e:
        print(f"Error re-ranking documents: {e}")
        return documents[0] if documents else ""
