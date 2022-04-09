# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 15:29:22 2022

@author: Afromullet
"""

import numpy as np
from scipy.io.wavfile import write
from collections import namedtuple
from csv import DictReader
import wave


'''
Stores the samples of a note.
This will serve as a reference to compare the samples of notes played by instruments.
Because it's a reference, it's immutable, and because it's immutable, it's a named tuple instead of a dictionary
'''
Note = namedtuple("Note", "note samples")

'''
A note maps to a symbol
Also immutable, so we use a named tuple instead of a dict
'''
Symbol = namedtuple("Symbol", "note bit")

Ascii_Mappings = namedtuple("Ascii_Mappings", "letter binary")

def read_ascii_table():
    '''
    Reads the ascii table, placing the letter and binary value into the Ascii_Mappings named tuple
    '''
    fh = open("asciitable.csv")
    ascii_csv_file = DictReader(fh)
    
    ascii_mappings = []
    for ascii_value in ascii_csv_file:
        ascii_mappings.append(  Ascii_Mappings(ascii_value['letter'], ascii_value['binary']) )
    return ascii_mappings


def get_wave(freq,fs=44100,duration=0.5):
    '''
    Self explanatory
    '''
    amplitude = 4096
    t = np.linspace(0, duration, int(fs * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    
    return wave

def get_piano_notes():
    '''
    Returns a dict object for all the piano 
    note's frequencies
    '''
    # White keys are in Uppercase and black keys (sharps) are in lowercase
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B'] 
    base_freq = 261.63 #Frequency of Note C4
    
    note_freqs = {octave[i]: base_freq * pow(2,(i/12)) for i in range(len(octave))}        
    note_freqs[''] = 0.0 # silent note
    
    return note_freqs
  

def create_binary_from_ascii_letter(letter,mapping_table):
    '''
    Gets the binary representation of an ascii letter
    '''
    return [value.binary for value in mapping_table if value.letter == letter]  


def convert_letter_to_notes(letter,symbol_list,a_mappings,bits_per_symbol):
    '''
    Returns the notes required for a letter
    I.E, Binary representation of A = 01000001
    A note is mapped to a symbol..i.i CSharp = 00 and an ASharp = 11
    Returns the note and the samples associated with that note
    We're using a generator because we don't want to return a ridiculous number of samples at once
    '''
    binary = create_binary_from_ascii_letter(letter,a_mappings)

    if len(binary):
        binary = ''.join((map(str,binary)))
  
        for i in range(len(binary)-(bits_per_symbol-1)):    
            symbol = [value.note for value in symbol_list if value.bit == binary[i:i+bits_per_symbol]] 
            yield symbol[0]
     
def write_message_to_wav(msg,a_table,symbols,fname,bits_per_symbol,fs=44100):
    
    f = wave.open(fname + ".wav", "w")
    f.setnchannels(1)
    f.setsampwidth(2)   # 2 bytes per sample.
    f.setframerate(fs)
    for letter in msg:
       
        symbol_generator = convert_letter_to_notes(letter,symbols,a_table,bits_per_symbol)
        audio = []        
        for val in symbol_generator:
            audio = val.samples * (16300/np.max(val.samples)) # Adjusting the Amplitude     
            f.writeframes(audio.astype(np.int16).tobytes())
    f.close()
            
'''
Test data

'''
a_table = read_ascii_table()
message = "The The The in a thing a the"
all_notes = get_piano_notes()

Note_C = Note("C",get_wave(all_notes['C']))
Note_A = Note("A",get_wave(all_notes['A']))
Note_D = Note("D",get_wave(all_notes['D']))
Note_E = Note("E",get_wave(all_notes['E']))

Symbol_0 = Symbol(Note_C,"00")
Symbol_1 = Symbol(Note_A,"10")
Symbol_2 = Symbol(Note_D,"01")
Symbol_3 = Symbol(Note_E,"11")

symbols = [Symbol_0,Symbol_1,Symbol_2,Symbol_3]


write_message_to_wav(message,a_table,symbols,"testfile",2)