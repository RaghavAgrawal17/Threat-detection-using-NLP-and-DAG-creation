# Runfile => runfile("C:/Users/Raghav/json_to_spacy.py",args="-i outputData.json -o output_file")


# Convert json file to spaCy format.
import plac
import logging
import argparse
import sys
import os
import json
import pickle

import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree,tree2conlltags
from pprint import pprint
import en_core_web_sm

@plac.annotations(input_file=('Input file', "option", "i", str), output_file=('Output file', "option", "o", str))


def main(input_file=None, output_file=None):
    try:
        training_data = []
        lines=[]
        with open(input_file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            data = json.loads(line)
            text = data['content']
            entities = []
            for annotation in data['annotation']:
                points = annotation['points']
                label = annotation['label'][0]
                if not isinstance(points, list):
                    points = [points]
                for point in points:
                    entities.append((point['start'], point['end'] + 1, label))


            training_data.append((text, {"entities" : entities}))

        print(training_data)

        with open(output_file, 'wb') as fp:
            pickle.dump(training_data, fp)

    except Exception as e:
        logging.exception("Unable to process " + input_file + "\n" + "error = " + str(e))
        return None
    
plac.call(main)
