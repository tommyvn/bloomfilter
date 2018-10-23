# bloom filter
A low level functional bloom filter

## What does it do?

* approximate length
* union
* intersection
* contains (currently done by an equality check on intersection)

## Can I use it?

Sure, it's Apache licensed, well tested, pip installable from github, API stable and I'm close to certain it does what it says on the tin. Make sure both producers and consumers of the bloom filter itself use the same inputs tho...

## Why did I write this?

I wanted to understand how bloom filters worked at their most basic level, no complex classes wrapped around them or arrays of True/False representing what should really just be some bytes easily manipulated with bitmasks like I've seen in other bloom filter implementations.

To that end
* the bloom filter is represented by a Python int. Python takes care of making it a variable size int which makes things a lot easier than other languages.
* the functions are pure functions that hold no state.
* the default hash functions are sha256 with the hash number pre-pended as salt.

## What next?

Something I'd like to explore is having uuids as the elements and using the uuid itself as the hash (+ count as salt). [Wikipedia tells me that this is known as a trivial hash function](https://en.wikipedia.org/wiki/Hash_function#Trivial_hash_function) and in a world where primary keys are often uuids this seems to make a lot of sense.
