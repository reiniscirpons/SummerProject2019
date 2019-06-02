

> This project description file gives a bit of background and outlines the main goals of the project.

# SummerProject2019
### Andy Lynch
#### May 2019

## 1 Introduction
Cancer is a disease thought largely to be driven by mutations of the genome.
Some cancers are dominated by large-scale rearrangements (big chunks of DNA
duplicated/lost/moved) and others by smaller mutations such as a single nucleotide changing from say and 'A' to a 'G'. These latter ones we will focus on.

Either way, disabling or diverting the repair mechanisms of the cell seems
to be a necessary process through which a cancer will have gone, and so there
are likely to be many 'passenger' mutations picked up on the way that won’t
necessarily effect the spread of the cancer.

To determine important (the ones we need to counter) mutations from the passengers, we look for mutations that occur in multiple patients (or for mutations that would have the same effect in multiple patients). The simplest case would be the same base mutated in each patient. Then we might consider genes
that are mutated in multiple patients (even if a different mutation in each one).
After that we might wonder about commonly affected biological pathways. Mutations that aren’t (obviously) affecting genes are also possible, but it is harder to know what to do with them.

The number of driver genes is $\leq 10$, the number of passengers can be in
the thousands or tens of thousands. Mutations do not occur uniformly, but
are more likely to occur in a specific location depending on the local sequence.
There will also be more evolutionary pressure in some areas of the genome than
in others.

## 2 Sequencing a cancer
We sequence a cancer by taking random fragments of the DNA ($2 \times150$ bases - we sequence from each end of the fragment), sequencing them and mapping
them to the reference genome. Due to the random sampling, we can’t guarantee
the coverage at any position, and so aim for an average.

The genome is $3, 000, 000, 000$ bases long, if each read has $300$ sequenced
bases then we need $10, 000, 000$ to average one read covering each position on the genome. Typically we seek to have an average of $50$ - $60$ reads covering each
base, so would require half a billion reads.

## 3 Detecting mutations
It seems like it might be easy to detect a mutation. We sequence the germline
genome of the patient and see $50$ 'A's, and we sequence the tumour genome and
see $25$ 'A's and $25$ 'G's. However the reality is that there is less certainty about
mutation calls than you might think.

The sample might be $60\%$ benign tissue, and the size of the tumour genome
might be double due to mutations. Therefore $4\times 40/(2\times 60+4\times 40)$ of the reads
will be from the tumour, and a mutation in one copy will be in $40/(2\times 60+4\times 40)$
of the reads. If the coverage of a base by chance is only $30$, then the expected
number of reads with the mutation is about $4$. So, more sequencing increases
the chance of detecting a mutation.

We may also have reads in the germline sequencing to show the other base
(sequencing error or contamination) making it harder to identify the mutation.

## 4 Recurrently affected genes

More sequencing helps with the detection of mutations in a sample, but se-
quencing is expensive. Given a finite budget there will be a tension between
sequencing individual samples to enough depth and including more samples.

If a gene is mutated in all samples (think TP53 in serous ovarian cancer) we
probably don’t need many samples to identify it, but if a gene is mutated in $2\%$
of cases then we will probably need a large sample size.

The size and composition of the gene are also important. Huge genes like
TTN are likely to be repeatedly mutated by chance. The background mutation
rate in the cancer is therefore also important.

The Mutsig family of programmes are the most popular for this task:
[https://software.broadinstitute.org/cancer/cga/mutsig](https://software.broadinstitute.org/cancer/cga/mutsig)

## 5 Selection of samples to sequence

Typically, we don’t know the size of the cancer genome in our samples, nor the
precise percentage of tumour in them. We do have the pathologist’s estimate
of the tumour percentage, but for various reasons this isn’t a great estimate
for our purposes. It is correlated with what we’ll see from the sequencing, but
doesn’t agree terribly well.

The studies with which I have been involved have used a threshold (e.g.
include the sample if the pathologist’s estimate is greater than $40\%$ cancer)
and applied the same amount of sequencing to each sample (although usually
different amounts for the tumour and germline samples).

For a tumour that is being included, we may have to choose between many
different samples, each of which will require assessment.

## 6 A cheap test

Suppose we have a test that allows for a cheap assessment of the size of the
genome and the proportion of tumour in the sample.

## 7 Experimental design scenarios

There are some other questions that we could ask, but the key one is, given a
set of potential samples for sequencing, and a finite budget for sequencing, how
do we best divide the sequencing amongst samples?