__author__ = 'ritesh'

"""
Parse the Vectorbase GFF file and extract gene information for all the scaffolds. The gene information is formatted as
gene1_start_end;gene2_start_end...
"""
def parseGFF(gffFile):

    scaffold_gene_dict = {}

    f_in = open(gffFile,'r')

    current_scaffold = ''

    gene_list_for_current_scaffold = []

    for line in f_in:
        if line.startswith('#'):
            continue

        if line.strip():

            gff_fields = line.split('\t')

            if len(gff_fields) == 9:
                seqName = gff_fields[0]
                feature = gff_fields[2]
                start = gff_fields[3]
                end = gff_fields[4]
                attribute = gff_fields[8]
                attribute_parts = attribute.split(';')
                id = attribute_parts[0]
                id_name = id.replace('ID=','')

                if feature == 'gene':
                    gene_info = id_name + '_' + start + '_' + end
                    gene_list_for_current_scaffold.append(gene_info);

                if feature == 'contig':
                    if not current_scaffold:
                        current_scaffold = id_name
                    else:
                        gene_info = ';'.join(gene_list_for_current_scaffold)
                        scaffold_gene_dict[current_scaffold] = gene_info
                        current_scaffold = id_name
                        gene_list_for_current_scaffold = []

    f_in.close()

    return scaffold_gene_dict

if __name__ == "__main__":

    gffFile = '/Users/ritesh/Ritesh_AedesAegypty/Analysis/VectorBaseFiles/Aedes-aegypti-Liverpool_BASEFEATURES_AaegL3.1.gff3_0'
    scaffold_gene_dict = parseGFF(gffFile)

    print scaffold_gene_dict