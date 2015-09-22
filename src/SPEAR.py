# Interprets and processes SPEAR analysis data
# John Burnett

import spectral

class SPEAR_Analyzer:

    def __init__(self,filename):
        self.data = []
        self.times = []
        self.file = open(filename, 'r')
        self.text = self.file.readlines()[5:]


    def populate_data(self,samples):
        for i in range(0,len(self.text),len(self.text)/samples):
            line = (self.text[i]).split()
            t = float(line[0])
            #n = int(line[1])
            self.times.append(t)

            fft_bin = []
            for j in range(2,len(line),3):
                #index = int(line[j])
                frequency = float(line[j+1])
                amplitude = float(line[j+2])

                pair = [frequency,amplitude]
                fft_bin.append(pair)
            self.data.append(fft_bin)


    def normalize_amplitudes(self):
        amplitudes = []
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                amplitudes.append(self.data[i][j][1])

        maximum = max(amplitudes)
        minimum = min(amplitudes)

        for i in range(len(amplitudes)):
            normalized = (amplitudes[i] - minimum) / (maximum - minimum)
            amplitudes[i] = normalized

        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                self.data[i][j][1] = amplitudes[i+j]


    def median_amplitude(self):
        amplitudes = []
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                amplitudes.append(self.data[i][j][1])

        amplitudes.sort()
        median = amplitudes[len(amplitudes)/2]
        return median


    def filter_by_amplitude(self, threshold):
        filtered_data = []
        for sample in self.data:
            filtered_sample = []
            for bin in sample:
                if bin[1] > threshold:
                    filtered_sample.append(bin)
            filtered_data.append(filtered_sample)
        self.data = filtered_data


    def high_pass_filter(self, threshold):
        filtered_data = []
        for sample in self.data:
            filtered_sample = []
            for bin in sample:
                if bin[0] > threshold:
                    filtered_sample.append(bin)
            filtered_data.append(filtered_sample)
        self.data = filtered_data


    def low_pass_filter(self, threshold):
        filtered_data = []
        for sample in self.data:
            filtered_sample = []
            for bin in sample:
                if bin[0] < threshold:
                    filtered_sample.append(bin)
            filtered_data.append(filtered_sample)
        self.data = filtered_data


    def band_pass_filter(self, low_freq, high_freq):
        self.high_pass_filter(low_freq)
        self.low_pass_filter(high_freq)


    def convert_to_midi(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                self.data[i][j][0] = spectral.FtoM(self.data[i][j][0])


    def round_microtones(self,semitones):
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                self.data[i][j][0] = spectral.roundMicro(self.data[i][j][0],semitones)
