import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from arxiv_groq import Arxiv
from duckduckgo_groq import duckduckgo
import os
#from youtube_groq import youtube_search

# Load environment variables from .env
load_dotenv()


def is_folder_empty(folder_path):
    return not any(os.scandir(folder_path))


# Enhanced prompt template
RESEARCH_SUMMARY_TEMPLATE = """
# Research Summary Report

## Instructions:
You are provided with research information from two sources: DuckDuckGo and arXiv. 
Your task is to **fully integrate all information** from these sources into a detailed and professional final report. 
Ensure factual accuracy and use Markdown for structure.

---

### DuckDuckGo Report:
{duckduckgo_report}

---

### arXiv Report:
{arxiv_report}


---

## Requirements:
1. **Incorporate every detail** without skipping any part.
2. **Use Markdown syntax** with headings and bullet points.
3. **Follow APA format** for citations and URLs.
4. **Aim for a minimum of 1,200 words**.
5. **Include an introduction, body sections, and a conclusion.**

---

"""

def generate_research_report(user_query):
    #Format the prompt with reports
    if not is_folder_empty("reports"):

        with open("reports/research_duckduckgo.txt","r") as file:
            duckduckgo_report = file.read()
        with open("reports/research_arxiv.txt","r") as file:
            arxiv_report = file.read()   
        with open("reports/research_youtube.txt","r") as file:
            youtube_report = file.read()     

        formatted_prompt = RESEARCH_SUMMARY_TEMPLATE.format(
                duckduckgo_report=duckduckgo_report,
                arxiv_report=arxiv_report
        )

        # Create the system message and ChatOpenAI model
        system_prompt = (
            "You are an AI assistant tasked with writing comprehensive research reports. "
            "Make sure every detail from the input is included accurately."
        )

        # Create the ChatPromptTemplate
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("user", formatted_prompt)])

        # Initialize LLM and parser
        llm = ChatOpenAI(model="gpt-3.5-turbo")
        parser = StrOutputParser()
        chain = prompt | llm | parser

        # Invoke the model to generate the final report
        result = chain.invoke({"input": ""})
        result = result + "\nRelavant YouTube links:\n" + youtube_report

        with open("reports/final_reprot.md", "w") as file:
                file.write(result)
        return result 
