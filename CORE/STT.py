import playsound as p
import speech_recognition as sr

# Record Audio
r = sr.Recognizer()


def listen_and_decode():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        p.playsound("DATA-FOLDER/RESPONSE DATA/sigdevoice.wav")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return ["ERROR", ["Sorry, Could not understand!"]]
    except sr.RequestError:
        return ["ERROR", ["Could not connect to STT servers!"]]


if __name__ == "__main__":
    print(listen_and_decode())
