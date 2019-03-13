#! /usr/bin/python
import json

colors = ['rgb(255,107,53)', 'rgb(157,150,184)', 'rgb(18,130,162)', 'rgb(150,147,155)', 'rgb(139,190,178)', 'rgb(128,26,134)', 'rgb(175,145,100)', 'rgb(184,51,106)', 'rgb(147,22,33)', 'rgb(191,200,173)']

# from https://www.materialpalette.com
materialpalette_colors = [
    '#303F9F',
    '#D32F2F',
    '#FFA000',
    '#689F38',
    '#5D4037',
    '#455A64',
    '#1976D2',
    '#C2185B',
    '#FBC02D',
    '#7B1FA2',
    '#512DA8',
    '#E64A19',
    '#0288D1',
    '#0097A7',
    '#00796B',
    '#388E3C',
    '#AFB42B',
    '#F57C00',
    '#616161',
    ]

class ParsingError(Exception):
    pass

class MachineCheckError(Exception):
    pass

class ExtensionError(Exception):
    pass


def pretty_label(label):
    try:
        with open('pretty_label.json') as f:
            label=json.load(f)[label]
    except Exception as e:
        logging.debug(e)
    return label
