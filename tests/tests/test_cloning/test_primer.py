'''Tests primer design module.'''
from nose.tools import assert_equals, assert_not_equal, assert_raises
import coral as cr


def test_primer():
    '''Test primer function.'''
    seq = ('ATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGC'
           'GACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGGCGATGCCACCTACGGCAAG'
           'CTGACCCTGAAGTTCATCTGCACCACCGGCAAGCTGCCCGTGCCCTGGCCCACCCTCGTGACC'
           'ACCTTCGGCTACGGCCTGCAGTGCTTCGCCCGCTACCCCGACCACATGAAGCAGCACGACTTC'
           'TTCAAGTCCGCCATGCCCGAAGGCTACGTCCAGGAGCGCACCATCTTCTTCAAGGACGACGGC'
           'AACTACAAGACCCGCGCCGAGGTGAAGTTCGAGGGCGACACCCTGGTGAACCGCATCGAGCTG'
           'AAGGGCATCGACTTCAAGGAGGACGGCAACATCCTGGGGCACAAGCTGGAGTACAACTACAAC'
           'AGCCACAACGTCTATATCATGGCCGACAAGCAGAAGAACGGCATCAAGGTGAACTTCAAGATC'
           'CGCCACAACATCGAGGACGGCAGCGTGCAGCTCGCCGACCACTACCAGCAGAACACCCCCATC'
           'GGCGACGGCCCCGTGCTGCTGCCCGACAACCACTACCTGAGCTACCAGTCCGCCCTGAGCAAA'
           'GACCCCAACGAGAAGCGCGATCACATGGTCCTGCTGGAGTTCGTGACCGCCGCCGGGATCACT'
           'CTCGGCATGGACGAGCTGTACAAGTAA')
    dna_seq = cr.DNA(seq)
    primer = cr.cloning.primer(dna_seq, tm=72, min_len=10, tm_undershoot=1,
                               tm_overshoot=3, end_gc=False,
                               tm_parameters='cloning', overhang=None)
    assert_equals(str(primer), 'ATGGTGAGCAAGGGCGAGGAG')
    # Ensure that overhang is appropriately applied
    overhang_primer = cr.cloning.primer(dna_seq, tm=72, min_len=10,
                                        tm_undershoot=1, tm_overshoot=3,
                                        end_gc=False,
                                        tm_parameters='cloning',
                                        overhang=cr.DNA('GATCGATAT'))
    assert_equals(str(overhang_primer), 'GATCGATATATGGTGAGCAAGGGCGAGGAG')
    # If sequence is too short (too low of Tm), raise ValueError
    too_short = cr.DNA('at')
    assert_raises(ValueError, cr.cloning.primer, too_short, tm=72)
    # Should design different primers (sometimes) if ending on GC is preferred
    diff_template = cr.DNA('GATCGATCGATACGATCGATATGCGATATGATCGATAT')
    nogc = cr.cloning.primer(diff_template, tm=72, min_len=10,
                             tm_undershoot=1, tm_overshoot=3, end_gc=False,
                             tm_parameters='cloning', overhang=None)
    withgc = cr.cloning.primer(diff_template, tm=72, min_len=10,
                               tm_undershoot=1, tm_overshoot=3,
                               end_gc=True, tm_parameters='cloning',
                               overhang=None)
    assert_not_equal(nogc, withgc)
    # Should raise ValueError if it's impossible to create an end_gc primer
    end_at_template = cr.DNA('ATGCGATACGATACGCGATATGATATATatatatat' +
                             'ATAAaaaaaaaaaattttttttTTTTTTTTTTTTTT' +
                             'TTTTTTTTTT')
    assert_raises(ValueError, cr.cloning.primer, end_at_template,
                  end_gc=True, tm=72)


def test_primers():
    '''Test primers function.'''
    seq = ('ATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGC'
           'GACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGGCGATGCCACCTACGGCAAG'
           'CTGACCCTGAAGTTCATCTGCACCACCGGCAAGCTGCCCGTGCCCTGGCCCACCCTCGTGACC'
           'ACCTTCGGCTACGGCCTGCAGTGCTTCGCCCGCTACCCCGACCACATGAAGCAGCACGACTTC'
           'TTCAAGTCCGCCATGCCCGAAGGCTACGTCCAGGAGCGCACCATCTTCTTCAAGGACGACGGC'
           'AACTACAAGACCCGCGCCGAGGTGAAGTTCGAGGGCGACACCCTGGTGAACCGCATCGAGCTG'
           'AAGGGCATCGACTTCAAGGAGGACGGCAACATCCTGGGGCACAAGCTGGAGTACAACTACAAC'
           'AGCCACAACGTCTATATCATGGCCGACAAGCAGAAGAACGGCATCAAGGTGAACTTCAAGATC'
           'CGCCACAACATCGAGGACGGCAGCGTGCAGCTCGCCGACCACTACCAGCAGAACACCCCCATC'
           'GGCGACGGCCCCGTGCTGCTGCCCGACAACCACTACCTGAGCTACCAGTCCGCCCTGAGCAAA'
           'GACCCCAACGAGAAGCGCGATCACATGGTCCTGCTGGAGTTCGTGACCGCCGCCGGGATCACT'
           'CTCGGCATGGACGAGCTGTACAAGTAA')
    dna_seq = cr.DNA(seq)
    primers_list = cr.cloning.primers(dna_seq, tm=72, min_len=10,
                                      tm_undershoot=1, tm_overshoot=3,
                                      end_gc=False, tm_parameters='cloning',
                                      overhangs=None)
    primers = [str(x.primer()) for x in primers_list]
    assert_equals(primers, ['ATGGTGAGCAAGGGCGAGGAG',
                            'TTACTTGTACAGCTCGTCCATGCCG'])
