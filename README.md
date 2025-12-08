# LLM Citation Machine

An AI-powered citation generator that automatically extracts metadata from websites and generates accurate MLA and APA citations using Google Gemini.

## Live Version
[https://llm-citation-machine.streamlit.app/](https://llm-citation-machine.streamlit.app/)

## Features

- 🤖 **AI-Powered Extraction**: Uses Google Gemini to intelligently extract citation metadata from web pages
- 📚 **Multiple Formats**: Supports both MLA and APA citation styles
- 🌐 **Web Interface**: Clean Streamlit-based UI for easy citation generation
- 🔍 **Smart Content Extraction**: Uses Playwright and Trafilatura to fetch and parse web content
- 📋 **Batch Processing**: Generate multiple citations at once from multiple URLs

## Installation

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Luke-Pitstick/llm-citation-machine.git
cd llm-citation-machine
```

2. Install dependencies:
```bash
uv sync
# or
pip install -e .
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

4. Set up environment variables:
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

You can get a Google API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

## Usage

### Web Interface (Recommended)

Launch the Streamlit web interface:

```bash
streamlit run src/main_interface.py
```

The interface will open in your browser at `http://localhost:8501`.

**Steps:**
1. Enter one or more website URLs (one per line) in the text area
2. Select your preferred citation style (MLA or APA)
3. Click "Generate Citation"
4. View the formatted citations and copy them as needed
5. Expand "View Extracted Metadata" to see the raw citation information extracted by the AI

### Command Line Usage

You can also use the citation generator programmatically:

```python
from src.citation import generate_citations

urls = [
    "https://example.com/article",
    "https://another-site.com/research"
]

# Generate MLA citations
citations, info_list = generate_citations(urls, "MLA")

# Generate APA citations
citations, info_list = generate_citations(urls, "APA")

# Print citations
for citation in citations:
    print(citation)
```

### Individual Citation Functions

For more control, you can use the individual citation functions:

```python
from src.citation import generate_mla_citation, generate_apa_citation

# Generate MLA citation
citation, info = generate_mla_citation("https://example.com/article")
print(citation)

# Generate APA citation
citation, info = generate_apa_citation("https://example.com/article")
print(citation)
```

## How It Works

1. **Web Scraping**: Uses Playwright to fetch the full HTML content of the website (including JavaScript-rendered content)
2. **Content Extraction**: Trafilatura extracts clean text content from the HTML
3. **AI Extraction**: Google Gemini analyzes the content and extracts structured citation metadata (authors, title, publication date, DOI, etc.)
4. **Citation Formatting**: The extracted metadata is formatted according to MLA or APA style guidelines

## Citation Formats

### MLA Format
- Author names (Last, First)
- Article title in quotes
- Publication title in italics
- Volume, issue, publication date
- Page range
- DOI (if available)

### APA Format
- Author names (Last, First Initial)
- Publication year in parentheses
- Article title
- Publication title in italics
- Volume and issue
- Page range or article number
- DOI link

## Configuration

### Streamlit Configuration

Streamlit settings can be customized in `.streamlit/config.toml`:
- Theme settings
- Browser settings
- Server configuration

### BAML Configuration

The AI extraction logic is configured in `baml_src/citation.baml`. You can:
- Modify the extraction prompt
- Adjust the citation formatting
- Add new citation styles

## Dependencies

- **baml-py**: BAML framework for LLM interactions
- **streamlit**: Web interface framework
- **playwright**: Browser automation for web scraping
- **trafilatura**: HTML content extraction
- **langchain**: LLM integration utilities
- **python-dotenv**: Environment variable management

## Troubleshooting

### Common Issues

1. **"Failed to extract content" error**
   - The website may be blocking automated access
   - Try a different URL or check if the site requires authentication

2. **API Key errors**
   - Ensure your `GOOGLE_API_KEY` is set in the `.env` file
   - Verify the API key is valid and has sufficient quota

3. **Playwright browser errors**
   - Run `playwright install chromium` to ensure browsers are installed
   - Check that you have the necessary system dependencies

## License

[Add your license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
