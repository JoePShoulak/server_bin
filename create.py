import questionary

# Prompt for input
name = questionary.text("What is your name?").ask()

# Prompt for a selection
color = questionary.select(
    "What is your favorite color?",
    choices=['Red', 'Blue', 'Green']
).ask()

print(f"Hello {name}, your favorite color is {color}.")
