import questionary

# Prompt for input
server_name = questionary.text("Server name: ").ask()
port = questionary.text("Port: ").ask()
version = questionary.text("Version: ").ask()


# Prompt for a selection
# color = questionary.select(
#     "What is your favorite color?",
#     choices=['Red', 'Blue', 'Green']
# ).ask()

