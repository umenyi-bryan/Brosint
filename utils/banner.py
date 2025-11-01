from rich.console import Console
from rich.text import Text

def show_banner():
    banner = Text(r"""
██████╗ ██████╗  ██████╗ ███████╗██╗███╗   ██╗████████╗
██╔══██╗██╔══██╗██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
██████╔╝██████╔╝██║   ██║███████╗██║██╔██╗ ██║   ██║   
██╔═══╝ ██╔══██╗██║   ██║╚════██║██║██║╚██╗██║   ██║   
██║     ██║  ██║╚██████╔╝███████║██║██║ ╚████║   ██║   
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
      Bright Responsible OSINT — (BROsint)
    """)
    banner.stylize("bold magenta")
    Console().print(banner)
