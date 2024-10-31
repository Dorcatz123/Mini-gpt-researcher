def duckduckgo(user_input):    
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema.output_parser import StrOutputParser
    from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
    from langchain.utilities import DuckDuckGoSearchAPIWrapper
    import requests
    from bs4 import BeautifulSoup
    import json
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    # Initialize Groq and OpenAI models
    
    llm_openai = ChatOpenAI()

    # DuckDuckGo Search API Wrapper
    ddg_search = DuckDuckGoSearchAPIWrapper()

    # Function to perform web search
    def web_search(query: str, num_results: int = 5):
        results = ddg_search.results(query, num_results)
        return [r["link"] for r in results]

    # Function to scrape text from a URL
    def scrape_text(url: str):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                return soup.get_text(separator=" ", strip=True)
            else:
                return f"Failed to retrieve: Status code {response.status_code}"
        except Exception as e:
            return f"Error retrieving webpage: {e}"

    # Summary template and prompt
    SUMMARY_TEMPLATE = """{text} 
    -----------
    Answer this question briefly: 
    > {question}
    -----------
    If not possible, summarize the content, including all available facts and stats.
    """

    SUMMARY_PROMPT = ChatPromptTemplate.from_template(SUMMARY_TEMPLATE)

    # Web scraping and summarization chain
    scrape_and_summarize_chain = (
        RunnablePassthrough.assign(
            summary=RunnablePassthrough.assign(
                text=lambda x: scrape_text(x["url"])[:1000]  # Limit to 1000 characters
            ) | SUMMARY_PROMPT | llm_openai | StrOutputParser()
        ) | (lambda x: f"URL: {x['url']}\n\nSUMMARY: {x['summary']}")
    )

    # Web search chain
    web_search_chain = (
        RunnablePassthrough.assign(
            urls=lambda x: web_search(x["question"])
        ) | (lambda x: [{"question": x["question"], "url": u} for u in x["urls"]]) 
        | scrape_and_summarize_chain.map()
    )

    # Search query generation prompt
    SEARCH_PROMPT = ChatPromptTemplate.from_template(
        'Generate 3 Google search queries on the following topic: "{question}". '
        'Respond with: ["query 1", "query 2", "query 3"].'
    )

    # Search query chain
    search_question_chain = SEARCH_PROMPT | llm_openai | StrOutputParser() | json.loads



    # Full research chain
    full_research_chain = (
        search_question_chain | (lambda x: [{'question': q} for q in x]) | web_search_chain.map()
    )

    # Report template
    RESEARCH_REPORT_TEMPLATE = """
    # Research Report

    ## Information:
    --------
    {research_summary}
    --------

    Based on the above, write a detailed report addressing: "{question}".
    - Focus on facts, structure, and in-depth insights. 
    - Include data and statistics if available. Aim for 1,200+ words.
    - Use Markdown syntax and follow APA format for citations.
    - Provide URLs used, avoiding duplication.

    This report is critical for my career, so ensure it is professional and thorough.
    """

    # System prompt for Groq
    WRITER_SYSTEM_PROMPT = (
        "You are an AI assistant tasked with writing detailed and structured reports. "
        "Incorporate all provided information without missing anything. Use APA format and Markdown."
    )

    # Create the Groq-compatible prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", WRITER_SYSTEM_PROMPT),
        ("user", RESEARCH_REPORT_TEMPLATE)
    ])

    # Utility function to merge nested lists into a single string
    def collapse_list_of_lists(lists_of_lists):
        return "\n\n".join("\n\n".join(lst) for lst in lists_of_lists)

    # Final chain to generate the report using Groq
    chain = (
        RunnablePassthrough.assign(
            research_summary=full_research_chain | collapse_list_of_lists
        ) | prompt | llm_openai | StrOutputParser()
    )

    # Invoke the chain with user input
    results = chain.invoke(
        {"question": user_input}
    )

    # Save the report
    with open("reports/research_duckduckgo.txt", "w", encoding='utf-8') as file:
        file.write(results)

    return results





