#!/usr/bin/env python3

import datetime
import json
import random
import textwrap
import traceback
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
    p1 = actor(person1, "red")
    p2 = actor(person2, "green")
    p1.print_wait()
    scene = p1.next_scene()
    with open(f"convo-{p1.name}-{p2.name}-{datetime.datetime.now()}.json", "w") as output:
        write_scene(scene, output)
        print(f"{p1.name}: [{p1.color}]{textwrap.fill(str(scene), width=80)}[/{p1.color}]")
        while True:
            p2.print_wait()
            scene = p2.next_scene(scene)
            write_scene(scene, output)
            print(f"{p2.name}: [{p2.color}]{textwrap.fill(str(scene), width=80)}[/{p2.color}]")
            p2, p1 = p1, p2

def wrap(msg):
    return textwrap.fill(str(msg), width=80) + "\n"

def write_scene(scene, output):
    output.write(f"{scene}\n")
    output.flush()

def gremlin(description, color="red"):
    gremllm = Gremllm(description, model=model_version)
    return Gremlin(gremllm, str(gremllm.name), color)

def actor(description, color="red"):
    gremllm = Gremllm(description, model=model_version)
    return Actor(gremllm, str(gremllm.name), color)

class Gremlin(NamedTuple):
    gremlin: Gremllm
    name: str
    color: str
    def print_wait(self):
        print(f"waiting for [{self.color}]{self.name}[/{self.color}]...")

class Actor(Gremlin):
    def next_scene(self, previous_scene: str = None):
        scene = self.gremlin.next_scene_actor_line_emotion_and_gesture_json(self.name, previous_scene)
        print(scene)
        if "Error executing code" in scene:
            print("trying again")
            return self.next_scene(previous_scene)
        if isinstance(scene, dict):
            return scene
        return json.loads(scene)

def check_quit(cmd, msg):
    if cmd == "quit":
        print(msg)
        exit(0)

if __name__ == "__main__":
    try:
        app()
    except Exception:
        traceback.print_exc()
