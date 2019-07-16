# Summer research internship notes
#### Reinis Cirpons 
> This repo contains notes, code and other useful stuff pertaining to my summer research internship with the
school of mathematics and statistics, supervised by Andy Lynch.

## Introduction 
TODO

## To do:
1. How do we know were done?
  * What is the end goal? 
  A: A protocol of distributing the number of reads to each sample in a manner which maximizes the power 
  of the test used to find driving mutations.
  * What metrics do we assess our allocation protocol by? 
  A: We look at the power of tests detecting driver mutations in the gene.
  * If we assume perfect knowledge, what is the best protocol we can come up with?
  * Does best change if we are targeting coverage of a specific gene instead of 
  looking at everything in general?
2. What are we permitted to do?
  * What are the inputs? 
  A: Size of genome and proportion of tumor in sample. Initially we assume this is free. 
  Later we can incorporate cost.  
  * How does the distribution proceed? Do we have to allocate reads all at once, or can we run it in rounds?
  A: Initially look at 
  * 
3. What is the case for a single sample?
  * Best strategy is to allocate all our reads.
  * What about efficiency: What is the least amount of reads we have to allocate to guarantee some metric?
4. How does the single sample case generalize?
  * Two sample case.
  * Can we generalize results? Is it more than the sum of its parts?
  * Is there something clever we can do (e.g. doing reads in rounds and adjusting)
5. How do we make our model realistic?
  * Start with a simple model for sequencing and mutations etc.
  * How to incorporate more complex effects and distributions?
6. How to we test our model?
  * Simulate reads from known tumor samples? A: I have found a review of multiple software for simulating sequencing experiments given a DNA sequence.
