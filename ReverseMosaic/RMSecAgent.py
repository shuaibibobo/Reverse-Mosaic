from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.llms.huggingface import HuggingFaceLLM
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.agent import AgentRunner
try:
    from ReverseMosaic.misc_helper import get_text_from_pdf
except:
    from misc_helper import get_text_from_pdf
from pprint import pprint 
import gc
from llama_index.core.base.llms.types import ChatMessage, MessageRole

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)


class AgentHelper:
    """
    A helper class for AgentRunner containing utility functions.
    """

    def __init__(self):
        self.saved_model = None
        self.saved_tokenizer = None
        self.saved_embed_model = None
        self.llm_model_name = "unsloth/codegemma-7b-bnb-4bit"
        self.embedding_model_name = "BAAI/bge-small-en-v1.5"

    def execute_step(self, agent: AgentRunner, task):
        """
        Execute a single step for an agent.

        Args:
            agent (AgentRunner): The agent runner.
            task: The task to execute.

        Returns:
            response: The response from the agent.
        """
        gc.collect()
        step_output = agent.run_step(task.task_id)
        if step_output.is_last:
            response = agent.finalize_response(task.task_id)
            print(f"> Agent finished: {str(response)}")
            return response
        else:
            return None

    def execute_steps(self, agent: AgentRunner, task, console=None):
        """
        Execute all steps for an agent.

        Args:
            agent (AgentRunner): The agent runner.
            task: The task to execute.
            console: The console for displaying steps (optional).

        Returns:
            response: The final response from the agent.
        """
        if console:
            with console.status("[bold green]Executing analysis...") as status:
                response = self.execute_step(agent, task)
                while response is None:
                    response = self.execute_step(agent, task)

                return response
        else:
            response = self.execute_step(agent, task)
            while response is None:
                response = self.execute_step(agent, task)
            return response

    def load_model(self):
        """
        Load the pre-trained language model and tokenizer.

        Returns:
            model (transformers.PreTrainedModel): Loaded language model.
            tokenizer (transformers.PreTrainedTokenizer): Loaded tokenizer.
        """
        if self.saved_model is None:
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                use_cuda_fp16=True,
            )
            model = AutoModelForCausalLM.from_pretrained(self.llm_model_name, quantization_config=quantization_config,low_cpu_mem_usage=True)
            tokenizer = AutoTokenizer.from_pretrained(self.llm_model_name, padding_side="left")

            self.saved_model = model
            self.saved_tokenizer = tokenizer
            return model, tokenizer
        else:
            return self.saved_model, self.saved_tokenizer

    def get_llm(self):
        """
        Get the HuggingFaceLLM object.

        Returns:
            llm (HuggingFaceLLM): HuggingFace Language Model object.
        """
        def messages_to_prompt(messages):
            prompt = ""
            for message in messages:
                if message.role == 'system':
                    prompt += f"\n{message.content}</s>\n"
                elif message.role == 'user':
                    prompt += f"\n{message.content}</s>\n"
                elif message.role == 'assistant':
                    prompt += f"\n{message.content}</s>\n"

            # Ensure we start with a system prompt, insert blank if needed
            if not prompt.startswith("\n"):
                prompt = "\n</s>\n" + prompt

            # Add final assistant prompt
            prompt = prompt + "\n"

            return prompt

        def completion_to_prompt(completion):
            return f"\n</s>\n\n{completion}</s>\n\n"

        model, tokenizer = self.load_model()

        llm = HuggingFaceLLM(
            model=model,
            tokenizer_name=self.llm_model_name,
            model_name=self.llm_model_name,
            tokenizer=tokenizer,
            max_new_tokens=500,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
        )

        return llm

    def generate_tool(self, tool_name, pdf_path, working_dir, description):
        """
        Generate a tool.

        Args:
            tool_name (str): Name of the tool.
            pdf_path (str): Path to the PDF file.
            working_dir (str): Working directory for storing indexes.
            description (str): Description of the tool.

        Returns:
            tool: The generated tool.
        """
        # Load embedding model
        if self.saved_embed_model is None:
            embed_model = HuggingFaceEmbedding(model_name=self.embedding_model_name)
            Settings.embed_model = embed_model
        else:
            embed_model = self.saved_embed_model

        try:
            storage_context = StorageContext.from_defaults(persist_dir=working_dir)
            index = load_index_from_storage(storage_context)
            index_loaded = True
        except:
            index_loaded = False

        if not index_loaded:
            # Load data
            docs = SimpleDirectoryReader(input_files=[pdf_path]).load_data()

            # Build index
            index = VectorStoreIndex.from_documents(docs)

            # Persist index
            index.storage_context.persist(persist_dir=working_dir)

        # Create query engine
        engine = index.as_query_engine(similarity_top_k=3, llm=self.get_llm())

        description = f"Provides information about: {description}."

        tool = QueryEngineTool(
            query_engine=engine,
            metadata=ToolMetadata(
                name=tool_name,
                description=(
                    description.split("\n")
                ),
            ),
        )

        return tool
