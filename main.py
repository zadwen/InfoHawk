import inquirer
from rich.console import Console
from modules import usernames, emailintel, phonelookup, domainrecon, socialscan, leaksearch

console = Console()

def main():
    console.print("[bold blue]Welcome to InfoHawk OSINT Tool[/bold blue] 🦅")

    questions = [
        inquirer.List(
            "module",
            message="Choose a module to run",
            choices=[
                "1. Username Discovery",
                "2. Email Intelligence",
                "3. Phone Number Lookup",
                "4. Domain & IP Recon",
                "5. Social Media Scanner",
                "6. Leak & Pastebin Search",
                "0. Exit"
            ],
        ),
    ]
    
    answers = inquirer.prompt(questions)
    choice = answers["module"]

    if choice.startswith("1"):
        usernames.run()
    elif choice.startswith("2"):
        emailintel.run()
    elif choice.startswith("3"):
        phonelookup.run()
    elif choice.startswith("4"):
        domainrecon.run()
    elif choice.startswith("5"):
        socialscan.run()
    elif choice.startswith("6"):
        leaksearch.run()
    else:
        console.print("Goodbye! 👋")

if __name__ == "__main__":
    main()
