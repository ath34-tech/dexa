import typer
import os
from dotenv import set_key, load_dotenv
from dexa.orchestration.orchestrator import Orchestrator

# Get absolute path for .env file
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOTENV_PATH = os.path.join(PROJECT_ROOT, ".env")

app=typer.Typer(no_args_is_help=True)
orch=Orchestrator()

@app.command()
def chat(
    api_key: str = typer.Option(None, help="The Groq API key to use."),
    model_name: str = typer.Option(None, "--model-name", help="The Groq model name to use (e.g., llama-3.1-8b-instant)."),
    kaggle_username: str = typer.Option(None, "--kaggle-username", help="The Kaggle username to use."),
    kaggle_key: str = typer.Option(None, "--kaggle-key", help="The Kaggle API key to use.")
):
    """
    Starts a chat session with the Dexa AI.
    """
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key
        set_key(DOTENV_PATH, "GROQ_API_KEY", api_key)
    
    if model_name:
        os.environ["GROQ_MODEL_NAME"] = model_name
        set_key(DOTENV_PATH, "GROQ_MODEL_NAME", model_name)
    
    if kaggle_username:
        os.environ["KAGGLE_USERNAME"] = kaggle_username
        set_key(DOTENV_PATH, "KAGGLE_USERNAME", kaggle_username)
    
    if kaggle_key:
        os.environ["KAGGLE_KEY"] = kaggle_key
        set_key(DOTENV_PATH, "KAGGLE_KEY", kaggle_key)

    # Re-initialize orchestrator if any configuration changed
    if any([api_key, model_name, kaggle_username, kaggle_key]):
        global orch
        orch = Orchestrator()

    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    
    console = Console()
    console.print("[bold green]Welcome to Dexa AI! Type 'exit' to quit.[/bold green]\n")

    while True:
        try:
            query = console.input("[bold cyan]>> [/bold cyan]")
            if not query.strip():
                continue
            if query.lower() in ['exit', 'quit']:
                console.print("[bold green]Goodbye![/bold green]")
                break
            
            with console.status("[bold yellow]Thinking...[/bold yellow]"):
                result = orch.run(query=query)
                
            console.print("\n[bold magenta]Dexa AI:[/bold magenta]")
            console.print(Panel(Markdown(result), border_style="blue"))
            console.print("")
            
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold green]Goodbye![/bold green]")
            break

@app.command()
def config(
    groq_key: str = typer.Option(None, "--groq-key", help="The Groq API key to set."),
    model_name: str = typer.Option(None, "--model-name", help="The Groq model name to set."),
    kaggle_username: str = typer.Option(None, "--kaggle-username", help="The Kaggle username to set."),
    kaggle_key: str = typer.Option(None, "--kaggle-key", help="The Kaggle API key to set.")
):
    """
    Set configuration for Dexa AI.
    """
    if groq_key:
        set_key(DOTENV_PATH, "GROQ_API_KEY", groq_key)
        print(f"GROQ_API_KEY set successfully in .env.")
    
    if model_name:
        set_key(DOTENV_PATH, "GROQ_MODEL_NAME", model_name)
        print(f"GROQ_MODEL_NAME set successfully in .env.")
    
    if kaggle_username:
        set_key(DOTENV_PATH, "KAGGLE_USERNAME", kaggle_username)
        print(f"KAGGLE_USERNAME set successfully in .env.")
    
    if kaggle_key:
        set_key(DOTENV_PATH, "KAGGLE_KEY", kaggle_key)
        print(f"KAGGLE_KEY set successfully in .env.")
    
    if not any([groq_key, model_name, kaggle_username, kaggle_key]):
        print("Please provide at least one option: --groq-key, --model-name, --kaggle-username, or --kaggle-key")

@app.command()
def load_data(path: str = typer.Argument(..., help="Path to the data file (CSV, Parquet, Excel).")):
    """
    Load a local data file into the session context.
    """
    result = orch.load_file(path)
    print(result)

@app.command()
def load_file(path: str = typer.Argument(..., help="Path to the data file (CSV, Parquet, Excel).")):
    """
    Load a local data file into the session context.
    """
    result = orch.load_file(path)
    print(result)

@app.command()
def load_kaggle(
    dataset: str = typer.Argument(..., help="Kaggle dataset identifier (e.g., 'username/dataset-name')."),
    username: str = typer.Option(None, help="Kaggle username."),
    key: str = typer.Option(None, help="Kaggle API key.")
):
    """
    Load a dataset from Kaggle into the session context.
    """
    if username:
        os.environ["KAGGLE_USERNAME"] = username
    if key:
        os.environ["KAGGLE_KEY"] = key
    
    result = orch.load_kaggle(dataset)
    print(result)

if __name__=="__main__":
    load_dotenv(DOTENV_PATH)
    app()
