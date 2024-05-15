import os
import vertexai
from vertexai.preview.generative_models import (
    GenerativeModel,
    Tool,
    grounding,
    GenerationConfig
)

PROJECT_ID = os.environ.get("GCP_PROJECT")
REGION = os.environ.get("GCP_REGION")

def answer_question(prompt):

    vertexai.init(project=PROJECT_ID, location=REGION)

    model = GenerativeModel("gemini-1.5-pro-preview-0409")

    tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())

    response = model.generate_content(
        prompt,
        tools=[tool],
        generation_config=GenerationConfig(
            temperature=0.0,
            max_output_tokens=8096
        )
    )

    return response.text
