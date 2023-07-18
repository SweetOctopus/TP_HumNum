import sentencepiece
import subprocess
from sacrebleu.metrics import BLEU, CHRF, TER
import align
#import align
# lire un fichier ligne par ligne
def read_file(filename):
  list_sents = []
  with open(filename) as fp:
    for line in fp:
      list_sents.append(line.strip())
  return list_sents

# écrire une liste de phrases dans un fichier
def write_file(list_sents, filename):
    with open(filename, 'w') as fp:
        for sent in list_sents:
            fp.write(sent + '\n')

def decode_sp(list_sents):
    return [''.join(sent).replace(' ', '').replace('▁', ' ').strip() for sent in list_sents]

def extract_hypothesis(filename):
    outputs = []
    with open(filename) as fp:
        for line in fp:
            # seulement les lignes qui commencet par H- (pour Hypothèse)
            if 'H-' in line:
                # prendre la 3ème colonne (c'est-à-dire l'indice 2)
                outputs.append(line.strip().split('\t')[2])
    return outputs
def normalize(file,  tmp ='data/tmp_norm.sp.src.tmp', model = 'models/my_third_norm' ):
    # preprocessing
    input_sp = spm.encode(file, out_type=str)
    # add decade token to each sentence
    input_sp_sents = [' '.join(sent) for sent in input_sp]
    write_file(input_sp_sents, tmp)
    #print("preprocessed = ", input_sp_sents)
    # denormalisation
    cmd = "cat " + tmp + " | fairseq-interactive " + model + " --source-lang src --target-lang trg --path " + model + "/checkpoint_best.pt > data/tmp_norm.sp.src.output 2> /tmp/dev"
    subprocess.run(cmd,shell=True)
    # postprocessing
    outputs = extract_hypothesis('data/tmp_norm.sp.src.output')
    outputs_postproc = decode_sp(outputs)
    return outputs_postproc

#testing
test_src = read_file('data/test.src')
test_trg = read_file('data/test.trg')
spm = sentencepiece.SentencePieceProcessor(model_file='data/bpe_joint_2000.model')

#commenter les deux premières pour juste tester ou la derniere pour normaliser
#test_norm = normalize(test_src)
#write_file(test_norm,'test/test.norm.trg')
test_norm = read_file('test/test.norm.trg')

bleu = BLEU()
chrf = CHRF()
ter = TER()

#test align
align_test = align.align('data/test.trg','test/test.norm.trg')
num_diff = 0
total = 0
for sentence in align_test:
    for word in sentence:
        if '>' in word:
            num_diff += 1
        total += 1

print(bleu.corpus_score(test_norm, [test_trg]))
print(chrf.corpus_score(test_norm, [test_trg]))
print(ter.corpus_score(test_norm, [test_trg]))
print('Accuracy = ' + str((total - num_diff)/total))


