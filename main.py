from terminal_copilot import Gemini
import sys

response = Gemini().generate_response(sys.argv[1:])

