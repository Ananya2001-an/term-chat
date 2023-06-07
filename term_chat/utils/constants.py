import time

from rich.progress import Progress, SpinnerColumn, TextColumn


# progress spinner
def spinner(text: str, timer: int):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=text, total=None)
        time.sleep(timer)
    return progress
