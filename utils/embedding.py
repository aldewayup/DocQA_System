from sentence_transformers import SentenceTransformer, util
import chromadb

def split_text_to_chunks(text, max_tokens=256):
    """
    Split text into chunks based on a maximum token count.

    Args:
    text (str): The input text to be split.
    max_tokens (int): The maximum number of tokens per chunk. Defaults to 256.

    Returns:
    list: A list of text chunks, each containing no more than max_tokens.
    """
    from nltk.tokenize import sent_tokenize
    
    # Split the text into sentences
    sentences = sent_tokenize(text)
    chunks = []
    chunk = []
    total_tokens = 0
    
    for sentence in sentences:
        # Count tokens in the current sentence (approximated by word count)
        sentence_tokens = len(sentence.split())
        
        # If adding this sentence exceeds the max_tokens, start a new chunk
        if total_tokens + sentence_tokens > max_tokens:
            chunks.append(' '.join(chunk))
            chunk = [sentence]
            total_tokens = sentence_tokens
        else:
            chunk.append(sentence)
            total_tokens += sentence_tokens
    
    # Add the last chunk if it's not empty
    if chunk:
        chunks.append(' '.join(chunk))
    
    return chunks

def create_vector_store(documents, embedding_model):
    """
    Create a vector store from a list of documents using ChromaDB.

    Args:
    documents (list): A list of dictionaries, each containing document text and metadata.
    embedding_model: A SentenceTransformer model for creating embeddings.

    Returns:
    chromadb.Collection: A ChromaDB collection containing the vectorized documents, or None if an error occurs.
    """
    try:
        # Initialize ChromaDB client
        client = chromadb.Client()
        collection = client.create_collection("documents")
        
        for doc in documents:
            # Combine main text and text from images
            combined_text = doc['text'] + " " + doc['images_text']
            
            if combined_text.strip():
                # Split the combined text into chunks
                chunks = split_text_to_chunks(combined_text)
                embeddings = []
                ids = []
                
                # Create embeddings for each chunk
                for i, chunk in enumerate(chunks):
                    embedding = embedding_model.encode(chunk).tolist()  # Convert numpy array to list
                    embeddings.append(embedding)
                    ids.append(f"{doc['file_name']}_chunk_{i}")
                
                # Add chunks, embeddings, and metadata to the collection
                collection.add(
                    documents=[chunk for chunk in chunks],
                    metadatas=[{'file_name': doc['file_name']}] * len(chunks),
                    ids=ids,
                    embeddings=embeddings
                )
            else:
                print(f"Warning: Document '{doc['file_name']}' is empty or contains only stop words. Skipping.")
        
        return collection
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return None
