import gradio as gr
from textblob import TextBlob

def sentiment_analysis(text: str) -> dict:
    """
    Performs sentiment analysis on the input text.

    Args:
        text (str): The text to analyze.

    Returns:
        dict: A dictionary containing polarity, subjectivity, and a qualitative assessment.
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0.1:
        assessment = "positive"
    elif polarity < -0.1:
        assessment = "negative"
    else:
        assessment = "neutral"

    return {
        "polarity": polarity,
        "subjectivity": subjectivity,
        "assessment": assessment
    }

iface = gr.Interface(
    fn=sentiment_analysis,
    inputs=gr.Textbox(lines=2, placeholder="Enter text for sentiment analysis..."),
    outputs=gr.JSON(),
    title="Sentiment Analysis Tool (MCP Enabled)",
    description="Enter text to get its sentiment polarity, subjectivity, and a qualitative assessment. This server is MCP enabled."
)

if __name__ == "__main__":
    # Launch the server with mcp_server=True to enable the MCP endpoint
    iface.launch(mcp_server=True)
