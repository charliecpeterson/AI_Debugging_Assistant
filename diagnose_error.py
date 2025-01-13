import argparse
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from rich.console import Console
from rich.text import Text

# Initialize rich console for formatted output
console = Console()

# Define the LangChain prompt template
template = """
You are an expert software debugging assistant. You will be provided with an error log or message.

Task:
1. Identify the key error(s) from the input.
2. Provide possible reasons and diagnoses for the error(s).
3. Highlight the specific lines or sections that indicate the error.

Error Log:
{error_log}

Response:
"""

prompt = ChatPromptTemplate.from_template(template)

# Initialize the Ollama LLM
model = OllamaLLM(model="llama3.2")

# Define the chain
error_chain = prompt | model


def analyze_log(error_log, conversation_history=None):
    """Analyze the provided error log and return the response."""
    if conversation_history:
        # Append context to maintain conversation history
        full_context = "\n".join(conversation_history) + f"\nFollow-up:\n{error_log}"
    else:
        full_context = error_log

    response = error_chain.invoke({"error_log": full_context})
    return response


def save_results(response, file_name="diagnosis.txt"):
    """Save the AI diagnosis to a file."""
    with open(file_name, "w") as file:
        file.write(response)
    console.print(f"Results saved to [green]{file_name}[/green].", style="bold green")


def interactive_mode(initial_context=None):
    """Interactive conversation mode with the AI agent."""
    console.print(
        "Entering [bold cyan]Interactive Mode[/bold cyan]. Type 'exit' to quit.",
        style="cyan",
    )
    conversation_history = [initial_context] if initial_context else []

    while True:
        user_input = input("\nEnter follow-up question or description (or 'exit' to quit):\n> ")
        if user_input.lower() == "exit":
            console.print("Goodbye!", style="bold cyan")
            break

        # Append to conversation history
        conversation_history.append(user_input)
        response = analyze_log(user_input, conversation_history)
        console.print("\n[bold cyan]AI Agent Response:[/bold cyan]")
        console.print(response, style="green")


def main():
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description="Process an error log file with an LLM.")
    parser.add_argument("file", type=str, nargs="?", help="Path to the error log file (optional)")
    parser.add_argument("--save", type=str, help="File name to save the results (optional)", default=None)
    args = parser.parse_args()

    initial_context = None

    if args.file:
        try:
            # Read the contents of the provided file
            with open(args.file, "r") as file:
                error_log = file.read()
        except FileNotFoundError:
            console.print(f"Error: File '{args.file}' not found.", style="bold red")
            return
        except Exception as e:
            console.print(f"Error reading file: {e}", style="bold red")
            return

        # Analyze the log and display the result
        initial_context = error_log
        response = analyze_log(error_log)
        console.print("\n[bold cyan]AI Agent Response:[/bold cyan]")
        console.print(response, style="green")

        # Save the result if the --save option is provided
        if args.save:
            save_results(response, args.save)

    # Enter interactive mode for follow-ups
    interactive_mode(initial_context)


if __name__ == "__main__":
    main()
