# A terminal chatbot using UF Navigator.
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# Navigator connection settings.
# API key is limited and will be deleted once graded.
API_KEY = "sk-gQyCQFaksVoq3t8vlpcMyQ"
API_URL = "https://api.navigator.ai.ufl.edu/v1/chat/completions"
MODEL = "meta-muse-glimmer-30b"


def get_reply(messages):
    # Send the conversation as JSON, with the API key in the headers.
    data = json.dumps({"model": MODEL, "messages": messages}).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    request = Request(API_URL, data=data, headers=headers)

    # Read the response and return just the chatbot's message.
    with urlopen(request, timeout=120) as response:
        result = json.load(response)
    return result["choices"][0]["message"]["content"]


def main():
    print("Navigator chatbot. Type 'quit' or 'exit' to stop.")
    # Keep the conversation in memory until the program closes.
    messages = []

    try:
        while True:
            # Ignore blank messages and check whether the user wants to exit.
            text = input("You: ").strip()
            if text.lower() in ("quit", "exit"):
                break
            if not text:
                continue

            # Only save this turn after a successful reply.
            conversation = messages + [{"role": "user", "content": text}]
            try:
                reply = get_reply(conversation)
                if not isinstance(reply, str) or not reply.strip():
                    raise ValueError("Empty reply")
            except HTTPError as error:
                print(f"Request failed (HTTP {error.code}). Check your API key and model access.")
                continue
            except (URLError, TimeoutError):
                print("Could not reach Navigator. Please try again.")
                continue
            except (ValueError, KeyError, IndexError, TypeError):
                print("Navigator returned an unexpected reply. Please try again.")
                continue

            print(f"Navigator: {reply}\n")
            messages = conversation + [{"role": "assistant", "content": reply}]
    except (KeyboardInterrupt, EOFError):
        # Exit cleanly if the user presses Ctrl+C or closes input.
        print()
    print("Goodbye!")


if __name__ == "__main__":
    # Start the chat when this file is run directly.
    main()
