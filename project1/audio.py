#1 import everything we need


##1##

import os
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import openai
from dotenv import load_dotenv




##2##

#setting up the app to work

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load Whisper model
model = whisper.load_model("small")

# Global flag to stop recording
stop_recording = False

##3##

#function to record audio until Enter is pressed




##saves file name of recorded audio under temp.wae and fs 44100 is the sampling frequency
##setsup the variable gloabl so we can use it in the callback function
##starts a list to store audio data chunks
def record_audio_until_enter(filename="temp.wav", fs=44100):
    global stop_recording
    stop_recording = False
    audio_data = []


    # Callback function to capture audio data. has four parameters.
    # indata: the recorded audio data.
    #  frames: number of frames.
    #  time: timestamp info.
    #  status: any errors or warnings.
    # If status is not None, it prints the status.
    # Appends a copy of indata to audio_data list. audio data is a list that stores chunks of recorded audio.
    # If stop_recording is True, raises sd.CallbackStop to stop the recording.
    #raises means it will stop the recording when the user presses Enter.
    #sd.CallbackStop is a special exception that tells the sounddevice library to stop the audio stream.


#our cllback function we get back to it a lot of times so we proccess the audio chunks and 
##add them to audio data list. when user hits enter in the func below it stops the recording
## and raises the exception to stop the stream which is the if statement below

    def callback(indata, frames, time, status):
        if status:
            print(status)
        audio_data.append(indata.copy())
        if stop_recording:
            raise sd.CallbackStop()
        



#our function the records but doesnt do proccesing it send all th audio chunks to the callback function
#it uses the sounddevice library to create an input stream with the specified sample rate and number of channels
#it prints a message to the user to start reciting from the book of Allah
#it waits for the user to press Enter to stop the recording
#when Enter is pressed it sets the stop_recording flag to True which will trigger the callback function to stop the recording
#after the recording is stopped it concatenates all the audio chunks into a single numpy array
# it saves it in audio_data list
    with sd.InputStream(samplerate=fs, channels=1, callback=callback):
        print("Recite from the Book of Allah...")
        input()  # Wait until user presses Enter
        stop_recording = True




    # Convert list to array and save as WAV
    audio_np = np.concatenate(audio_data, axis=0)
    write(filename, fs, audio_np)
    print("Recording stopped and saved!")
    return filename

##take every chunck in the audio data list and concatenate them into a single numpy array
## called audio np. then take it and save it as filename which is temp.wav
##fs is the sampling frequency we set earlier which is 44100





##4##

#function to transcribe audio using Whisper


def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]



##transcribe audio in the file path using the whisper model we loaded earlier which is 
## filepath is just aplaceholder we are going to use later on and put or actual file name in it. it returns the transcribed text from the audio
## return the resutl as text




##5##

#fnction to ask GPT a question and get a response


def ask_gpt(question):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Ibn Kathir. Respond by transcribing the ayah into English in the first line. In the second line, say which surah it is, its number, and the ayah number(s). In the third and fourth lines, give a tafsir summary of the ayah/ayas from Ibn Kathir."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content




## question is the input we get from the user which is the transcribed text from the audio
## it sends the question to the openai chat completion endpoint using the gpt-4 model
## it formats the question as a message with the role of user




##6##

#main loop to run the app


if __name__ == "__main__":
    print("Mic Transcription + GPT Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        cmd = input("Press Enter to record, or type 'exit': ").strip()
        if cmd.lower() == "exit":
            break

        audio_file = record_audio_until_enter()
        text = transcribe_audio(audio_file)
        print(f"Transcribed Text: {text}")

        answer = ask_gpt(text)
        print(f"Assistant: {answer}\n")

### it prints a welcome message and instructions to the user
### if user preses on enter in cmd it calls the record audio function to start recording
###if user types exit it exits the app
###  if user clicks on enter a file named temp.wav is created and the audio is recorded until user presses enter again
### audio is then saved in audio data which is then saved as after concanetation audio.np 
# and then audio np is saved as temp.wav
### then the transcribe audio function is called with the audio file path as argument
### the text variable stores the transcribed text from the audio
### it prints the transcribed text to the console
### then it calls the ask gpt function with the transcribed text as argument
### the answer variable stores the response from gpt
### it prints the assistant's response to the console