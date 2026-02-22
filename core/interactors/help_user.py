from typing import List
import json

from core.interfaces.terminal import ITerminal
from core.interfaces.llm_responder import ILLMResponder
from domain.entities.chat_element import ChatElement
from domain.entities.request import Request
from domain.entities.response import Response

class HelpUser:
    def __init__(self, terminal: ITerminal, llm_responder: ILLMResponder):
        self.terminal = terminal
        self.llm_responder = llm_responder
        self.memory: List[ChatElement] = []

    def prompt_template(self) -> str:
        return f"""
        Hello, you are a professional and smart AI agent for all general
        purpose tasks for your users PC. You can give three types of responses.
        All must be strictly in JSON format wrapped without anything like ``` or
        something similar. It must be parsable into JSON.

        You can use the terminal for achieving users desire and also you can
        continue working from terminal's feedback on your own. Remember every
        time you will use the terminal, the next response will be from the terminal
        not the user. It will also be given you in the prompt who is making the
        request anyway.

        the JSON will have these values
            type: str       # one of "terminal", "response" or "exit"
            body: str       # main body of response
            command: str    # command if the type is terminal

        When type == "terminal":
        - body MUST be an empty string
        - command MUST be a complete, executable command
        - NEVER explain what the command does
        - NEVER instruct the user

        If the user's request requires any real-world action
        (files, folders, programs, system state),
        YOU MUST respond with type = "terminal".

        Using type = "response" is FORBIDDEN
        until all required terminal actions are completed.

        If the user's request is clear and achievable,
        execute ALL required terminal commands autonomously
        until the task is complete.

        DO NOT ask for confirmation.
        DO NOT show users command steps to explain. The user is non-technical guy
        DO NOT wait for the user between steps.
        NEVER give a response while retrying. Using response while retrying
        will hamper everything and ask for prompt from the user

        The terminal is a windows Command Prompt (cmd) (not Linux or WSL)
        The terminal is stateless.
        Each command runs independently.
        Always use absolute paths.
        Never rely on `cd`.

        Past Conversation Memory:
        {self.format_memory()}

        Prompt:
        """
    
    def format_memory(self):
        lines = []
        for m in self.memory:
            if isinstance(m, Request):
                lines.append(f"{m.maker.upper()}: {m.body}") # type: ignore
            elif isinstance(m, Response):
                if m.type == "terminal":
                    lines.append(f"AGENT → TERMINAL: {m.command}") # type: ignore
                else:
                    lines.append(f"AGENT: {m.body}") # type: ignore
        return "\n".join(lines)

    def ask_user_for_prompt(self) -> str:
        print("You: ", end="")
        prompt = input("")
        self.memory.append(Request("user", prompt))
        return prompt
    
    def help(self):
        print("Hello, How can I help you?")
        mode = "ask"
        while True:
            if mode == "ask":
                prompt = self.ask_user_for_prompt()
            else:
                prompt = "no prompt. continue pending task"
            prompt = self.prompt_template() + prompt
            response = self.llm_responder.ask(prompt)
            try:
                response_json_content = json.loads(response)
                #print(response_json_content)
                response_element = Response(
                    response_json_content["type"],
                    response_json_content["body"],
                    response_json_content["command"],    
                )
                self.memory.append(response_element)
                if response_json_content["type"] == "terminal":
                    print("Running...")
                    print(response_element.command)
                    terminal_response = self.terminal.execute(response_element.command)
                    request_element = Request(
                        "terminal",
                        str(terminal_response),
                    )
                    self.memory.append(request_element)
                    mode = "pending"
                elif response_json_content["type"] == "response":
                    print("Agent47:", response_json_content["body"])
                    mode = "ask"
                else:
                    mode = "pending"
            except:
                request_element = Request(
                    "error",
                    str("There were error parsing the last JSON message"),
                )
                self.memory.append(request_element)
                mode = "pending"


            #print(self.memory)   
            #print(response_json_content)
