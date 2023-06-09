import openai
from elevenlabs import generate, play
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
import base64
from voice import get_voices


openai.api_key = os.getenv("OPENAI_API_KEY")


#may need to use response from POST 

# audio = generate(
#   text="Hi! My name is Bella, nice to meet you!",
#   voice="Bella",
#   model="eleven_monolingual_v1"
# )

# play(audio)

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    # Here's a class function
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        """Handles GET requests to the server
        """
        # Set the response code to 'Ok'
        self._set_headers(200)

        # Your new console.log() that outputs to the terminal
        print(self.path)

        # It's an if..else statement
        if self.path == "/chat":
            # In Python, this is a list of dictionaries
            # In JavaScript, you would call it an array of objects
            response = [
                {"id": 1, "name": "Snickers", "species": "Dog"},
                {"id": 2, "name": "Lenny", "species": "Cat"}
            ]

        else:
            response = []

        # This weird code sends a response back to the client
        self.wfile.write(f"{response}".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    
    def do_POST(self):
        """Handles POST requests to the server
        """
        # Set response code to 'Created'
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)
        if self.path == "/chat":
            # send user input
            # put input into array


            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=post_body, temperature=1.4)
            print(completion.choices[0].message.content)
            answer = completion.choices[0].message.content
            audio = get_voices(answer)

            # Convert audio bytes to a base64 encoded string
            audio_base64 = base64.b64encode(audio)

            # Decode the base64 encoded string to get a regular string
            audio_string = audio_base64.decode()

            response = {"content": answer, "audio": audio_string}
            self.wfile.write(json.dumps(response).encode())
            # self.wfile.write(response.encode())



    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    def do_PUT(self):
        """Handles PUT requests to the server
        """
        self.do_POST()


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
