#!/usr/bin/python
from levenshtein import *
import re, os
from utils import *

def align(src_file, hyp_file):

    alignments = []
    with open(hyp_file, encoding='utf-8') as hfp, open(src_file, encoding='utf-8') as sfp:
        for hyp, src in zip(hfp, sfp):
            # get rid of any double spaces
            hyp, src = re.sub(' +', ' ', hyp.strip()), re.sub(' +', ' ', src.strip())
            
            # tokenise in order to align on src whitespace later
            hyp, src = tokenise(hyp), tokenise(src)
            len_hyp, len_src = len(hyp.strip()), len(src.strip())
            
            # calculate alignments and scores
            dist, matrix, backpointers  = levenshtein('@ ' + src, '@ ' + hyp)
            s2h = get_correspondences(backpointers, len_src + 2, len_hyp + 2)
            aligned_words = segment_hyp('@ ' +src, '@ ' + hyp, s2h)

            # get alignments
            alignment = []
            for a in aligned_words:
                if a[0] == '▁@▁':
                    continue
                src_tok = postprocess_word(a[0])
                hyp_tok = postprocess_word(a[1])
                if src_tok == hyp_tok:
                    alignment.append(src_tok)
                else:
                    alignment.append(src_tok + '>' + hyp_tok)
            alignments.append(alignment)
    return alignments
    

def postprocess_word(word):
    new_word = word
    if len(word) < 1:
        return '▁'
    if word[0] == '▁':
        new_word = new_word[1:]
    else:
        new_word = '▁' + new_word
    if word[-1] == '▁':
        new_word = new_word[:-1]
    else:
        new_word += '▁'
    return new_word

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('src', help='The source document to be aligned against (or srcerence if appropriate)')
    parser.add_argument('hyp', help='The hypothesis document to align against src')
    args = parser.parse_args()

    align(args.src, args.hyp)
