
from gtts import gTTS
from mutagen.mp3 import MP3

from reportlab.pdfgen import canvas 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase import pdfmetrics 
from reportlab.lib import colors

import os
import time
import random

import fitz


def create_random_words(): # We will create a list of 1000 most common words in English
    my_list = []
    with open('most_common_1000_words.txt','r') as file:
        for line in file:
            my_list.append(line.strip())
    return my_list


def create_random_pdf():
    
    fileName = 'random_words.pdf'
    documentTitle = 'Random Words Sample'
    title = 'Melih\'s Random Words'
    subTitle = '1000 Random Words'
    
    my_list = []
    
    all_words = create_random_words() # We have a list of 1000 most common words in English
    one_line = ""
    
    for i in range(1000):
        random_word = random.choice(all_words) # We will choose a random word from the list
        one_line += random_word + " "
        if i % 10 == 0: # We will have 100 lines in total
            my_list.append(one_line.strip())
            one_line = ""
        all_words.remove(random_word) # We will remove the word from the list to avoid repetition
        
    my_list.append(one_line.strip())
    #image = 'nature.jpg' # You can add an image to the pdf file
    
    pdf = canvas.Canvas(fileName)
    pdf.setTitle(documentTitle)
    
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdf.setFont("Vera", 36)
    pdf.drawCentredString(300, 770, title)
    
    pdf.setFillColorRGB(0, 0, 255)
    pdf.setFont('Courier-Bold', 24)
    pdf.drawCentredString(290, 720, subTitle)
    
    pdf.line(30, 710, 570, 710)
    
    text = pdf.beginText(40, 680)
    text.setFont("Courier", 16)
    text.setFillColor(colors.red)
    
    text_width = 500
    
    for line in my_list:
        words = line.split()
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if pdf.stringWidth(test_line, "Courier", 16) > text_width: 
                # If the line is too long, write the current line and start a new line
                text.textLine(current_line.strip())
                current_line = word + " "
            else:
                current_line = test_line
        text.textLine(current_line.strip())
    
    pdf.drawText(text) # Write the text to the pdf file
    #pdf.drawInlineImage(image, x=40, y=400, width=100, height=150) # You can add an image to the pdf file
    pdf.save()
    

def read_from_pdf():
    
    #pdf = fitz.open('pdf-test.pdf') # This is another example for reading from a pdf file
    pdf = fitz.open('random_words.pdf')

    text = []
    
    for page_num in range(len(pdf)): # We will read the text from each page
        page = pdf.load_page(page_num)
        page_text = page.get_text()
        page_text = page_text.replace("\n", " ")
        page_text = page_text.strip()
        text.append(page_text)
        
    pdf.close()
    print(text) # You can see the text in the console
    
    language = "en" # You can change the language if you want
    myText = " ".join(text) # We will convert the text to speech
    
    myobj = gTTS(text=myText, lang=language, slow=False) # This could take some time depending on the length of the text
    myobj.save("random_words.mp3") 
    
    os.system("start random_words.mp3") # Play the audio file
    
    audio = MP3("random_words.mp3") 
    
    duration_in_seconds = audio.info.length # Here, we get the duration of the audio file in order to wait for it to be played completely
    duration_in_seconds += 5 # Add 5 seconds to make sure the audio is played completely
    time.sleep(duration_in_seconds) # Wait for the audio to be played, then delete the audio file (optional)
    
    os.remove("random_words.mp3")



def main():
    create_random_pdf()
    read_from_pdf()    
    

if __name__ == '__main__':
    main()

