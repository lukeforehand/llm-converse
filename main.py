#!/usr/bin/env python3

import textwrap
import typer

from gremllm import Gremllm as Gremlin
from rich import print
from rich.prompt import Prompt

model_version = "anthropic/claude-3-5-sonnet-20241022"

app = typer.Typer(add_completion=False)

@app.command()
def play_text_adventure(game_description: str):
    color = "green"
    game = Gremlin(f"text adventure with description: {game_description}", model=model_version)
    description = game.description()
    while True:
        cmd = Prompt.ask(prompt(f"[{color}]{description}[/{color}]"))
        if cmd == "quit":
            print("exiting game")
            break
        print(f"thinking...")
        description = game.next_state(cmd)


@app.command()
def start_conversation(person: str):
    color = "red"
    person = Gremlin(person, model=model_version)
    name = person.name
    answer = f"[{color}]{name}[/{color}]: What is your question?"
    while True:
        question = Prompt.ask(prompt(answer))
        if question == "quit":
            print("good bye")
            break
        print(f"[{color}]{name}[/{color}] is thinking...")
        answer = person.answer_question(question)
    

@app.command()
def watch_conversation(person1: str, person2: str): 
    color1 = "red"
    color2 = "green"
    person1 = Gremlin(person1, model=model_version)
    person2 = Gremlin(person2, model=model_version)
    name1 = person1.name
    name2 = person2.name
    print(f"waiting for [{color1}]{name1}[/{color1}] to talk...")
    words = person1.talk()
    print(f"{name1}: [{color1}]{textwrap.fill(str(words), width=80)}[/{color1}]")
    while True:
        print(f"waiting for a response from [{color2}]{name2}[/{color2}]...")
        words = person2.respond_to(words)
        print(f"{name2}: [{color2}]{textwrap.fill(str(words), width=80)}[/{color2}]")
        color2, color1 = color1, color2
        person2, person1 = person1, person2
        name2, name1 = name1, name2

def prompt(msg):
    return textwrap.fill(str(msg), width=80) + "\n"

if __name__ == "__main__":
    app()