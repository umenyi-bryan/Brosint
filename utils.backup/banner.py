from time import sleep
from rich.console import Console
from rich.text import Text
console = Console()
def animated_banner(author="Chinedu", version="1.0.0"):
    frames = [
        "[bold magenta]██████╗ ██████╗  ██████╗ ███████╗██╗███╗   ██╗████████╗[/]",
        "[bold cyan]██╔══██╗██╔══██╗██╔════╝ ██╔════╝██║████╗  ██║╚══██╔══╝[/]",
        "[bold magenta]██████╔╝██████╔╝██║  ███╗█████╗  ██║██╔██╗ ██║   ██║   [/]",
        "[bold cyan]██╔═══╝ ██╔══██╗██║   ██║██╔══╝  ██║██║╚██╗██║   ██║   [/]",
        "[bold magenta]██║     ██║  ██║╚██████╔╝██║     ██║██║ ╚████║   ██║   [/]",
        "[bold cyan]╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝   ╚═╝   [/]"
    ]
    for _ in range(1):
        for f in frames:
            console.clear()
            console.print(f)
            console.print(f"\\n[bold yellow]by {author} | v{version}[/]\\n", justify="center")
            sleep(0.12)
    console.clear()
    console.print(Text("BROsint - Bright Responsible OSINT", style="bold magenta underline"))
    console.print(f"[bold cyan]Author:[/] {author} | [bold cyan]Version:[/] {version}\\n", justify="center")
