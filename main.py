import sys
import warnings
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextBrowser, QTextEdit, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QLineEdit
)
from PyQt5.QtCore import QThread, pyqtSignal
from arxiv_groq import Arxiv
from duckduckgo_groq import duckduckgo
from researcher import generate_research_report
from youtube_groq import youtube_search
from dotenv import load_dotenv, set_key

warnings.filterwarnings("ignore", category=DeprecationWarning)

class Worker(QThread):
    update_signal = pyqtSignal(str)  # Signal to send updates to the main thread

    def __init__(self, query):
        super().__init__()
        self.query = query

    def run(self):
        """Run the research tasks in a separate thread."""
        try:
            self.update_signal.emit("🔍 Initializing DuckDuckGo 🦆...")
            duckduckgo_report = duckduckgo(self.query)
            
            #self.update_signal.emit(duckduckgo_report)
            self.update_signal.emit("✅ DuckDuckGo report fetched successfully!")

        except Exception as e:
            self.update_signal.emit(f"❌ Error: {str(e)}")

        try:        

            self.update_signal.emit("🔍 Initializing arXiv 📚...")
            arxiv_report = Arxiv(self.query)
            
            #self.update_signal.emit(arxiv_report)
            self.update_signal.emit("✅ arXiv report fetched successfully!")

        except Exception as e:
            self.update_signal.emit(f"❌ Error: {str(e)}")    

        try:    

            self.update_signal.emit("🔍 Initializing youtube 😎 ...")
            youtube_report = youtube_search(self.query)
            
            #self.update_signal.emit(youtube_report)
            self.update_signal.emit("✅ youtube report fetched successfully!")

        except Exception as e:
            self.update_signal.emit(f"❌ Error: {str(e)}")

        try:     

            self.update_signal.emit("🚀 Finalizing report...")
            final_report = generate_research_report(self.query)
                            
            self.update_signal.emit("✅ Final report generated successfully!")
            self.update_signal.emit("📄 Final report ready.")
            self.update_signal.emit(final_report)  # Emit the final report
        except Exception as e:
            self.update_signal.emit(f"❌ Error: {str(e)}")    
            

            


        except Exception as e:
            self.update_signal.emit(f"❌ Error: {str(e)}")

    def format_links(self, text):
        """Format any URLs in the text as clickable HTML links."""
        import re
        url_pattern = re.compile(r"(https?://[^\s]+)")
        formatted_text = re.sub(
            url_pattern, r'<a href="\1">\1</a>', text
        )
        return formatted_text            


class ResearcherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini GPT Researcher")

        # Create widgets
        self.result_output = QTextBrowser(self)
        self.result_output.setReadOnly(True)
        
        self.result_output.setOpenExternalLinks(True)  # Enable opening links in the browser

        self.query_input = QTextEdit(self)
        self.query_input.setPlaceholderText("Enter your research question...")


        self.generate_button = QPushButton("Generate Report")
        self.save_button = QPushButton("Save Report")

        # API key input fields
        self.openai_key_input = QLineEdit(self)
        self.openai_key_input.setPlaceholderText("Enter OpenAI API Key")
        self.openai_key_input.setEchoMode(QLineEdit.Password) 
        self.youtube_key_input = QLineEdit(self)
        self.youtube_key_input.setPlaceholderText("Enter YouTube API Key: \nCheck the readme on how to get your YouTube API key:")
        self.youtube_key_input.setEchoMode(QLineEdit.Password) 


        # Save Keys Button
        self.save_keys_button = QPushButton("Save API Keys")
        self.save_keys_button.clicked.connect(self.save_api_keys)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.query_input)
        layout.addWidget(self.openai_key_input)
        layout.addWidget(self.youtube_key_input)
        layout.addWidget(self.save_keys_button)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.result_output)
        layout.addWidget(self.save_button)
        

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        

         # Connect buttons to functions
        self.generate_button.clicked.connect(self.generate_report)
        self.save_button.clicked.connect(self.save_report)
       

    def save_api_keys(self):
        """Save API keys to .env file."""
        openai_key = self.openai_key_input.text().strip()
        youtube_key = self.youtube_key_input.text().strip()
     

        # Save each key if it's not empty
        if openai_key:
            set_key('.env', 'OPENAI_API_KEY', openai_key)
        if youtube_key:
            set_key('.env', 'YOUTUBE_API_KEY', youtube_key)
        

        QMessageBox.information(self, "Success", "API keys saved successfully!")



   
    

    def generate_report(self):
        """Generate the research report based on user input."""
        query = self.query_input.toPlainText().strip()
        if query:
            self.result_output.clear()  # Clear previous output
            self.worker = Worker(query)  # Create the worker with the query
            self.worker.update_signal.connect(self.update_output)  # Connect the signal to the output method
            self.worker.start()  # Start the worker thread
        else:
            QMessageBox.warning(self, "Warning", "Please enter a research question.")

    def update_output(self, message):
        """Update the result output text area with messages from the worker."""
        if "Final Report:" in message:
            # If the message contains the final report, set it as HTML
            self.result_output.setHtml(message)  # Display the final report as HTML
        else:
            # Otherwise, append the message as text
            self.result_output.append(message)

    def save_report(self):
        """Save the generated report as a Markdown file."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Report", "", "Markdown Files (*.md);;All Files (*)", options=options
        )
        if file_path:
            try:
                with open(file_path, 'w',encoding='utf-8') as f:
                    f.write(self.result_output.toPlainText())
                QMessageBox.information(self, "Success", "Report saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save report: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResearcherApp()
    window.show()
    sys.exit(app.exec_())
