---
title: MCP Tools Demo
emoji: 🛠️
colorFrom: indigo
colorTo: blue
sdk: gradio
sdk_version: 5.32.1
app_file: app.py
pinned: false
license: apache-2.0
short_description: A multi-tool Gradio application with MCP integration
---

# MCP Tools Demo

This is a multi-tool Gradio application that demonstrates the integration of Model Context Protocol (MCP) tools. The application includes three tools:

1. **Sentiment Analysis Tool**: Analyzes the sentiment of text and provides polarity and subjectivity scores.
2. **Weather Tool**: Provides weather information for a specified location.
3. **Calculator Tool**: Performs basic arithmetic operations (add, subtract, multiply, divide).

## MCP Integration

This application uses the `smolagents` library to expose its tools via the Model Context Protocol (MCP). When running locally with the `MCP_SERVER=true` environment variable, the tools are accessible programmatically through MCP endpoints.

## Local Development

To run this application locally with MCP support:

1. Create a `.env` file with the following content:
   ```
   SERVER_NAME=0.0.0.0
   SERVER_PORT=7860
   MCP_SERVER=true
   ```

2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

## Hugging Face Space Deployment

When deployed to Hugging Face Spaces, the application will run with standard Gradio functionality. MCP support in Hugging Face Spaces is currently limited.
