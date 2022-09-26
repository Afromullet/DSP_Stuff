# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 15:29:22 2022

@author: Afromullet
"""

import numpy as np
from collections import namedtuple
from csv import DictReader,writer
import wave
import random
import struct
import scipy
from scipy import signal
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfilt
from itertools import zip_longest




'''
DEBUG NOTES

Writes the correct frequencies to the file

Does not read the correct frequencies in. Read in too many frequencies


'''


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
Symbol = namedtuple("Symbol", "note bit freq")

Ascii_Mappings = namedtuple("Ascii_Mappings", "letter binary")

'''
Knowing the symbol duration lets us know how large our FFT slices should be
'''
Encoding_Params = namedtuple("Encoding_Params", "fs symbol_duration")



def grouper(iterable, n, fillvalue=None):
    '''
    grouper('ABCDEFG', 3, 'x')  # --> 'ABC' 'DEF' 'Gxx'

    '''
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

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
    Returns a dict object for all the piano note's frequencies
    '''
    # White keys are in Uppercase and black keys (sharps) are in lowercase
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B'] 
    note_freqs = {octave[i]: base_freq * pow(2,(i/12)) for i in range(len(octave))}        
    #note_freqs[''] = 0.0 # silent note todo figure out whether there's an impact for removing this
    
    return note_freqs
  

def create_binary_from_ascii_letter(letter,mapping_table):
    '''
    Gets the binary representation of an ascii letter
    '''
    return [value.binary for value in mapping_table if value.letter == letter]  


def get_ascii_from_binary(binary,mapping_table):
    '''
    Gets the ascii letter of a byte
    '''
    
    for value in mapping_table:
        
        if value.binary == binary:
            return value

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
        
        
        #Doing some extra work now by combining the string, then splitting it into chunks. Those steps can be combined in the future once things work todo
       
        binary = ''.join((map(str,binary))) #Originally a list and we want a string..Todo just use binary[0] in the future
        binary = grouper(binary,bits_per_symbol)
        
        for sym in binary:
            
            #Here is the extra work part where we combine the chunks and the part we have to combine in the future todo
            sym = ''.join((map(str,sym))) 
            symbol = [value.note for value in symbol_list if value.bit == sym]
            yield symbol[0]
     
   
#Added some debug code todo remove later    
def write_message_to_wav(msg,a_table,symbols,fname,bits_per_symbol,bytes_per_sample,fs=44100):
    
    f = wave.open(fname + ".wav", "w")
    f.setnchannels(1)
    f.setsampwidth(bytes_per_sample)   # 2 bytes per sample.
    f.setframerate(fs)
    
    debug_file = open("debug_freqs_written_to_wav.csv","w",newline="") #debug filehandle
    header = ["Binary","Freq"]
    deb_writer = writer(debug_file)
    deb_writer.writerow(header)
    
    num_times_written_to_wav = 0
    for letter in msg:
       
        symbol_generator = convert_letter_to_notes(letter,symbols,a_table,bits_per_symbol)
        audio = []        
        
        
        notes_written_debug = [] #Debug list that keeps tracks of the notes written to the wav file
        for val in symbol_generator:
            
            notes_written_debug.append([val[0],val[1]]) #Storing the samples too...
            audio = val.samples * (16300/np.max(val.samples)) # Adjusting the Amplitude   
            f.writeframes(audio.astype(np.int16).tobytes())
            
            num_times_written_to_wav += 1
            
        
        #Debug stuff in loop below
        out_line = []
        for note in notes_written_debug:
            deb_writer.writerow
            written_freq_data = get_freq_from_note(note,symbols)
            deb_writer.writerow([written_freq_data[1],written_freq_data[2]])
            
           
    deb_writer.writerow(["Num Times written to wav"])   
    deb_writer.writerow([num_times_written_to_wav])  
    f.close()
    debug_file.close()
    
def get_freq_from_note(note,symbols):
    '''
    Gets the frequency of a note
    Returns a list containing [Note, binary, frequency]
    '''
    
    for sym in symbols:
        #Checking if the samples are equal...Not the best way to do it, but this is just something quick for debug
        if note[0] == sym[0][0] and np.array_equal(note[1],sym[0][1]):
            return [note[0],sym[1],sym[2]]
            
 
    return [] #Can't find the symbol. Something really went wrong here
    
    
def read_message_from_wav(fname):
    
    obj = wave.open(fname + ".wav",'r')
    frames = []
    num_frames = obj.getnframes()
    for frame in range(num_frames):
        samples = struct.unpack("<h", obj.readframes(1))
        frames.append(samples[0])
    return frames
   
    
    
def basic_message_example(fname,message):
    octave_1_freq = 161.63
    ocatave_2_freq = 593.88
    
    a_table = read_ascii_table()
 
    octave_1 = get_piano_notes(octave_1_freq)
    octave_2 = get_piano_notes(ocatave_2_freq)
    
    #todo get min and max freq of both octaves think I already did this verify later 
    encoding_params = Encoding_Params((44100), 0.1)
    freq_ranges = [get_symbol_freq_range(octave_1),get_symbol_freq_range(octave_2)]
    
    symbols = [
    Symbol( Note("A",get_wave(octave_1['A'],encoding_params.fs,encoding_params.symbol_duration)),"0000",octave_1['A']),
    Symbol( Note("B",get_wave(octave_1['B'],encoding_params.fs,encoding_params.symbol_duration)),"0001",octave_1['B']),
    Symbol( Note("C",get_wave(octave_1['C'],encoding_params.fs,encoding_params.symbol_duration)),"0010",octave_1['C']),
    Symbol( Note("D",get_wave(octave_1['D'],encoding_params.fs,encoding_params.symbol_duration)),"0011",octave_1['D']),
    Symbol( Note("A",get_wave(octave_2['A'],encoding_params.fs,encoding_params.symbol_duration)),"0100",octave_2['A']),
    Symbol( Note("B",get_wave(octave_2['B'],encoding_params.fs,encoding_params.symbol_duration)),"0101",octave_2['B']),
    Symbol( Note("C",get_wave(octave_2['C'],encoding_params.fs,encoding_params.symbol_duration)),"0110",octave_2['C']),
    Symbol( Note("D",get_wave(octave_2['D'],encoding_params.fs,encoding_params.symbol_duration)),"0111",octave_2['D']),
    Symbol( Note("E",get_wave(octave_1['E'],encoding_params.fs,encoding_params.symbol_duration)),"1000",octave_1['E']),
    Symbol( Note("F",get_wave(octave_1['F'],encoding_params.fs,encoding_params.symbol_duration)),"1001",octave_1['F']),
    Symbol( Note("G",get_wave(octave_1['G'],encoding_params.fs,encoding_params.symbol_duration)),"1010",octave_1['G']),
    Symbol( Note("E",get_wave(octave_2['E'],encoding_params.fs,encoding_params.symbol_duration)),"1011",octave_2['E']),
    Symbol( Note("F",get_wave(octave_2['F'],encoding_params.fs,encoding_params.symbol_duration)),"1100",octave_2['F']),
    Symbol( Note("G",get_wave(octave_2['G'],encoding_params.fs,encoding_params.symbol_duration)),"1101",octave_2['G']),
    Symbol( Note("a",get_wave(octave_1['a'],encoding_params.fs,encoding_params.symbol_duration)),"1110",octave_1['a']),
    Symbol( Note("a",get_wave(octave_2['a'])),"1111",octave_2['a'])
    ]
    
    write_message_to_wav(message,a_table,symbols,fname,4,2)
    read_message_from_wav(fname)
    return symbols,encoding_params,freq_ranges
    
    
def create_random_symbol_groups(base_freq_1,base_freq_2):
    
    '''
    Uses 4 symbols per bit. Breaks down the symbols into two groups, each associated with a different octave
    Selects a random note from that octave and maps it to a symbol.
    Returns the symbol list
    '''
    symbol_sets = [["0000","0001","0010","0011","0100", "0101","0110","0111"],[ "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"]]
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B'] 
    note_frequencies = [get_piano_notes(base_freq_1),get_piano_notes(base_freq_2)] #List of lists, where each sublist are all the octaves of a base frequency

    #todo add frequency argumetn to the symbol init
    symbols = [] 
    for i,symbol_set in enumerate(symbol_sets):
        #Creates a list of random indices for a symbol set. The index will be used to select a random note. 
        random_indices = random.sample(range(len(symbol_set)),len(symbol_set))
        for j,rand_num in enumerate(random_indices):
            random_octave = octave[rand_num]
            symbol =  Symbol(
                Note(random_octave,get_wave(note_frequencies[i][random_octave])),
                symbol_set[j])
            symbols.append(symbol)
       
    return symbols

def get_symbol_freq_range(freq_list):
    
    '''
    Returns the minimum and maximum frequency of the octave.
    Might use more than music notes in the future so we use min and max 
    Instead of defaulting to the start and end note of a scale
    
    '''
    return {"low" : min(freq_list.values()), "high" : max(freq_list.values())}
  
    
  
def butter_bandpass(lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        sos = butter(order, [low, high], analog=False, btype='band', output='sos')
        return sos

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
        sos = butter_bandpass(lowcut, highcut, fs, order=order)
        y = sosfilt(sos, data)
        return y
    
    
def get_peaks(column):
    '''
    Simple prototype function that finds the peaks. Will expand in the future todo
    '''
    height_threshold=1000 # We need a threshold. 
    peaks_index, properties = signal.find_peaks(np.abs(column), height=height_threshold)
    return peaks_index

def get_frequencies(Zxx,freqs):
    
    '''
    Gets the frequencies of teh peaks. Not using any vectorization at the moment so not applicable to large sffts
    Once the initial decoding works, we'll optimize it. 
    
    '''
    frequencies = np.array([])

    for i in range(len(Zxx[0,:])):
        peaks_index = get_peaks(Zxx[:,i])
        frequencies =  np.append(frequencies,freqs[peaks_index])  
    return frequencies


def plot_stft(t,f,Zxx):
    
    fig,ax = plt.subplots()
    plt.pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=2500, shading='gouraud')
    ax.set_ylim(0,2500)
    plt.title('Message Components')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()
    
def __get_all_freqs_from_symbols__(symbols):
    '''
    Debug function. Gets all the frequencies of the symbols
    '''
    return [sym.freq for sym in symbols]

    
def create_expected_symbols_debug_file(symbols,binary):
    '''
    Takes a symbol mapping and binary strings as input
    Outputs a CSV file with the expected frequencies 
    '''
    
    with open('debug_expected_symbol.csv','w',newline="") as symDebug:
        debWriter = writer(symDebug)
        header = ["Binary","Freq"]
        
        expected_num_frequencies = 0 
        
        debWriter.writerow(header)
        lower = ""
        upper = ""
        for bits in binary:
           
            
            lower = [[sym[1],sym[2]] for sym in symbols if sym[1] == bits[0][:4]]  
            upper = [[sym[1],sym[2]] for sym in symbols if sym[1] == bits[0][4:]]
            #debWriter.writerow([bits[0],lower[0][0],lower[0][1],upper[0][0],upper[0][1]])
            
            debWriter.writerow([lower[0][0],lower[0][1]])
            debWriter.writerow([upper[0][0],upper[0][1]])
            
            expected_num_frequencies += 2
            
      
        debWriter.writerow([["Expected Number of Frequencies"]])
        debWriter.writerow([[expected_num_frequencies]])
        
def write_read_frequencies_to_file(frequencies):
    '''
    Debug function that writes the frequencies read from the wav file to a csv. After performing short time fft
    '''
      
    
   
    with open("debug_freqs_read_from_wav_stfft.csv","w",newline="") as freq_debug:
        header = ["Frequency"]
    
        deb_writer = writer(freq_debug)
        
        deb_writer.writerow(header)
    
        for freq in frequencies:
            deb_writer.writerow([round(freq,3)])
            
            
            
        
  
    
'''
Test data

'''

#symbols = create_random_symbol_groups(261.63,493.88)
#write_message_to_wav(message,a_table,symbols,fname,bits_per_symbol=4,bytes_per_sample=2)

fname = "testfile2"
a_table = read_ascii_table()
message = "z"


binary = [create_binary_from_ascii_letter(letter,a_table) for letter in message]

symbols,encoding_params,freq_ranges = basic_message_example(fname,message)
frames = read_message_from_wav(fname)




create_expected_symbols_debug_file(symbols,binary)   
    


samples_needed_for_symbol = encoding_params.symbol_duration / (1/encoding_params.fs)
print(encoding_params.symbol_duration,samples_needed_for_symbol)


# f, t, Zxx = signal.stft(frames, encoding_params.fs, nperseg=2056)
f, t, Zxx = signal.stft(frames, encoding_params.fs, nperseg=samples_needed_for_symbol)
plot_stft(t,f,Zxx)

N = 600
yf = scipy.fft(frames)
T = 1.0 / 800.0
xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
fig, ax = plt.subplots()
ax.plot(xf, 2.0/N * np.abs(yf[:N//2]))
plt.show()


freqs = get_frequencies(Zxx,f)
write_read_frequencies_to_file(freqs)

pairs = []
decoded_symbols = []
for i in range(0,len(freqs) - 1,2):
  
    symbol_pair = [0,0]
    for sym in symbols:
        
        freq1_diff = np.abs(sym.freq-freqs[i])
        freq2_diff = np.abs(sym.freq-freqs[i+1])
     
        if freq1_diff >= 0 and freq1_diff <= 1:
            symbol_pair[0] = sym.bit
          
        if freq2_diff >= 0 and freq2_diff <= 1:
            symbol_pair[1] = sym.bit       
            
            
        if symbol_pair[0] != 0 and symbol_pair[1] != 0:
            decoded_symbols.append(symbol_pair[0] + symbol_pair[1])
            break
            
        
        
letters = []

# print("start")
# for binary in decoded_symbols:
#     print(binary)
#     letters.append(get_ascii_from_binary(binary,a_table)) 
       

    
# sym_freqs = __get_all_freqs_from_symbols__(symbols)
    

