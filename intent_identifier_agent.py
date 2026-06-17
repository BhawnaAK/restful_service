from functions import call_llm
def identify_intent(user_query):
    prompt=f"""
        You are an intent classification agent for an HR chatbot.

        Your job is to determine which vector database should be queried to answer the user's question.

        Available vector databases:

        1. benefits_policy
        Topics include:
        - Health insurance
        - Maternity leave
        - Paternity leave
        - Wellness allowance
        - Gym reimbursement
        - Employee assistance programs
        - Employee benefits and perks

        2. employee_handbook
        Topics include:
        - Working hours
        - Leave policy
        - Casual leave
        - Sick leave
        - Probation period
        - Remote work policy
        - Code of conduct
        - Notice period
        - General employee rules and policies

        3. travel_policy
        Topics include:
        - Business travel
        - Flight booking
        - Hotel reimbursement
        - Meal allowance
        - Taxi reimbursement
        - Travel expenses
        - Travel approvals

        4. extra
        Use this when the user question is NOT related to HR policies, HR benefits, employee rules, or travel-related company policies.

        This includes:
        - General knowledge questions (e.g., science, history, coding, math)
        - Personal advice unrelated to workplace HR policies
        - Greetings or casual conversation
        - Anything outside company HR documents
        - Ambiguous questions that do not match any of the above categories

        Examples:

        User: How many sick leaves do I get?
        Output: employee_handbook

        User: Can I work remotely?
        Output: employee_handbook

        User: How much is the meal allowance during travel?
        Output: travel_policy

        User: Do employees get health insurance?
        Output: benefits_policy

        User: How many days of maternity leave are provided?
        Output: benefits_policy

        User: What is the capital of France?
        Output: extra

        User: Write a Python function for sorting a list
        Output: extra

        User: Hi
        Output: extra

        Instructions:
        - Choose exactly ONE value.
        - Select the most relevant database if the question is HR-related.
        - Use "extra" ONLY when the question is not related to HR policies or company HR knowledge.
        - Do not explain reasoning.
        - Do not output sentences or JSON.
        - Output only one of:

        benefits_policy
        employee_handbook
        travel_policy
        extra

        This is the User Query:
        {user_query}

    """
    answer = call_llm(prompt)
    return answer