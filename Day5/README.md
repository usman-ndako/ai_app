# AI Document Summarizer API

Professional document summarization API with context-aware tone control and fact-grounding.

## 🚀 Features

- **5 Summary Types:** Standard, Executive, Legal, Technical, Financial
- **Context-Aware:** Each type uses appropriate tone and focus
- **Anti-Hallucination:** AI strictly uses only information from source document
- **Enterprise-Ready:** Error handling, performance metrics, validation
- **Fast Performance:** Sub-second processing for most documents

## 📋 Business Use Cases

| Summary Type | Target Users | Use Case |
|--------------|--------------|----------|
| **Executive** | C-Suite, VPs | Strategic decisions, key metrics, ROI |
| **Legal** | Legal Teams | Contract analysis, obligations, deadlines |
| **Technical** | Engineers, IT | System specs, performance, recommendations |
| **Financial** | Finance Teams | Revenue, expenses, metrics, percentages |
| **Standard** | General Users | Balanced summaries for any document |

## 🔧 Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Start API server
uvicorn summarizer_api:app --reload