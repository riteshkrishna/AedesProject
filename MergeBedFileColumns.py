__author__ = 'riteshk'

import glob
import os

    #     This program takes a directory containing BED files containing the output
    #     of coverageBED. It first creates a list of all the features present across
    #      all the files, and then for each feature, it collects the relevant data
    #      from all the bed files. The output is presented in a tabular format, where
    #      the first row is the name of the features, and the first column is the file
    #      names.

def mergeBEDFiles(bed_file_dir,outputFile):
    os.chdir(bed_file_dir)

    f_out = open(outputFile,'w')

    dict_scaffold = {}

    for bed_file in glob.glob("*.bed"):
        f_in = open(bed_file,'r')

        for line in f_in:
            if line.startswith('##'):
                continue
            fields = line.split('\t')
            if len(fields) == 7:
                scaffold = fields[0]
                num_feature_overlap = int(fields[3])
                num_bases = int(fields[4])
                base_fraction = float(fields[6])

                if not scaffold in dict_scaffold:
                    dict_scaffold[scaffold] = 1

        f_in.close()

    # When the dictionary is built, we preform processing
    scaffold_list = []
    for key, value in dict_scaffold.items():
        print (key + ' ' + str(value))
        scaffold_list.append(key)

    print (len(scaffold_list))
    f_out.write('scaffold' + ',')
    for item in scaffold_list:
        f_out.write(item + ',')
    f_out.write('\n')

    for bed_file in glob.glob("*.bed"):

        f_in = open(bed_file,'r')
        list_for_this_bed = [0] * len(scaffold_list)

        for line in f_in:
            if line.startswith('##'):
                continue
            fields = line.split('\t')
            if len(fields) == 7:
                scaffold = fields[0]
                num_feature_overlap = int(fields[3])
                num_bases = int(fields[4])
                base_fraction = float(fields[6])

                if scaffold in scaffold_list:
                    idx = scaffold_list.index(scaffold)
                    list_for_this_bed[idx] = base_fraction
                else:
                    print (scaffold + ' not found')

        f_in.close()
        print (len(list_for_this_bed))
        f_out.write(bed_file + ',')
        for item in list_for_this_bed:
            f_out.write(str(item) + ',')
        f_out.write('\n')

    f_out.close()

if __name__=="__main__":
    bed_file_dir = "C:\\tmp"
    mergedFile = "C:\\tmp\\merged.txt"
    mergeBEDFiles(bed_file_dir,mergedFile)

