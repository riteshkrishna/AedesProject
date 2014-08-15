__author__ = 'ritesh'

"""
    Takes an input file with a list of contigs (one name per line). The contigs are first
    looked in the APG file to identify the scaffolds they sit on, the scaffolds are further
    looked into a GFF file to identify the genes present. Finally, a list of contigs, scaffolds,
    genes is presented. The script also identifies the genes that contain or overlap with
    the provided contigs.
"""

from contig_APL_GFF_query import get_scaffold_for_contigs
from readVectorBaseGFF import parseGFF

def checkIfContigFallsInGene(contig_start,contig_end,genes_info):

    containing_gene_name = '\t'

    if not genes_info.strip():
        return containing_gene_name

    #genes_info is a ; separated list of genename_start_end information
    genes = genes_info.split(';');

    for gene in genes:
        gene_st_end = gene.split('_')
        gene_name = gene_st_end[0]
        gene_start = int(gene_st_end[1])
        gene_end = int(gene_st_end[2])

        if (contig_start >= gene_start and contig_end <= gene_end):
            containing_gene_name = gene_name
            return containing_gene_name
        elif (contig_start < gene_start and contig_end >= gene_start):
            containing_gene_name = gene_name
            return containing_gene_name
        elif (contig_start >= gene_start and contig_start <= gene_end):
            containing_gene_name = gene_name
            return containing_gene_name

    return containing_gene_name


def createOutputFile(scaffold_contig_dict,scaffold_gene_dict,outFile):

    f_out = open(outFile,'w')

    header = 'Contig (start-end) \t Scaffold \t Overlapping gene \t List of genes in scaffold \n'
    f_out.write(header)

    contig_names = scaffold_contig_dict.keys()

    for contig in contig_names:

        scaffold_continfo = scaffold_contig_dict[contig]
        scaffold_continfo_parts = scaffold_continfo.split('_')
        scaffold_name = scaffold_continfo_parts[0]
        contig_start = int(scaffold_continfo_parts[1])
        contig_end = int(scaffold_continfo_parts[2])

        if scaffold_gene_dict.has_key(scaffold_name):

            genes_info = scaffold_gene_dict[scaffold_name]
            containing_gene_name = checkIfContigFallsInGene(contig_start,contig_end,genes_info)

            contig_info = contig + '(' + str(contig_start) + '-' + str(contig_end) + ')'

            to_print = contig_info + '\t' + scaffold_name + '\t' + containing_gene_name + '\t' + genes_info + '\n'
            print (to_print)
            f_out.write(to_print)
        else:
            to_print = contig_info + '\t' + scaffold_name + '\n'
            print (to_print)
            f_out.write(to_print)


    f_out.close()

if __name__ == "__main__":

    contigFile = '/Users/ritesh/Ritesh_AedesAegypty/Analysis/CoverageFiles/DataFiles/DistanceBased/contig_list_top_6.txt'
    apgFile = '/Users/ritesh/Ritesh_AedesAegypty/Analysis/VectorBaseFiles/Aedes-aegypti-Liverpool_CONTIG2SCAFFOLD_AaegL3.agp'

    gffFile = '/Users/ritesh/Ritesh_AedesAegypty/Analysis/VectorBaseFiles/Aedes-aegypti-Liverpool_BASEFEATURES_AaegL3.1.gff3_0'
    outFile = '/Users/ritesh/Ritesh_AedesAegypty/Analysis/CoverageFiles/DataFiles/DistanceBased/contig_list_6_GENEINFO.txt'

    scaffold_contig_dict = get_scaffold_for_contigs(contigFile,apgFile)
    scaffold_gene_dict = parseGFF(gffFile)

    createOutputFile(scaffold_contig_dict,scaffold_gene_dict,outFile)