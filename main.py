from utils.config import load_config, setup_tesseract
from utils.document_processing import process_documents
from utils.embedding import create_vector_store
from utils.search import hybrid_search, re_rank_documents
from utils.qa import get_answer_from_documents, find_page_number
from utils.excel import save_to_excel
from sentence_transformers import SentenceTransformer
import os
import openai

def main():
    """The main function."""
    try:
        print("Welcome to DocQA System\n")
        config = load_config()
        openai.api_key = config.get('openai_api_key')
        setup_tesseract(config)

        documents_path = input(f"Enter the path to the documents (default: {config.get('documents_path', './documents/')}): ").strip()
        if not documents_path:
            documents_path = config.get('documents_path', './documents/')
        print("\n")
        processed_documents_file = config.get('processed_documents_path', './processed_documents.json')
        documents = process_documents(documents_path, processed_documents_file)

        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        collection = create_vector_store(documents, embedding_model)

        qa_data = []
        queries = []
        print("\nEnter your queries (type 'done' to finish):")
        while True:
            query = input("Query: ")
            if query.lower() == 'done':
                break
            queries.append(query)

        print("\nProcessing queries...\n")

        for i, query in enumerate(queries):
            combined_results, combined_metadatas, combined_ids = hybrid_search(query, collection, embedding_model)
            most_relevant_document = re_rank_documents(query, combined_results, config.get('gpt_model', 'gpt-4'))
            if isinstance(most_relevant_document, list):
                most_relevant_document = ' '.join(most_relevant_document)
            answer = get_answer_from_documents(query, most_relevant_document, config.get('gpt_model', 'gpt-4'))
            if any(phrase.lower() in answer.lower() for phrase in ["the document does not provide information", "no information found", "not available"]):
                source_file = "None"
                page_number = "None"
            else:
                source_file = combined_metadatas[0][0]['file_name']
                page_number = find_page_number(query, next((doc['page_texts'] for doc in documents if doc['file_name'] == source_file), []))
            qa_data.append([i + 1, query, answer, source_file, page_number])

            # Display the results on the CLI
            print(f"Query: {query}")
            print(f"Answer: {answer}")
            print(f"Source file: {source_file}")
            print(f"Page number: {page_number}")
            print("\n" + "-"*50 + "\n")

        output_folder_path = input(f"\nEnter the folder path for the output Excel file (default: {os.path.dirname(config.get('output_excel_path', './query_answers.xlsx'))}): ").strip()
        if not output_folder_path:
            output_folder_path = os.path.dirname(config.get('output_excel_path', './query_answers.xlsx'))
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)
        output_excel_path = os.path.join(output_folder_path, os.path.basename(config.get('output_excel_path', './query_answers.xlsx')))
        
        save_to_excel(qa_data, output_excel_path)
        print(f"\nResults have been saved to {output_excel_path}")

    except Exception as e:
        print(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main()
