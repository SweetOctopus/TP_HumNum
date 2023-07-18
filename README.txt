Explication de ce que j'ai fait :
	(pour la partie xml/tei/xslt)

	Dans corpus/corpu_tei, il y'a tous les documents que tu m'as donné, légèrement revus, et un script xslt "xml_to_tsv" pour les transformer en tsv

	Dans le dossier /corpus, il y'a un script "traitement.py" qui formate les tsv obtenus plus haut, ajoute leurs premières lignes à "tableOfContent.tsv" (tableOfContent.tsv doit se trouver dans le même dossier que traitement) et le reste dans un dossier "corpus_tsv", deplace ensuite la table et le dossier dans le dossier parent (c'est à dire "final_hum")

	(A noter que j'ai utilisé traitement.py uniquement sur les nouveaux documents, et que j'ai utilisé la tableOfContents.tsv avec deja les infos du corpus de base et que j'ai copié-collé les tsv du corpus de base dans corpus_tsv à la main)

	Dans final hum il y'a split.py (à toi) qui effectue le split et split_to_src_trg.py qui separe les fichiers obtenus par le split en .src et .trg, et les place dans un dossier data

	(pour la partie entrainement/testing de modele)

	Avec les données obtenues plus haut, on peut entrainer un modèle, pour se faire j'ai suivi le jupyter du cours 4, donc j'ai segmenté avec sentencepiece en 2000
	
	Ensuite j'ai entrainé avec cette commande :
	fairseq-train \
        	data/data_norm_bin_2000 \
        	--save-dir models/my_third_norm \
        	--save-interval 1 --patience 12 \
        	--arch lstm \
        	--encoder-layers 3 --decoder-layers 3 \
        	--encoder-embed-dim 384 --decoder-embed-dim 384 --decoder-out-embed-dim 384 \
        	--encoder-hidden-size 768 --encoder-bidirectional --decoder-hidden-size 768 \
        	--dropout 0.3 \
        	--criterion cross_entropy --optimizer adam --adam-betas '(0.9, 0.98)' \
        	--lr 0.0001 --lr-scheduler inverse_sqrt \
        	--warmup-updates 4000 \
        	--share-all-embeddings \
        	--max-tokens 3000 \
        	--batch-size-valid 64

	le modèle se trouve dans models/my_third_norm

	On peut l'utiliser avec fairseq-interactive

	Si l'on lance normalize.py, on va avoir le resultat des 4 différents tests sur la normalisation de test.trg (il y'a 2 lignes commentées qui permettent de normaliser test.trg, mais là je l'ai déjà fait)
	j'arrive à 
		BLEU = 88.65 94.8/90.5/86.7/83.0 (BP = 1.000 ratio = 1.002 hyp_len = 82769 ref_len = 82598)
		chrF2 = 95.83
		TER = 6.22
		Accuracy = 0.9512266784192743


Mes questions :
	C'est quoi "paratext", "Belles-Lettres" et "link" ? je comprends l'idée mais en fait j'ai pas accès aux documents de base, juste à la TEI donc je sais pas comment remplir ces trois-là...

	En ce qui concerne la TEI, j'ai tenté de mettre toutes les données de la tableOfContents dans le TEIHeader, mais je suis pas parvenu à trouver comment mentionner le genre, la date de naissance et de mort des auteurs. J'ai tenté avec le premier texte (Agrippa) mais j'aimerais bien que tu me corriges avant que je fasse les autres (j'ai deja recup les infos pour tout le monde dans un excel "corpus/corpus_tei/__info_pour_tei"

	Sinon en general j'ai mis des commentaires (pas beaucoup) un peu dans chaque document, le truc le plus important je dirais c'est que le teiHeader du document Cahusac contiennent une copie de celui de Laclos sinon un des doc n'avait pas de <l>, que des <choice><orig><reg>, ce que je trouvais semantiquement bizarre (et pas pratique pour mon script alors j'ai tout remplacé par des <l>

	J'ai remarqué que je prenais que les <l> avec mon xslt, je me rend pas compte si je devrais prendre aussi les titre, sous-titre,etc ou si ça fausserait tout

REMARQUES :
	Dans le Jupyter, pour la cmd de preprocess, je crois que source et target sont inversés, du coup les deux premiers modèles que j'ai entrainés, c'était des denormaliseur XD

		!fairseq-preprocess --destdir data/data_norm_bin_2000/ \
                    -s trg -t src \    	<!!!!--ICI le src et trg est inversé--!!!!>
                    --trainpref data/train.sp2000 \
                    --validpref data/dev.sp2000 \
                    --testpref data/test.sp2000 \
                    --joined-dictionary

