def Arxiv(user_input):    
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema.output_parser import StrOutputParser
    from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
    from langchain.utilities import DuckDuckGoSearchAPIWrapper
    import requests
    from bs4 import BeautifulSoup
    from langchain.retrievers import ArxivRetriever
    import json
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    # Initialize Groq and OpenAI models
    llm = ChatOpenAI()
    retriever = ArxivRetriever()

    SUMMARY_TEMPLATE = """{text} 
    -----------
    Using the above text, answer in short the following question: 
    > {question}
    -----------
    if the question cannot be answered using the text, imply summarize the text. Include all factual information, numbers, stats etc if available.""" 

    SUMMARY_PROMPT = ChatPromptTemplate.from_template(SUMMARY_TEMPLATE)

    def scrape_text(url: str):
        try:
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                page_text = soup.get_text(separator=" ",strip=True)
                return page_text
            else:
                return f"Failed to retrieve the webpage: Status code {response.status_code}"
        
        except Exception as e:
            print(e)
            return f"Failed to retrieve the webpage: {e}"
    


    SUMMARY_TEMPLATE = """{doc} 
    -----------
    Using the above text, answer in short the following question: 
    > {question}
    -----------
    if the question cannot be answered using the text, imply summarize the text. Include all factual information, numbers, stats etc if available.""" 

    SUMMARY_PROMPT = ChatPromptTemplate.from_template(SUMMARY_TEMPLATE)


    scrape_and_summarize_chain = RunnablePassthrough.assign(
        
        summary = SUMMARY_PROMPT | llm| StrOutputParser()
    ) | (lambda x:f"Title: {x['doc'].metadata['Title']}\n\nSUMMARY: {x['summary']}")


    web_search_chain = RunnablePassthrough.assign( 
        
        docs =lambda x: retriever.get_summaries_as_docs(x["question"])

    ) | (lambda x: [{"question": x["question"], "doc":u} for u in x["docs"]]) |  scrape_and_summarize_chain.map()


    SEARCH_PROMPT = ChatPromptTemplate.from_messages(
        [
            (
                "user",
                "Write 3 google search queries to search online that form an "
                "objective opinion from the following: {question}\n"
                "You must respond with a list of strings in the following format: "
                '["query 1", "query 2", "query 3"].',
            ),
        ]
    )

    search_question_chain = SEARCH_PROMPT | llm | StrOutputParser() | json.loads

    full_research_chain = search_question_chain | (lambda x: [{'question': i} for i in x])| web_search_chain.map()

    RESEARCH_REPORT_TEMPLATE = """Information:
    --------
    {research_summary}
    --------
    Using the above information, answer the following question or topic: "{question}" in a detailed report -- \
    The report should focus on the answer to the question, should be well structured, informative, \
    in depth, with facts and numbers if available and a minimum of 1,200 words.
    You should strive to write the report as long as you can using all relevant and necessary information provided.
    You must write the report with markdown syntax.
    You MUST determine your own concrete and valid opinion based on the given information. Do NOT deter to general and meaningless conclusions.
    Write all used source urls at the end of the report, and make sure to not add duplicated sources, but only one reference for each.
    You must write the report in apa format.
    Please do your best, this is very important to my career."""  

    WRITER_SYSTEM_PROMPT = "You are an AI critical thinker research assistant. Your sole purpose is to write well written, critically acclaimed, objective and structured reports on given text." 

    prompt = ChatPromptTemplate.from_messages(      
        [
            ("system", WRITER_SYSTEM_PROMPT),
            ("user", RESEARCH_REPORT_TEMPLATE)          


        ]
    )


    def collapse_list_of_lists(lists_of_lists):
        content = []
        for l in lists_of_lists:
            content.append("\n\n".join(l))
        return "\n\n".join(content)    


    chain = RunnablePassthrough.assign(
    research_summary = full_research_chain | collapse_list_of_lists

    ) | prompt | llm | StrOutputParser()



    # #!/usr/bin/env python
    # from fastapi import FastAPI
    # from langserve import add_routes

    # app = FastAPI(
    #     title="LangChain Server",
    #     version="1.0",
    #     description="A simple api server using Langchain's Runnable interfaces",
    # )

    # add_routes(
    #     app,
    #     chain,
    #     path="/research-assistant"
    # )


    # if __name__ == "__main__":
    #     import uvicorn

    #     uvicorn.run(app, host="localhost", port=8000)

    results=chain.invoke({"question":user_input})


    with open("reports/research_arxiv.txt","w",encoding='utf-8') as file:
        file.write(results)


    return results   






