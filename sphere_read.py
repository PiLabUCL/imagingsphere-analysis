#!/usr/bin/env python2

import re

class SphereData(object):
    def __init__(self, filepath):
        # Open the file
        is_datafile = open(filepath, 'r')

        # Process the preamble line-by-line
        reading_preamble = True
        store_next_line = False
        label_for_next_line = ''
        num_items_for_next_line = 0
        self.meta_data = {}
        while True:
            line = is_datafile.readline()
            if not line: break
            line = line[:-2]
            if store_next_line:
                spline = filter(None, re.split('\s', line))
                self.meta_data[label_for_next_line] = [float(i) for i in spline[:num_items_for_next_line]]
                store_next_line = False
                continue
            if reading_preamble:
                if line == 'DataBegin':
                    reading_preamble = False
                    continue
                spline = filter(None, re.split('\s', line))
                if len(spline) == 2:
                    try:
                        numvals = int(spline[1])
                        store_next_line = True
                        label_for_next_line = spline[0]
                        num_items_for_next_line = int(spline[1])
                    except ValueError:
                        pass
            else:
                break

        self.intensity_data = {}
        for wavelength in self.meta_data['Wavelengths']:
            is_datafile.readlines(4)
            this_wavelength = {}

            this_wavelength['forward'] = []
            for azimuth in self.meta_data['ScatterAzimuth']:
                line = is_datafile.readline()
                spline = filter(None, re.split('\s', line))
                try:
                    this_wavelength['forward'].append([float(i) for i in spline[:len(self.meta_data['ScatterRadial'])]])
                except ValueError:
                    break

            this_wavelength['backward'] = []
            for azimuth in self.meta_data['ScatterAzimuth']:
                line = is_datafile.readline()
                spline = filter(None, re.split('\s', line))
                try:
                    this_wavelength['backward'].append([float(i) for i in spline[:len(self.meta_data['ScatterRadial'])]])
                except ValueError:
                    break

            self.intensity_data[wavelength] = this_wavelength

    def plot(self, wavelength,direction="forward"):
        from matplotlib import pyplot as plt
        from numpy import meshgrid, log
        r, theta = meshgrid(self.meta_data['ScatterRadial'][:len(self.intensity_data[wavelength][direction][0])],
                            self.meta_data['ScatterAzimuth'][:len(self.intensity_data[wavelength][direction])])
        fig, ax = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(10, 10))
        plot = ax.contourf(theta, r, log(self.intensity_data[wavelength][direction]), 1000)
        plt.colorbar(plot, ax=ax)
        plt.show()


def main(args):
    if len(args) == 3:
        sphere_data = SphereData(args[1])
        sphere_data.plot(int(args[2]))
    else:
        print "Please specify a file and a wavelength"

        
if __name__ == '__main__':
    from sys import argv
    main(argv)

