# MTP - The Mersenne Twister Pseudo-random number generator
MTP is an implementation of the 32-bit Mersenne Twister pseudo-random number generator in Python. This is the same RNG that Python's 'random' module uses, as well as many other programming languages including R, Matlab, Ruby, Julia, and Common Lisp.

Most of my understanding of this algorithm came thanks to the following sites:
* http://www.eetimes.com/document.asp?doc_id=1274550 - a tutorial on linear feedback shift registers
* http://www.quadibloc.com/crypto/jscrypt.htm - the pages on the Mersenne Twister and LFSRs in particular
* https://en.wikipedia.org/wiki/Mersenne_Twister - background information and pseudocode

## Usage
To initialize the RNG:
```python
generator = mersenne_rng(seed = 123)
```
If you don't pass it a seed, it will default to 5489

To generate a random number:
```
random_number = generator.get_random_number()
```
