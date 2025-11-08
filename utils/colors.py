from rich import print
def info(msg): print(f"[bold cyan][*][/bold cyan] {msg}")
def ok(msg): print(f"[bold green][+][/bold green] {msg}")
def warn(msg): print(f"[bold yellow][!][/bold yellow] {msg}")
def err(msg): print(f"[bold red][-][/bold red] {msg}")
