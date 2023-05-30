import time

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.style import Style

# styles for rich console
error_style = Style(color="red", bold=True)
success_style = Style(color="green", bold=True)
message_style = Style(color="blue", bold=True)
header_style = Style(color="magenta", bold=True)
console = Console()


# progress spinner
def spinner(text: str, timer: int) -> Progress:
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=text, total=None)
        time.sleep(timer)
    return progress
