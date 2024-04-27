import asyncio
import re
import os
from dotenv import load_dotenv, find_dotenv
import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai
from semantic_kernel.prompt_template.input_variable import InputVariable

# Load from .env file
load_dotenv(find_dotenv(), override=True)

# Function to extract text from a file
def extract_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to split text into chunks based on max_tokens
def chunk_text(text, max_tokens=2000):
    chunks = [] # list to store schunks of the text
    current_chunk = ""
    paragraphs = re.split(r'\n\s*\n', text) # split text into paragraphs (one or more break line)
    
    for paragraph in paragraphs:
        paragraph_tokens = len(paragraph.split()) # divides paragraph into words (tokens)
        
        # Check if adding this paragraph to the current chunk exceeds the max token limit for the current chunk
        if len(current_chunk.split()) + paragraph_tokens > max_tokens:
            
            # If it does, add the current chunk to the list of chunks and start a new chunk with the current paragraph
            chunks.append(current_chunk.strip()) # Remove leading/trailing whitespace from the chunk before adding
            current_chunk = paragraph + "\n" # Start a new chunk with the current paragraph
        
        else:
            current_chunk += paragraph + "\n" # If not, add the current paragraph to the current chunk
    
    # After all paragraphs have been processed, we check if there is an unfinished chunk (it could be the case if the last paragraph doesn't exceed the max tokens)
    # If so, add this last chunk to the chunks list
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    # Return the list of text chunks
    return chunks

# Function to set up the semantic kernel
def setup_kernel():
    kernel = sk.Kernel() # Kernel instance
    # Add the Azure Chat Completion service to the kernel
    kernel.add_service(
        sk_oai.AzureChatCompletion(
            service_id=None,
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"), # Load from .env
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), # Load from .env
            api_key=os.getenv("AZURE_OPENAI_API_KEY") # Load from .env
        )
    )
    return kernel

# Function to create a summarization function in the kernel based on a template
def create_summarization_function(kernel, name, prompt, is_chunked=False):
    # Set up execution settings for the AI model
    execution_settings = sk_oai.OpenAIChatPromptExecutionSettings(
        service_id=None,
        ai_model_id=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"), # Model to use
        max_tokens=2000, # Maximum number of tokens
        temperature=0.7, # Creativity of the AI
    )
    
    # Configure the prompt template
    prompt_template_config = sk.PromptTemplateConfig(
        template=prompt, # The prompt to use
        name=name, # The name of the template
        template_format="semantic-kernel", # Format of the template
        input_variables=[InputVariable(name="input", description="The user input", is_required=True)], # Required inputs
        execution_settings=execution_settings, # Execution settings
    )
    
    # Define function and plugin names
    function_name = f"{name}Func" if not is_chunked else f"{name}ChunksFunc"
    plugin_name = f"{name}Plugin"
    
    # Create and return the function in the kernel
    return kernel.create_function_from_prompt(
        function_name=function_name,
        plugin_name=plugin_name,
        prompt_template_config=prompt_template_config,
    )


# Main function to execute the program summarization
async def main(chunks):
    # Setup the kernel
    kernel = setup_kernel()

    # Define prompts for summarization
    summarize_prompt = """{{$input}}\nSummarize the content above in a paragraph.\nThis summary should capture the key points of the input texts in a coherent and concise manner. \nAnd after the paragraph, give me 5 bullet points of the main ideas.\n"""
    summarize_chunks_prompt = """{{$input}}\nSummarize the content above in a paragraph.\nThis summary should capture the key points of the input texts in a coherent and concise manner.\n"""

    # Create summarization functions
    summarize = create_summarization_function(kernel, "summarize", summarize_prompt)
    summarize_chunks = create_summarization_function(kernel, "summarizeChunks", summarize_chunks_prompt, is_chunked=True)
    
    # Generate summaries for each chunk
    summaries = [str(await kernel.invoke(summarize_chunks, sk.KernelArguments(input=chunk))) for chunk in chunks]
    # Combine all chunk summaries into one final summary
    final_summary = "\n\n".join(summaries)

    # Generate a final summary of the combined summaries
    summary = await kernel.invoke(summarize, sk.KernelArguments(input=final_summary))
 
    return summary