import typer
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from model import Todo
from database import get_all_todo, delete_todo, insert_todo, complete_todo, update_todo, deleteall_data

app = typer.Typer()
console = Console()

@app.command(short_help='Adds an item')
def add(task: str, category: str):
    console.print(f"[green]To-do ADDED: {task} Category: {category} [/green]")
    todo = Todo(task, category)
    insert_todo(todo)
    show()

@app.command(short_help='Deletes an item')
def delete(id: int):
    console.print(f"[red]To-do with ID {id} DELETED [/red]")
    delete_todo(id)
    show()

@app.command(short_help='Update an item')
def update(id: int, task: str = None, category: str = None):
    console.print(f"[yellow]Updating task with ID {id}[/yellow]")
    update_todo(id, task, category)
    show()

@app.command(short_help='Mark as done an item')
def complete(id: int):
    console.print(f"[green]To-do with ID {id} COMPLETE[/green]")
    complete_todo(id)
    show()

@app.command(short_help='Delete all data')
def deleteall():
    deleteall_data()
    console.print(f"[red]LIST HAS BEEN CLEANED[/red]")
    show()

@app.command(short_help='Show To-Do list')
def show():
    tasks = get_all_todo()
    # print(f"Tasks fetched from database: {tasks}") 
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("ID", style="dim", width=3)
    table.add_column("Todo", min_width=20, width=24)
    table.add_column("Category", min_width=24, justify="right")
    table.add_column("Status", min_width=6, justify="right")
    
    color = 'cyan'

    for task in tasks:
        is_done_str = f'[green]DONE[/green]' if task.status == 2 else f'[bold red]NOT YET[bold /red]'
        table.add_row(f'[{color}]{task.id}[/{color}]', 
                      f'[{color}]{task.task}[/{color}]', 
                      f'[{color}]{task.category}[/{color}]', is_done_str)
    
    console.print(Panel.fit(table, title=f"[bold blue]TooDoos[/bold blue]", style="magenta"))

if __name__ == "__main__":
    app()
