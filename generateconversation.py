import re
import torch
import os
import gtts
import datetime

from transformers import GPT2Tokenizer, GPT2LMHeadModel

index = 1

def generate_dialogue(model, tokenizer, scenario, num_chars=2, max_length=200, top_k=10, top_p=0.9):
    """
    Generate a dialogue between characters based on the given scenario.

    :param model: GPT2LMHeadModel, Pretrained GPT-2 model.
    :param tokenizer: GPT2Tokenizer, Pretrained GPT-2 tokenizer.
    :param scenario: str, Scenario description.
    :param num_chars: int, Number of characters in the dialogue.
    :param max_length: int, Maximum length of the generated text.
    :param top_k: int, Top-k sampling parameter.
    :param top_p: float, Nucleus sampling parameter.
    :return: str, Generated dialogue.
    """

    # Prepare the scenario
    scenario = re.sub(r'[^\w\s]', '', scenario.lower())
    scenario_tokens = tokenizer.encode(f"{scenario} Speaker 1: ", return_tensors="pt")

    # Generate the dialogue
    generated_dialogue = ""
    last_speaker = "1"
    input_ids = scenario_tokens

    for i in range(num_chars - 1):
        # Generate the text for the current speaker
        output = model.generate(
            input_ids,
            max_length=max_length,
            pad_token_id=tokenizer.eos_token_id,
            top_k=top_k,
            top_p=top_p,
            do_sample=True,  # Enable sampling for top-k and top-p
        )

        # Decode the output
        output_text = tokenizer.decode(output[0], skip_special_tokens=True)

        # Find the last speaker's index in the generated text
        last_speaker = predict_next_speaker(output_text, last_speaker)

        # Update the input for the next speaker
        next_speaker_text = f"speaker {last_speaker}: "
        next_speaker_ids = tokenizer.encode(next_speaker_text, return_tensors="pt")
        input_ids = torch.cat((input_ids[0], next_speaker_ids[0][1:]), dim=0)

        # Add the generated text to the dialogue
        generated_dialogue += f"{output_text}\n"

    return generated_dialogue.strip()  # Strip any leading or trailing whitespace

def predict_next_speaker(output_text, last_speaker):
    """
    Predict the next speaker based on the previous speaker's index.

    :param output_text: str, The generated text.
    :param last_speaker: str, The last speaker's index.
    :return: str, The next speaker's index.
    """
    next_speaker = "1" if last_speaker == "2" else "2"
    if output_text.endswith(":"):
        output_text = output_text[:-1]
    next_speaker_index = re.search(rf"speaker {next_speaker}:", output_text)

    if next_speaker_index:
        return next_speaker
    else:
        return last_speaker

def generate_audio(text, conversation_time):
    global index

    # Generate a timestamp
    timestamp = conversation_time.strftime("%Y%m%d_%H%M%S")

    # Create a directory for the current conversation
    conversation_dir = f"conversation_{timestamp}"
    os.makedirs(conversation_dir, exist_ok=True)

    # Create subdirectories for sender and receiver messages
    sender_dir = os.path.join(conversation_dir, "sender_messages")
    receiver_dir = os.path.join(conversation_dir, "receiver_messages")
    os.makedirs(sender_dir, exist_ok=True)
    os.makedirs(receiver_dir, exist_ok=True)

    # Split the dialogue into separate sentences
    sentences = text.split("\n")

    for i, sentence in enumerate(sentences):
        speaker = "speaker 1" if i % 2 == 0 else "speaker 2"
        message_dir = sender_dir if speaker == "speaker 1" else receiver_dir
        if sentence.strip():  # Check if the sentence is not empty
            # Generate audio for each sentence
            tts = gtts.gTTS(text=sentence, lang="en",tld="co.uk", slow=False)
            audio_file_name = f"{speaker}_message_{str(index).zfill(2)}.mp3"
            audio_file_path = os.path.join(message_dir, audio_file_name)
            tts.save(audio_file_path)
            print(f"Audio saved as {audio_file_path}")
            index += 1

def main(scenario):
    # Load the pretrained GPT-2 model and tokenizer
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    # Generate the dialogue
    generated_dialogue = generate_dialogue(model, tokenizer, scenario)

    # Print the generated dialogue
    print(generated_dialogue)

    # Convert the generated text to speech
    current_time = datetime.datetime.now()
    generate_audio(generated_dialogue, current_time)

# Provide the scenario here
scenario = "two friends discussing their favorite sport"

if __name__ == "__main__":
    main(scenario)
