"""Interactive Terminal User Interface for ZeroTrace."""
import asyncio
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn

from zerotrace.modules.ip_intel import scan_ip, get_my_ip
from zerotrace.modules.phone_intel import scan_phone
from zerotrace.modules.username_intel import scan_username
from zerotrace.modules.domain_intel import scan_domain
from zerotrace.modules.email_intel import scan_email
from zerotrace.core.exporter import export_report

console = Console()

BANNER = """[bold cyan]
  ______                 _______                    
 |___  /                |__   __|                   
    / / ___ _ __ ___       | |_ __ __ _  ___ ___    
   / / / _ \ '__/ _ \      | | '__/ _` |/ __/ _ \   
  / /_|  __/ | | (_) |     | | | | (_| | (_|  __/   
 /_____\___|_|  \___/      |_|_|  \__,_|\___\___|   
[/bold cyan]
[dim bold cyan]  OSINT & Reconnaissance Framework • v1.0.0[/dim bold cyan]
[dim italic]  https://github.com/stymrj/ZeroTrace[/dim italic]
"""

def print_result_table(title: str, data: dict):
    table = Table(title=title, show_header=True, header_style="bold magenta", border_style="cyan")
    table.add_column("Property", style="bold cyan", width=26)
    table.add_column("Details", style="white")
    for key, val in data.items():
        table.add_row(key, str(val))
    console.print(table)

def maybe_export(module_name: str, target: str, data: dict):
    if Confirm.ask("\n[bold yellow]Export these findings to report files (JSON & Markdown)?[/bold yellow]", default=False):
        saved_file = export_report(module_name, target, data)
        console.print(f"[bold green]✓ Report generated successfully at:[/bold green] [cyan]{saved_file}[/cyan]")

def handle_ip():
    target = Prompt.ask("[bold yellow]Enter target IP address[/bold yellow]")
    with Progress(SpinnerColumn(), TextColumn("[cyan]Querying IP Intelligence...[/cyan]"), transient=True) as p:
        p.add_task("query", total=None)
        res = scan_ip(target)
    if "error" in res:
        console.print(f"[bold red]✗ Error:[/bold red] {res['error']}")
    else:
        print_result_table(f"IP Reconnaissance: {target}", res)
        maybe_export("IP", target, res)

def handle_my_ip():
    with Progress(SpinnerColumn(), TextColumn("[cyan]Resolving local public IP...[/cyan]"), transient=True) as p:
        p.add_task("query", total=None)
        res = get_my_ip()
    if "error" in res:
        console.print(f"[bold red]✗ Error:[/bold red] {res['error']}")
    else:
        print_result_table("Public IP Telemetry", res)
        maybe_export("Public_IP", res.get("Target IP", "self"), res)

def handle_phone():
    phone = Prompt.ask("[bold yellow]Enter target phone number (e.g. +14155552671 or +919876543210)[/bold yellow]")
    res = scan_phone(phone)
    if "error" in res:
        console.print(f"[bold red]✗ Error:[/bold red] {res['error']}")
    else:
        print_result_table(f"Phone Reconnaissance: {phone}", res)
        maybe_export("Phone", phone, res)

def handle_username():
    uname = Prompt.ask("[bold yellow]Enter target username[/bold yellow]")
    with Progress(SpinnerColumn(), TextColumn(f"[cyan]Scanning 20+ social targets for @{uname}...[/cyan]"), transient=True) as p:
        p.add_task("scan", total=None)
        results = asyncio.run(scan_username(uname))

    table = Table(title=f"Social Footprint: @{uname}", show_header=True, header_style="bold magenta", border_style="cyan")
    table.add_column("Platform", style="bold cyan", width=20)
    table.add_column("Status", width=14)
    table.add_column("Profile URL", style="white")

    found_count = 0
    export_dict = {}
    for r in results:
        if r["found"]:
            found_count += 1
            status_text = "[bold green]FOUND[/bold green]"
            table.add_row(r["name"], status_text, r["url"])
            export_dict[r["name"]] = r["url"]
        else:
            status_text = "[dim red]NOT FOUND[/dim red]"
            table.add_row(r["name"], status_text, "[dim]-[/dim]")
            export_dict[r["name"]] = "Not Found"

    console.print(table)
    console.print(f"[bold green]Summary:[/bold green] Found {found_count} profile(s) across {len(results)} platforms.")
    maybe_export("Username", uname, export_dict)

def handle_domain():
    domain = Prompt.ask("[bold yellow]Enter domain name (e.g. example.com)[/bold yellow]")
    res = scan_domain(domain)
    print_result_table(f"Domain Reconnaissance: {domain}", res)
    maybe_export("Domain", domain, res)

def handle_email():
    email = Prompt.ask("[bold yellow]Enter email address (e.g. target@example.com)[/bold yellow]")
    res = scan_email(email)
    if "error" in res:
        console.print(f"[bold red]✗ Error:[/bold red] {res['error']}")
    else:
        print_result_table(f"Email Reconnaissance: {email}", res)
        maybe_export("Email", email, res)

def main():
    while True:
        console.clear()
        console.print(BANNER)
        console.print(Panel("""[bold white]Select Reconnaissance Module:[/bold white]

 [1] [cyan]Target IP Intelligence & ASN Telemetry[/cyan]
 [2] [cyan]Resolve & Inspect Your Public IP[/cyan]
 [3] [cyan]Global Phone Number Footprinting[/cyan]
 [4] [cyan]Asynchronous Username Scanner (Multi-Platform)[/cyan]
 [5] [cyan]Domain & DNS Footprinting (A, AAAA, MX, NS, TXT)[/cyan]
 [6] [cyan]Email Address Validator & Gravatar Recon[/cyan]
 [0] [red]Exit ZeroTrace[/red]
""", title="[bold green]ZeroTrace Terminal Engine[/bold green]", border_style="cyan", expand=False))

        choice = Prompt.ask("[bold yellow]Select Option[/bold yellow]", choices=["0", "1", "2", "3", "4", "5", "6"], default="1")
        if choice == "1":
            handle_ip()
        elif choice == "2":
            handle_my_ip()
        elif choice == "3":
            handle_phone()
        elif choice == "4":
            handle_username()
        elif choice == "5":
            handle_domain()
        elif choice == "6":
            handle_email()
        elif choice == "0":
            console.print("\n[bold cyan]Exiting ZeroTrace. Good hunting![/bold cyan]\n")
            sys.exit(0)

        Prompt.ask("\n[dim]Press [bold yellow]Enter[/bold yellow] to return to main menu...[/dim]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Terminated by user. Exiting...[/bold red]")
        sys.exit(0)
