from functions import call_llm
def generate_response(context, user_query):
    prompt = f"""
            You are a helpful AI assistant.

            Use ONLY the provided document context.

            When answering, cite the chunk numbers like:

            Example:
            "The company revenue increased by 20% [Chunk 3]"

            If information is taken from multiple chunks:

            "... [Chunk 3, Chunk 7]"

            If answer is not found, say:

            "I could not find that information in the uploaded document."

            Document Context:
            {context}

            Question:
            {user_query}
        
            Answer:
        """
    answer = call_llm(prompt)
    return answer