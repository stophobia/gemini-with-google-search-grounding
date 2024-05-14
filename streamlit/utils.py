import os
import vertexai
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory
)
from typing import List
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1alpha as discoveryengine
from dataclasses import dataclass

@dataclass
class SearchResult:
    source_doc_url: str
    source_file_name: str
    summary: str
    extracted_content: str

PROJECT_ID = os.environ.get("GCP_PROJECT")  # Your Google Cloud Project ID
REGION = os.environ.get("GCP_REGION")  # Your Google Cloud Project Region
LOCATION = os.environ.get("AGENT_LOCATION")  # Your Google Cloud Project Region
DATASTORE_ID = os.environ.get("DATASTORE_ID") 
BUCKET_NAME = os.environ.get("BUCKET_NAME") 

def search_document(prompt):

    client = discoveryengine.SearchServiceClient(
        client_options=(
            ClientOptions(
                api_endpoint=f"{LOCATION}-discoveryengine.googleapis.com"
            )
            if LOCATION != "global"
            else None
        )
    )

    serving_config = client.serving_config_path(
        project=PROJECT_ID,
        location=LOCATION,
        data_store=DATASTORE_ID,
        serving_config="default_config",
    )

    content_search_spec = discoveryengine.SearchRequest.ContentSearchSpec(
        # For information about snippets, refer to:
        # https://cloud.google.com/generative-ai-app-builder/docs/snippets
        snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
            return_snippet=True
        ),  
        extractive_content_spec=discoveryengine.SearchRequest.ContentSearchSpec.ExtractiveContentSpec(
            max_extractive_answer_count=1,
            max_extractive_segment_count=1,
        ),
        # For information about search summaries, refer to:
        # https://cloud.google.com/generative-ai-app-builder/docs/get-search-summaries
        summary_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
            summary_result_count=1,
            include_citations=True,
            ignore_adversarial_query=False,
            ignore_non_summary_seeking_query=False,
        ),
    )

    response = client.search(
        discoveryengine.SearchRequest(
            serving_config=serving_config,
            query=prompt,
            page_size=10,
            content_search_spec=content_search_spec,
            query_expansion_spec=discoveryengine.SearchRequest.QueryExpansionSpec(
                condition=discoveryengine.SearchRequest.QueryExpansionSpec.Condition.AUTO,
            ),
            spell_correction_spec=discoveryengine.SearchRequest.SpellCorrectionSpec(
                mode=discoveryengine.SearchRequest.SpellCorrectionSpec.Mode.AUTO
            ),
        )
    )

    #print(f"Full response: {response}")

    summary = response.summary.summary_text
    print(f"Generated summary: {summary}")

    extractive_segments = response.results[0].document.derived_struct_data.get("extractive_segments", "")
    extracted_content = extractive_segments[0].get("content", "")
    #print(f"Extracted content: {extracted_content}")

    link = response.results[0].document.derived_struct_data.get("link", "")
    print(f"Source document URL: {link}")

    # Extract the source file name from the link)
    start_index = link.find(f'{BUCKET_NAME}/') + len(f'{BUCKET_NAME}/')
    substring = link[start_index:]
    source_file_name = substring
    source_doc_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{source_file_name}"

    return SearchResult(source_doc_url, source_file_name, summary, extracted_content)

def generate_answer(question, summary, extracted_content, source_doc_url):

    # Prompt for Gemini Pro model
    prompt_gemini = f"""
    You work for the Ninja Rail company and is an expert on everything about the company and rail in general.

    Your job is to answer to employee's questions about the company but only if the data retrieval was successful.

    So when a user refers to "us" or "our" it should refer to the company (Ninja Rail).

    Evaluate the answer obtained from a retrieval system, and if looks like an answer was retrieved do the following:
    - First, clearly state that you found an answer in Ninja Rail corporatedata (in bolded text)
    - Second, answer it using the the summary and the extracted content while keeping the original question in context.
    - Finally, provide the source url as a reference to the answer.

    If no answer was retrieved from the retrieval system, do the following:
    
    - First, clearly states (in bolded text) that you did not find an answer in Ninja Rail corporate data. Be concise and use a funny tone.
    - Second, tell the user you will try to answer the question anyways using common knowledge. Clearly indicate that it is not coming from official Ninja Rail corporatedata you have been trained on and that it might not be accurate.
    - Finally, reiterate the following limitations of your capabilities:
        - You don't remember previous questions and you just focus on the current one.
        - When you don't find an answer in the Ninja Rail corporate data, you sometimes invent stuff
    -    You are still in training and constantly evolving.

    Question: {question}
    Answer: {summary}
    Retrieved Content: {extracted_content}
    Reference: {source_doc_url}
    """

    print(f"Prompt for Gemini Pro model:{prompt_gemini}")

    model = GenerativeModel("gemini-1.0-pro-002")  # specify the gemini model version

    generation_config = GenerationConfig(
        temperature=0.0,
        top_p=1.0,
        max_output_tokens=8096,
    )

    print(f"Prompt for Gemini Pro model:{prompt_gemini}")

    response = model.generate_content(
        prompt_gemini,
        generation_config=generation_config,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        stream=False,
    )

    response_text = response.text

    return response_text