__author__ = 'ritesh'

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


def extract_requiredSequences(fastaFile,accessionFile,out_acc_fasta):
    '''
    We need only those sequences that start with a particular pattern in accession.
    We provide the pattern here and pull out the ones required
    '''

    f_out = open(out_acc_fasta,'w')
    f_in = open(accessionFile, 'r')

    L = list()
    for line in f_in:
        L.append(line.rstrip())
    print ('L Before :', len(L))

    # Find unique accessions
    set_L = set(L)
    print ('set_L length :', len(set_L))

    new_L = list(set_L)

    mygenerator = fasta_iter(fastaFile)
    for head, seq in mygenerator:
        stripped_head = head.lstrip('>')
        head_to_search = stripped_head.split()
        if head_to_search[0] in new_L:
            f_out.write(head)
            f_out.write('\n')
            f_out.write(seq)
            f_out.write('\n')

    f_in.close()
    f_out.close()


if __name__ == "__main__":



    # Fasta file that you want to use
    fastaFile = 'me49.new_genes.final.fasta'
    # File containing FASTA accessions
    accessionFile = 'ID.txt'
    # Output FASTA file
    out_acc_fasta = 'ID_extracted.fasta'

    extract_requiredSequences(fastaFile,accessionFile,out_acc_fasta)


