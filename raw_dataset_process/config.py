import os
import pandas as pd

# root of all recorded folders
raw_data_roots = ['/rawisl1/ARGISL/dataset', 
                  '/rawisl2/ARGISL/dataset',
                  '/rawisl3/ARGISL/dataset',
                  '/rawisl4/ARGISL/dataset']

# intermediate output roots
im_output_roots = ['/data3/dataset',
                   '/data4/dataset',
                   '/data5/dataset']

# final cropped output roots
output_roots = ['/data2/dataset']

# retrieve all subject's recoding details
sub_rec_details = pd.read_csv('input/subject_recording_details.csv')

# words and tags mapping
word_tags = pd.read_csv('input/word_tags.csv')



