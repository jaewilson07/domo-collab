from dataclasses import  dataclass, field
from typing import List

@dataclass
class Message:
    role: str
    content : str
    
    def to_json(self):
        return {"role":  self.role, "content":  self.content}
    
    def generate_context(self):
        return f"{self.role} : {self.content}"

@dataclass
class Messages:
    messages : List[Message] = field(default_factory = [])
    
    @classmethod
    def from_system_prompt(cls, filename: str = './prompts/chatbot.txt'):
        with open(filename, "r") as f:
            return cls([Message("SYSTEM", f.read())])
    
    def add_message(self, message : Message):
        if isinstance(message, str):
            message = Message('USER', message)
            
        self.messages.append(message)
        return self.messages
        
    def generate_context(self, text_input : str = None):
        
        if text_input:
            self.add_message(Message("USER" , text_input))
        
        return "\n".join([msg.generate_context() for msg in self.messages])

    def to_json(self):
        return [msg.to_json() for msg in self.messages]