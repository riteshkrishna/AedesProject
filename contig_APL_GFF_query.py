__author__ = 'ritesh'

""" Queries for a contigFile where contigs are listed in a single column/one per line. The contigs are looked in the
    APG file for occurrences. A dictionary is returned where contigs are mapped on a string containing the corresponding
    scaffoldname_contigstart_contigend. Any other program calling this function should parse the value string if desired.
"""
def get_scaffold_for_contigs(contigFile, apgFile):

    f_in_cont = open(contigFile,'r')
    f_in_agp = open(apgFile,'r')

    scaffold_contig_dict = {}
    contig_set = set()

    for line in f_in_cont:
        if line.startswith('##'):
            continue
        contig_set.add(line.rstrip())
    f_in_cont.close()

    for line in f_in_agp:
        if line.startswith('##'):
            continue
        apg_records = line.split('\t')
        scaffold_name = apg_records[0]
        contig_start  = apg_records[1]
        contig_end    = apg_records[2]
        contig_name   = apg_records[5]

        if contig_name in contig_set:
            scaffold_info = scaffold_name + "_" + contig_start + "_" + contig_end
            scaffold_contig_dict[contig_name] = scaffold_info

    f_in_agp.close()

    return scaffold_contig_dict

if __name__ == "__main__":
    contigFile = '/Users/ritesh/tmp/trial_CGR.txt'
    apgFile = '/Users/ritesh/Ritesh_AedesAegypty/Analysis/VectorBaseFiles/Aedes-aegypti-Liverpool_CONTIG2SCAFFOLD_AaegL3.agp'
    scaffold_contig_dict = get_scaffold_for_contigs(contigFile,apgFile)
    print scaffold_contig_dict