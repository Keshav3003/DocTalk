from tkinter import *
import tkinter.messagebox as mb
from path import Path
from PyPDF4.pdf import PdfFileReader as PDFreader, PdfFileWriter as PDFwriter
import pyttsx3
from speech_recognition import Recognizer, AudioFile
from pydub import AudioSegment
import os


# Initializing the GUI window
class Window(Tk):
    def __init__(self):
        super(Window, self).__init__()
        self.title("DocTalk")
        self.geometry('1280x720')
        self.resizable(0, 0)
        self.config(bg='#F8DFD4')

        Label(self, text='PROJECT DOCTALK', wraplength=400,
              bg='Burlywood', font=("Times New Roman", 18) , height=5 , width = 35).place(x=420, y=50)

        Button(self, text="Convert PDF to Audio", font=("Comic Sans MS", 15), bg='Tomato',
               command=self.pdf_to_audio, width=50).place(x=350, y=250)

        Button(self, text="Convert Audio to PDF", font=("Comic Sans MS", 15), bg='Tomato',
               command=self.audio_to_pdf, width=50).place(x=350, y=350)
        
        Button(self, text="Credits", font=("Comic Sans MS", 15), bg='Tomato',
               command=self.credit, width=50).place(x=350, y=450)
        
    def credit(self):
        pta = Toplevel(self)
        pta.title('Credit To The Developers')
        pta.geometry('1280x720')
        pta.resizable(0, 0)
        pta.config(bg='#F8DFD4')

        Label(pta, text='MADE BY', font=('Times New Roman', 18), bg='Burlywood', height=5 , width = 32).place(x=450, y=50)

        Label(pta, text='Keshav Prakash Sharma (2K21/CO/238) ', bg='Chocolate', font=("Verdana", 11), height=5 , width=47).place(
            x=450, y=250)

        Label(pta, text='Kunal (2K21/CO/248)', bg='Chocolate',
              font=("Verdana", 11), height=5,width = 47).place(x=450, y=350)
        
        Label(pta, text='Krishnanshu Bansal (2K21/CO/244) ', bg='Chocolate',
              font=("Verdana", 11), height=5,width = 47).place(x=450, y=450)
        
        Label(pta, text='Lakshay Dabas (2K21/CO/254) ', bg='Chocolate',
              font=("Verdana", 11), height=5,width = 47).place(x=450, y=550)


    def pdf_to_audio(self):
        pta = Toplevel(self)
        pta.title('Convert PDF to Audio')
        pta.geometry('1280x720')
        pta.resizable(0, 0)
        pta.config(bg='#F8DFD4')

        Label(pta, text='Convert PDF to Audio', font=('Times New Roman', 18), bg='Burlywood', height=5 , width = 35).place(x=450, y=50)

        Label(pta, text='Enter the PDF file location (with extension): ', bg='Chocolate', font=("Verdana", 11)).place(
            x=400, y=250)
        filename = Entry(pta, width=32, font=('Verdana', 11))
        filename.place(x= 400, y=290)

        Label(pta, text='Enter the page to read from the PDF (only one can be read): ', bg='Chocolate',
              font=("Verdana", 11)).place(x=400, y=350)
        page = Entry(pta, width=15, font=('Verdana', 11))
        page.place(x=400, y=390)

        Button(pta, text='Click Here To Speak the text', font=('Gill Sans MT', 15), bg='#637E76', width=40,height=5,
               command=lambda: self.speak_text(filename.get(), page.get())).place(x=450, y=450)

    def audio_to_pdf(self):
        atp = Toplevel(self)
        atp.title('Convert Audio to PDF')
        atp.geometry('1280x720')
        atp.resizable(0, 0)
        atp.config(bg='#F8DFD4')

        Label(atp, text='Convert Audio to PDF', font=('Times New Roman', 18), bg='Burlywood',width=40,height=5).place(x=450, y=50)

        Label(atp, text='Enter the Audio File location that you want to read [in .wav or .mp3 extensions only]:',
              bg='Chocolate', font=('Verdana', 11)).place(x=400, y=250)
        audiofile = Entry(atp, width=58, font=('Verdana', 11))
        audiofile.place(x=400, y=290)

        Label(atp, text='Enter the PDF File location that you want to save the text in (with extension):',
              bg='Chocolate', font=('Verdana', 11)).place(x=400, y=350)
        pdffile = Entry(atp, width=58, font=('Verdana', 11))
        pdffile.place(x=400, y=390)

        Button(atp, text='Create PDF', bg='Green', font=('Gill Sans MT', 15),width=40,height=5,
               command=lambda: self.speech_recognition(audiofile.get(), pdffile.get())).place(x=500, y=450)

    @staticmethod
    def speak_text(filename, page):
        if not filename or not page:
            mb.showerror('Missing field!', 'Please check your responses, because one of the fields is missing')
            return

        reader = PDFreader(filename)
        engine = pyttsx3.init()

        with Path(filename).open('rb'):
            page_to_read = reader.getPage(int(page) - 1)
            text = page_to_read.extractText()

            engine.say(text)
            engine.runAndWait()

    @staticmethod
    def write_text(filename, text):
        writer = PDFwriter()
        writer.addBlankPage(72, 72)

        pdf_path = Path(filename)

        with pdf_path.open('ab') as output_file:
            writer.write(output_file)
            output_file.write(text)

    def speech_recognition(self, audio, pdf):
        if not audio or not pdf:
            mb.showerror('Missing field!', 'Please check your responses, because one of the fields is missing')
            return

        audio_file_name = os.path.basename(audio).split('.')[0]
        audio_file_extension = os.path.basename(audio).split('.')[1]

        if audio_file_extension != 'wav' and audio_file_extension != 'mp3':
            mb.showerror('Error!', 'The format of the audio file should only be either "wav" and "mp3"!')

        if audio_file_extension == 'mp3':
            audio_file = AudioSegment.from_file(Path(audio), format='mp3')
            audio_file.export(f'{audio_file_name}.wav', format='wav')

        source_file = f'{audio_file_name}.wav'

        r = Recognizer()
        with AudioFile(source_file) as source:
            r.pause_threshold = 5
            speech = r.record(source)

            text = r.recognize_google(speech)

            self.write_text(pdf, text)


# Finalizing the GUI window
app = Window()

app.update()
app.mainloop()