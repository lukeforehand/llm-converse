#!/usr/bin/env python3

import datetime
import json
import textwrap
import typer

from gremllm import Gremllm
from rich import print
from rich.prompt import Prompt
from typing import NamedTuple

model_version = "anthropic/claude-3-5-sonnet-20241022"

app = typer.Typer(add_completion=False)

@app.command()
def play_text_adventure(description: str):
    print("loading")
    game = gremlin(description, "green")
    description = game.gremlin.description()
    while True:
        cmd = Prompt.ask(wrap(f"[{game.color}]{description}[/{game.color}]"))
        check_quit(cmd, "exiting game")
        print(f"thinking...")
        description = game.gremlin.next_state(cmd)

@app.command()
def start_conversation(person: str):
    print("loading")
    person = gremlin(person, "red")
    answer = f"[{person.color}]{person.name}[/{person.color}]: What is your question?"
    while True:
        question = Prompt.ask(wrap(answer))
        check_quit(question, "good bye")
        person.print_wait()
        answer = person.gremlin.answer_question(question)

@app.command()
def watch_conversation(person1: str, person2: str):
    print("loading")
    p1 = gremlin(person1, "red")
    p2 = gremlin(person2, "green")
    p1.print_wait()
    words = p1.gremlin.talk()
    print(f"{p1.name}: [{p1.color}]{textwrap.fill(str(words), width=80)}[/{p1.color}]")
    while True:
        p2.print_wait()
        words = p2.gremlin.respond_to(words)
        print(f"{p2.name}: [{p2.color}]{textwrap.fill(str(words), width=80)}[/{p2.color}]")
        p2, p1 = p1, p2

def wrap(msg):
    return textwrap.fill(str(msg), width=80) + "\n"

def gremlin(description, color="red"):
    gremllm = Gremllm(description, model=model_version)
    return Gremlin(gremllm, gremllm.name, color)

class Gremlin(NamedTuple):
    gremlin: Gremllm
    name: str
    color: str
    def print_wait(self):
        print(f"waiting for [{self.color}]{self.name}[/{self.color}]...")

def check_quit(cmd, msg):
    if cmd == "quit":
        print(msg)
        exit(0)

if __name__ == "__main__":
    app()