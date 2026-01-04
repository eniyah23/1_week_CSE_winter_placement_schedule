import os
from dotenv import load_dotenv

from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from elevenlabs.types import ConversationConfig

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

AGENT_ID = os.getenv("AGENT_ID")
API_KEY = os.getenv("API_KEY")

# --------------------------------------------------
# User context configuration
# --------------------------------------------------
user_name = "Alex"
schedule = "Sales Meeting with Taipy at 10:00; Gym with Sophie at 17:00"

prompt = f"You are a helpful assistant. Your interlocutor has the following schedule: {schedule}."
first_message = f"Hello {user_name}, how can I help you today?"

conversation_override = {
    "agent": {
        "prompt": {
            "prompt": prompt,
        },
        "first_message": first_message,
    },
}

config = ConversationConfig(
    conversation_config_override=conversation_override,
    extra_body={},
    dynamic_variables={},
)

# --------------------------------------------------
# Callback functions
# --------------------------------------------------
def print_agent_response(response):
    print(f"Agent: {response}")

def print_interrupted_response(original, corrected):
    print(f"Agent interrupted. Corrected response: {corrected}")

def print_user_transcript(transcript):
    print(f"User: {transcript}")

# --------------------------------------------------
# Initialize ElevenLabs client
# --------------------------------------------------
client = ElevenLabs(api_key=API_KEY)

conversation = Conversation(
    client=client,
    agent_id=AGENT_ID,
    config=config,
    requires_auth=True,
    audio_interface=DefaultAudioInterface(),
    callback_agent_response=print_agent_response,
    callback_agent_response_correction=print_interrupted_response,
    callback_user_transcript=print_user_transcript,
)

# --------------------------------------------------
# Start the voice assistant
# --------------------------------------------------
conversation.start_session()
