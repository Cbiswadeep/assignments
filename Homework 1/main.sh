echo "Solution to Question 4"
#echo "Count Frequencies for Baseline Model "
mkdir Outputs
#python Codes/count_freqs.py gene.train>Outputs/gene.counts

#echo "Evaluating Baseline Model"
#python Codes/eval_gene_tagger.py gene.key Outputs/gene_test.p1.out 
#python eval_gene_tagger.py gene.key gene_test.p1.out
#echo "########################################################################"
##############################################################################
echo "Solution to Question 4.1"


echo "Replacing infrequent words with __RARE__"
python Codes/rare.py gene.train Outputs/gene.train.rare 
echo "Recalculating counts"
python Codes/count_freqs.py Outputs/gene.train.rare>Outputs/gene.train.rare.counts

echo "Running Baseline Decoding"
python Codes/baseline.py Outputs/gene.train.rare.counts gene.test Outputs/gene_test.p1.out 
echo "Evaluating Baseline Decoding"
python Codes/eval_gene_tagger.py gene.key Outputs/gene_test.p1.out 

echo "##########################################################################"

########################################################################
echo "Solution to Question 4.2"
echo "Running HMM with Trigram Features"

python Codes/trigram.py Outputs/gene.train.rare.counts gene.test Outputs/gene_test.p2.out 
echo "Evaluating HMM with Trigram Features"
python Codes/eval_gene_tagger.py gene.key Outputs/gene_test.p2.out 