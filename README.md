# Mini GPT Researcher


![Mini-gpt-researcher](https://github.com/Dorcatz123/Mini-gpt-researcher/blob/main/mini-gpt-researcher.jpg)



**Mini GPT Researcher** is an interactive desktop application powered by GPT-3.5, which generates comprehensive research reports by querying information from sources like DuckDuckGo, arXiv, and YouTube. The app combines AI and information retrieval to assist users in producing detailed, structured reports based on their queries. This project was built motivated by the famous gpt researcher whose link is here: https://github.com/assafelovic/gpt-researcher

## Features

- **Query Research Information**: Users can input a research question, and the app fetches relevant information from multiple sources.
- **Multiple Sources Integration**: Combines data from DuckDuckGo and YouTube (API key required for now).
- **Automatic Report Generation**: Integrates collected data into a Markdown-formatted research report.
- **Save Reports**: Save generated reports to a file with Markdown support.
- **User-Friendly UI**: Built with PyQt5, the app has an intuitive interface.
- **Link-Enabled Reports**: Displays clickable links within reports for easy reference.

## Screenshots


## Requirements

- **Python 3.10**
- API keys for:
  - **OpenAI GPT**: Used for generating content.
  - **DuckDuckGo, arXiv, and YouTube**: For fetching research data.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/mini-gpt-researcher.git
   cd mini-gpt-researcher
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API Keys**:
   The app will let you easily input your API keys.

## Usage

1. **Run the App**:
   ```bash
   python main.py
   ```

2. **Query a Research Topic**:
   - Open the app and enter a research question.
   - Click **Generate Report** to start the process.

3. **Save Reports**:
   - After the report is generated, click **Save Report** to save it as a Markdown file.

## File Structure

- `main.py`: Main entry point for the app.
- `researcher.py`: Contains the core research functions and logic.
- `arxiv_groq.py`, `duckduckgo_groq.py`: Modules for fetching data from respective sources.
- `ui/`: Contains .ui files and style sheets for UI customization.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you find a bug or have suggestions.

## History of the Mini-gpt researcher

-A project initiated by Akshay P R.

**Key Milestones**:
-[09 2024]: Initial concept and prototype developed.
-As we bring in more contributors, the project remains rooted in its mission to provide accessible and reliable information backed by links to the source documents.

## License

This project is licensed under the MIT License.

---

