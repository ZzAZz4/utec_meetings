from dataclasses import dataclass
import json

@dataclass
class Credentials:
    email: str
    password: str
    
    @staticmethod
    def from_file(filename):
        with open(filename, "r") as file:
            obj = json.load(file)
            email, password = obj['email'], obj['password']
            return Credentials(email, password)
 