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
import random

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


def get_wave(freq,fs=44100,duration=0.1):
    '''
    Self explanatory
    '''
    amplitude = 4096
    t = np.linspace(0, duration, int(fs * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    
    return wave

def get_piano_notes(base_freq):
    '''
    Returns a dict object for all the piano 
    note's frequencies
    '''
    # White keys are in Uppercase and black keys (sharps) are in lowercase
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B'] 
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
    A note is mapped to a symbol..i.i FSharp = 00 and an A = 11
    Returns the note and the samples associated with that note
    We're using a generator because we don't want to return a ridiculous number of samples at once
    '''
    binary = create_binary_from_ascii_letter(letter,a_mappings)

    if len(binary):
        binary = ''.join((map(str,binary)))
  
        for i in range(len(binary)-(bits_per_symbol-1)):    
            symbol = [value.note for value in symbol_list if value.bit == binary[i:i+bits_per_symbol]] 
            yield symbol[0]
     
def write_message_to_wav(msg,a_table,symbols,fname,bits_per_symbol,bytes_per_sample,fs=44100):
    
    f = wave.open(fname + ".wav", "w")
    f.setnchannels(1)
    f.setsampwidth(bytes_per_sample)   # 2 bytes per sample.
    f.setframerate(fs)
    for letter in msg:
       
        symbol_generator = convert_letter_to_notes(letter,symbols,a_table,bits_per_symbol)
        audio = []        
        for val in symbol_generator:
            audio = val.samples * (16300/np.max(val.samples)) # Adjusting the Amplitude     
            f.writeframes(audio.astype(np.int16).tobytes())
    f.close()
    
    
def read_message_from_wav(fname):
    
    obj = wave.open(fname + ".wav",'r')
    print( "Number of channels",obj.getnchannels())
    print ( "Sample width",obj.getsampwidth())
    print ( "Frame rate.",obj.getframerate())
    print ("Number of frames",obj.getnframes())
    print ( "parameters:",obj.getparams())
    a = obj.getnframes()
    print(a)
    obj.close()
    
    
def basic_message_example():
    C4_freq = 261.63
    B4_freq = 493.88
    
    fname = "testfile1"
    a_table = read_ascii_table()
    message = "I cast a fireball"
    C4_Octave = get_piano_notes(C4_freq)
    B4_Octave = get_piano_notes(B4_freq)
    

    symbols = [
    Symbol( Note("A",get_wave(C4_Octave['A'])),"0000"),
    Symbol( Note("B",get_wave(C4_Octave['B'])),"0001"),
    Symbol( Note("C",get_wave(C4_Octave['C'])),"0010"),
    Symbol( Note("D",get_wave(C4_Octave['D'])),"0011"),
    Symbol( Note("A",get_wave(B4_Octave['A'])),"0100"),
    Symbol( Note("B",get_wave(B4_Octave['B'])),"0101"),
    Symbol( Note("C",get_wave(B4_Octave['C'])),"0110"),
    Symbol( Note("D",get_wave(B4_Octave['D'])),"0111"),
    Symbol( Note("E",get_wave(C4_Octave['E'])),"1000"),
    Symbol( Note("F",get_wave(C4_Octave['F'])),"1001"),
    Symbol( Note("G",get_wave(C4_Octave['G'])),"1010"),
    Symbol( Note("E",get_wave(B4_Octave['E'])),"1011"),
    Symbol( Note("F",get_wave(B4_Octave['F'])),"1100"),
    Symbol( Note("G",get_wave(B4_Octave['G'])),"1101"),
    Symbol( Note("a",get_wave(C4_Octave['a'])),"1110"),
    Symbol( Note("a",get_wave(B4_Octave['a'])),"1111")
    ]
    
    write_message_to_wav(message,a_table,symbols,fname,4,2)
    read_message_from_wav(fname)
    
    
def create_random_symbol_groups(base_freq_1,base_freq_2):
    
    '''
    Uses 4 symbols per bit. Breaks down the symbols into two groups, each associated with a different octave
    Selects a random note from that octave and maps it to a symbol.
    Returns the symbol list
    '''
    symbol_sets = [["0000","0001","0010","0011","0100", "0101","0110","0111"],[ "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"]]
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B'] 
    note_frequencies = [get_piano_notes(base_freq_1),get_piano_notes(base_freq_2)] #List of lists, where each sublist are all the octaves of a base frequency

    symbols = [] 
    for i,symbol_set in enumerate(symbol_sets):
        #Creates a list of random indices for a symbol set. The index will be used to select a random note. 
        random_indices = random.sample(range(len(symbol_set)),len(symbol_set))
        for j,rand_num in enumerate(random_indices):
            random_octave = octave[rand_num]
            current_symbol = symbol_set[j]
            symbol =  Symbol(
                Note(random_octave,get_wave(note_frequencies[i][random_octave])),
                symbol_set[j])
            symbols.append(symbol)
       
    return symbols
    
'''
Test data

'''

symbols = create_random_symbol_groups(261.63,493.88)

fname = "testfile1"
a_table = read_ascii_table()
message = "I cast a fireball"
write_message_to_wav(message,a_table,symbols,fname,bits_per_symbol=4,bytes_per_sample=2)
#basic_message_example()