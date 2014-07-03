__author__ = 'riteshk'

import subprocess


    # The file extracts Fastq blocks for given read accessions. The input file has a block-wise format where each block
    # starts with a ##. The text next to ## indicates name of a SAM file that contains mapping information for the
    # reads of interest. The lines following ## list the read accessions that can be associated with the SAM mentioned
    # in the preceding ## line. SAM files are also categorised according to male and female. We want to extract FASTQ
    # records (both left read and right read) for each read and store the information in relevant male or female file.
    # In the end, we want four files - R1 and R2 for all male SAMs, and R1 and R2 for all female SAMs.
    #

def extract_reads(readListFile, locationOfFastqDir):
    # Fixed according to the Aedes dataset
    female_samples = [1,2,3,4,5,6,7,8,9,10,11,12]
    male_samples = [13,14,15,16,17,18,19,20,21,22,23,24]

    male_R1_out   = "aedes_male_R1.fq"
    male_R2_out   = "aedes_male_R2.fq"
    female_R1_out = "aedes_female_R1.fq"
    female_R2_out = "aedes_female_R2.fq"

    # Sample block header - ##../BowtieMappings_single/contigs_lane_1/10-Lane_1.sam
    f_in = open(readListFile)
    f_out_male_R1 = open(male_R1_out,'w')
    f_out_male_R2 = open(male_R2_out,'w')
    f_out_female_R1 = open(female_R1_out,'w')
    f_out_female_R2 = open(female_R2_out,'w')

    for line in f_in:
        if line.startswith('##'):
            sam_parts = line.split('/')
            sam_name = sam_parts[-1]
            sam_sample_lane = sam_name.split('-')
            sam_sample = sam_sample_lane[0]

            if sam_sample in male_samples:
                r1_out = f_out_male_R1
                r2_out = f_out_male_R2
            else:
                r1_out = f_out_female_R1
                r2_out = f_out_female_R2

            r1_fastq = locationOfFastqDir + sam_sample + '.R1.fastq.gz'
            r2_fastq = locationOfFastqDir + sam_sample + '.R2.fastq.gz'
        else:
            r1_P = subprocess.Popen(["zgrep","-A 3",line,r1_fastq],stdout=subprocess.PIPE)
            r2_P = subprocess.Popen(["zgrep","-A 3",line,r2_fastq],stdout=subprocess.PIPE)
            (r1_zgrep,err_R1) = r1_P.communicate()
            (r2_zgrep, err_R2) = r2_P.communicate()

            r1_out.write(line + '\n')
            r2_out.write(r2_zgrep + '\n')

    f_in.close()
    f_out_male_R1.close()
    f_out_male_R2.close()
    f_out_female_R1.close()
    f_out_female_R2.close()

if __name__=="__main__":
    fastqLocation="/pub19/acdguest/Beth/Sex_locus_identification/Fastq_files/Lane_1/"
    readListFile="/pub9/ritesh/Aedes_Aegypti/BowtieMappings_single/contigs_lane_1/unmapped_reads_lane1.txt"
    extract_reads(readListFile,fastqLocation)


