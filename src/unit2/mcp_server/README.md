---
title: Text Sentiment Analysis
emoji: 😊
colorFrom: blue
colorTo: green
sdk: gradio
python_version: 3.11
app_file: app.py
short_description: Analyze text sentiment
tags:
    - sentiment-analysis
    - textblob
    - nlp
    - text-analysis
---

# Text Sentiment Analysis

This project provides a simple web interface for analyzing the sentiment of text using [TextBlob](https://textblob.readthedocs.io/en/dev/). The app is built with [Gradio](https://gradio.app/) and can be launched locally or as an MCP server.

## Features

- Analyze the sentiment (polarity and subjectivity) of any input text.
- Get a quick assessment: positive, negative, or neutral.
- Easy-to-use web interface.

## Setup

1. **Clone the repository** (if not already done):

     ```bash
     git clone <your-repo-url>
     cd mcp_course/src/unit2
     ```

2. **Install dependencies**:

     ```bash
     pip install -r requirements.txt
     ```

## Usage

To launch the Gradio app locally:

```bash
python app.py
```

This will start a web server and open the interface in your browser.

## Example

Input:
```
I love using Gradio for building machine learning demos!
```

Output:
```json
{
    "polarity": 0.5,
    "subjectivity": 0.6,
    "assessment": "positive"
}
```

## Files

- `app.py`: Main application code.
- `requirements.txt`: Python dependencies.
- `README.md`: Project documentation.

## License

This project is for educational purposes.