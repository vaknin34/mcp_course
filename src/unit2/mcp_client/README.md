---
title: AI Agent with MCP Tools
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: gradio
python_version: 3.11
app_file: app.py
short_description: AI agent using MCP tools for sentiment analysis
tags:
    - ai-agent
    - mcp
    - sentiment-analysis
    - smolagents
    - chatbot
---

# AI Agent with MCP Tools for Sentiment Analysis

This project provides an intelligent AI agent that can analyze text sentiment using Model Context Protocol (MCP) tools. The agent is built with [smolagents](https://huggingface.co/docs/smolagents) and [Gradio](https://gradio.app/) to provide a conversational interface for sentiment analysis tasks.

## Features

- **Conversational AI Agent**: Chat-based interface powered by Hugging Face's inference API
- **MCP Integration**: Uses Model Context Protocol to connect to external sentiment analysis tools
- **Real-time Analysis**: Analyze sentiment through natural language conversations
- **Easy-to-use Interface**: Clean Gradio chat interface with example prompts

## Setup

1. **Clone the repository** (if not already done):

     ```bash
     git clone <your-repo-url>
     cd mcp_course/src/unit2/mcp_client
     ```

2. **Install dependencies**:

     ```bash
     pip install -r requirements.txt
     ```

3. **Set up environment variables**:
     ```bash
     export HUGGINGFACE_API_TOKEN=your_token_here
     ```

## Usage

To launch the Gradio app locally:

```bash
python app.py
```

This will start a web server and open the chat interface in your browser. You can then interact with the AI agent using natural language to perform sentiment analysis.

## Example

**User Input:**
```
Analyze the sentiment of the following text 'This is awesome'
```

**Agent Response:**
The agent will use the connected MCP tools to analyze the sentiment and provide a detailed response about the polarity, subjectivity, and overall sentiment assessment.

## Architecture

- **AI Agent**: Built with smolagents CodeAgent for intelligent task execution
- **MCP Client**: Connects to external sentiment analysis MCP server
- **Model**: Uses Hugging Face Inference API for language understanding
- **Interface**: Gradio ChatInterface for seamless user interaction

## Files

- `app.py`: Main application with AI agent setup and Gradio interface
- `requirements.txt`: Python dependencies (smolagents with MCP support)
- `tiny_agent.json`: MCP client configuration
- `README.md`: Project documentation

## License

This project is for educational purposes.