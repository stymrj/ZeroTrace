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
from zerotrace.modules.exif_intel import analyze_exif, strip_exif
from zerotrace.modules.url_intel import unshorten_url
from zerotrace.modules.geoip_consensus import get_consensus
from zerotrace.modules.mac_intel import lookup_mac
from zerotrace.core.exporter import export_report
from zerotrace.core.config import SOCIAL_TARGETS

console = Console()

BANNER = """[bold cyan]
  ______                 _______                    
 |___  /                |__   __|                   
    / / ___ _ __ ___       | |_ __ __ _  ___ ___    
   / / / _ \ '__/ _ \      | | '__/ _` |/ __/ _ \   
  / /_|  __/ | | (_) |     | | | | (_| | (_|  __/   
 /_____\___|_|  \___/      |_|_|  \__,_|\___\___|   
[/bold cyan]
[dim bold cyan]  ⚡ Advanced OSINT, Threat Intel & Digital Forensics Suite • v1.2.0[/dim bold cyan]
[dim italic]  https://github.com/stymrj/ZeroTrace[/dim italic]
"""

def print_result_table(title: str, data: dict):
    table = Table(title=title, show_header=True, header_style="bold magenta", border_style="cyan")
    table.add_column("Property / Indicator", style="bold cyan", width=28)
    table.add_column("Intelligence Details", style="white")
    for key, val in data.items():
        val_str = str(val)
        if "HIGH" in val_str or ("Vulnerabilities" in key and val_str not in ("Clean / None indexed", "None publicly indexed")):
            table.add_row(key, f"[bold red]{val_str}[/bold red]")
        elif "Hosting" in val_str or "VPN" in val_str or "Redirected" in val_str:
            table.add_row(key, f"[bold yellow]{val_str}[/bold yellow]")
        elif val_str.startswith("http"):
            table.add_row(key, f"[underline blue]{val_str}[/underline blue]")
        else:
            table.add_row(key, val_str)
    console.print(table)

def maybe_export(module_name: str, target: str, data: dict):
    if Confirm.ask("\n[bold yellow]Export findings to report files (JSON & Markdown)?[/bold yellow]", default=False):
        saved_file = export_report(module_name, target, data)
        console.print(f"[bold green]✓ Report generated successfully at:[/bold green] [cyan]{saved_file}[/cyan]")

def handle_ip():
    target = Prompt.ask("[bold yellow]Enter target IP address (e.g. 1.1.1.1)[/bold yellow]")
    with Progress(SpinnerColumn(), TextColumn("[cyan]Querying IP, ASN & Shodan InternetDB...[/cyan]"), transient=True) as p:
        p.add_task("query", total=None)
        res = scan_ip(target)
    if "error" in res:
        console.print(f"[bold red]✗ Error:[/bold red] {res['error']}")
    else:
        print_result_table(f"IP & Shodan Telemetry: {target}", res)
        maybe_export("IP", target, res)

def handle_geoip_consensus():
    target = Prompt.ask("[bold yellow]Enter IP address for Multi-Engine Consensus[/bold yellow]")
    with Progress(SpinnerColumn(), TextColumn("[cyan]Cross-checking multiple GeoIP engines...[/cyan]"), transient=True) as p:
        p.add_task("query", total=None)
        res = get_consensus(target)
    if "error" in res:
        console.print(f"[bold red]✗ Error:[/bold red] {res['error']}")
    else:
        print_result_table(f"Multi-Engine GeoIP Consensus: {target}", res)
        maybe_export("GeoIP_Consensus", target, res)

def handle_my_ip():
    with Progress(SpinnerColumn(), TextColumn("[cyan]Resolving local public IP & threat footprint...[/cyan]"), transient=True) as p:
        p.add_task("query", total=None)
        res = get_my_ip()
    if "error" in res:
        console.print(f"[bold red]✗ Error:[/bold red] {res['error']}")
    else:
        print_result_table("Public IP Telemetry", res)
        maybe_export("Public_IP", res.get("Target IP", "self"), res)

def handle_phone():
    phone = Prompt.ask("[bold yellow]Enter phone number (e.g. +919876543210)[/bold yellow]")
    res = scan_phone(phone)
    if "error" in res:
        console.print(f"[bold red]✗ Error:[/bold red] {res['error']}")
    else:
        print_result_table(f"Phone & Telecom Recon: {phone}", res)
        maybe_export("Phone", phone, res)

def handle_username():
    uname = Prompt.ask("[bold yellow]Enter target username[/bold yellow]")
    with Progress(SpinnerColumn(), TextColumn(f"[cyan]Scanning {len(SOCIAL_TARGETS)}+ platforms for @{uname}...[/cyan]"), transient=True) as p:
        p.add_task("scan", total=None)
        results = asyncio.run(scan_username(uname))

    table = Table(title=f"Social & Dev Footprint: @{uname}", show_header=True, header_style="bold magenta", border_style="cyan")
    table.add_column("Platform", style="bold cyan", width=18)
    table.add_column("Category", style="yellow", width=12)
    table.add_column("Status", width=14)
    table.add_column("Profile URL", style="white")

    found_count = 0
    export_dict = {}
    for r in results:
        cat = next((s.get("cat", "General") for s in SOCIAL_TARGETS if s["name"] == r["name"]), "General")
        if r["found"]:
            found_count += 1
            status_text = "[bold green]FOUND[/bold green]"
            table.add_row(r["name"], cat, status_text, r["url"])
            export_dict[r["name"]] = r["url"]
        else:
            status_text = "[dim red]NOT FOUND[/dim red]"
            table.add_row(r["name"], cat, status_text, "[dim]-[/dim]")
            export_dict[r["name"]] = "Not Found"

    console.print(table)
    console.print(f"[bold green]Summary:[/bold green] Found [bold cyan]{found_count}[/bold cyan] profile(s) across {len(results)} platforms.")
    maybe_export("Username", uname, export_dict)

def handle_domain():
    domain = Prompt.ask("[bold yellow]Enter domain name (e.g. github.com)[/bold yellow]")
    with Progress(SpinnerColumn(), TextColumn("[cyan]Querying DNS & crt.sh Subdomains...[/cyan]"), transient=True) as p:
        p.add_task("query", total=None)
        res = scan_domain(domain)
    print_result_table(f"Domain & CT Recon: {domain}", res)
    maybe_export("Domain", domain, res)

def handle_email():
    email = Prompt.ask("[bold yellow]Enter email address (e.g. target@example.com)[/bold yellow]")
    res = scan_email(email)
    if "error" in res:
        console.print(f"[bold red]✗ Error:[/bold red] {res['error']}")
    else:
        print_result_table(f"Email Reconnaissance: {email}", res)
        maybe_export("Email", email, res)

def handle_exif():
    path = Prompt.ask("[bold yellow]Enter image file path (e.g. photo.jpg)[/bold yellow]")
    res = analyze_exif(path)
    if "error" in res:
        console.print(f"[bold red]✗ Error:[/bold red] {res['error']}")
    else:
        print_result_table(f"Image EXIF Forensics: {path}", res)
        if Confirm.ask("\n[bold yellow]Strip (remove) all metadata from this image for privacy?[/bold yellow]", default=False):
            strip_res = strip_exif(path)
            console.print(f"[bold green]✓ {strip_res.get('Status')}:[/bold green] [cyan]{strip_res.get('Cleaned File Saved At')}[/cyan]")
        maybe_export("EXIF", path, res)

def handle_url():
    url = Prompt.ask("[bold yellow]Enter URL / Shortened Link (e.g. bit.ly/xxx)[/bold yellow]")
    with Progress(SpinnerColumn(), TextColumn("[cyan]Tracing redirect hops and unshortening URL...[/cyan]"), transient=True) as p:
        p.add_task("trace", total=None)
        res = unshorten_url(url)
    if "error" in res:
        console.print(f"[bold red]✗ Error:[/bold red] {res['error']}")
    else:
        print_result_table(f"URL Trace & Defanging: {url}", res)
        maybe_export("URL", url, res)

def handle_mac():
    mac = Prompt.ask("[bold yellow]Enter MAC Address or Wi-Fi BSSID (e.g. B8:27:EB:00:00:00)[/bold yellow]")
    res = lookup_mac(mac)
    if "error" in res:
        console.print(f"[bold red]✗ Error:[/bold red] {res['error']}")
    else:
        print_result_table(f"MAC / BSSID Hardware Recon: {mac}", res)
        maybe_export("MAC", mac, res)

def main():
    while True:
        console.clear()
        console.print(BANNER)
        console.print(Panel("""[bold white]Select Reconnaissance & Forensics Module:[/bold white]

 [1]  [cyan]Target IP Intelligence & Shodan InternetDB (Open Ports, CVEs, ASN)[/cyan]
 [2]  [cyan]Multi-Engine GeoIP Consensus (Compare Providers & ISP Gateway Radius)[/cyan]
 [3]  [cyan]Inspect Your Public IP & Threat Footprint[/cyan]
 [4]  [cyan]Phone Number Validator, Carrier & Google Dork Recon[/cyan]
 [5]  [cyan]Asynchronous Username Scanner (35+ Categorized Platforms)[/cyan]
 [6]  [cyan]Domain & DNS Intelligence + Subdomain Discovery (crt.sh)[/cyan]
 [7]  [cyan]Email Address Validator, MX Check & Gravatar Profile[/cyan]
 [8]  [cyan]Image EXIF & Metadata Forensics (GPS Extraction & Privacy Stripper)[/cyan]
 [9]  [cyan]URL Unshortener, Redirect Hop Tracer & Link Defanger[/cyan]
 [10] [cyan]MAC Address & Wi-Fi BSSID Hardware Vendor Lookup[/cyan]
 [0]  [red]Exit ZeroTrace[/red]
""", title="[bold green]ZeroTrace Terminal Engine[/bold green]", border_style="cyan", expand=False))

        choice = Prompt.ask("[bold yellow]Select Option[/bold yellow]", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], default="1")
        if choice == "1":
            handle_ip()
        elif choice == "2":
            handle_geoip_consensus()
        elif choice == "3":
            handle_my_ip()
        elif choice == "4":
            handle_phone()
        elif choice == "5":
            handle_username()
        elif choice == "6":
            handle_domain()
        elif choice == "7":
            handle_email()
        elif choice == "8":
            handle_exif()
        elif choice == "9":
            handle_url()
        elif choice == "10":
            handle_mac()
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
