__author__ = 'riteshk'

'''
Plutella : Code to handle the FASTA produced by assembly
Format of original assembly as stored in -/pub9/ritesh/Plutella/sequenceStorage/sspaceTry19_with_unscaffoldedContigs.fas
Example accessions -
    >scaffold17257|size1500
    >scaffold17258|size1500
    >scaffold17259|size1500
    >scaffold17260|size1500
    >contig60119  length=1501   numreads=51
    >contig60120  length=1500   numreads=14
    >contig60121  length=1501   numreads=31
    >contig60122  length=1485   numreads=18
'''

from itertools import groupby

def fasta_iter(fasta_name):
    """
    given a fasta file. yield tuples of header, sequence
    """
    fh = open(fasta_name)
    # ditch the boolean (x[0]) and just keep the header or sequence since
    # we know they alternate.
    faiter = (x[1] for x in groupby(fh, lambda line: line[0] == ">"))
    for header in faiter:
        header = header.next().strip()
        # join all sequence lines to one.
        seq = "".join(s.strip() for s in faiter.next())
        yield header, seq


def handle_accession(accession):
    clean_accession = ''
    seq_length = 0

    if accession.startswith('scaffold'):
        acc_parts = accession.split('|')
        clean_accession = acc_parts[0]
        seq_length = acc_parts[1].replace('size','')
    elif accession.startswith('contig'):
        acc_parts = accession.split()
        clean_accession = acc_parts[0]
	
        temp_seq_length = (acc_parts[1]).split('=')
        seq_length = temp_seq_length[1]
    else:
        print 'Error : ' + accession

    return (clean_accession, seq_length)

def extract_requiredSequences(fastaFile,out_scf_fasta,out_scf_bed,out_cnt_fasta,out_cnt_bed):

    scf_fas_out = open(out_scf_fasta,'w')
    scf_bed_out = open(out_scf_bed,'w')
    cnt_fas_out = open(out_cnt_fasta,'w')
    cnt_bed_out = open(out_cnt_bed,'w')

    mygenerator = fasta_iter(fastaFile)
    for head, seq in mygenerator:
        stripped_head = head.lstrip('>')
        accession, seq_length = handle_accession(stripped_head)

        if 'scaffold' in accession:
            scf_fas_out.write('>' + accession + '\n' + seq + '\n')
            scf_bed_out.write(accession + '\t' + str(0) + '\t' + str(int(seq_length) - 1) + '\n')
        elif 'contig' in accession:
            cnt_fas_out.write('>' + accession + '\n' + seq + '\n')
            cnt_bed_out.write(accession + '\t' + str(0) + '\t' + str(int(seq_length) - 1) + '\n')

    scf_fas_out.close()
    scf_bed_out.close()
    cnt_fas_out.close()
    cnt_bed_out.close()


if __name__ == "__main__":
    fastaFile     = '/pub9/ritesh/Plutella/sequenceStorage/sspaceTry19_with_unscaffoldedContigs.fas'

    out_scf_fasta = '/pub9/ritesh/Plutella/sequenceStorage/scf.fasta'
    out_scf_bed   = '/pub9/ritesh/Plutella/sequenceStorage/scf.bed'
    out_cnt_fasta = '/pub9/ritesh/Plutella/sequenceStorage/cnt.fasta'
    out_cnt_bed   = '/pub9/ritesh/Plutella/sequenceStorage/cnt.bed'

    extract_requiredSequences(fastaFile,out_scf_fasta,out_scf_bed,out_cnt_fasta,out_cnt_bed)
