=======
anorack
=======

-------------------
“a” vs “an” checker
-------------------

:manual section: 1
:version: anorack 0.2.6
:date: 2020-05-22

Synopsis
--------
**anorack** [*option*...] [*file*...]

Description
-----------

The English language has two indefinite articles:

+ *a*: used before words that begin with a consonant sound (e.g., *a program*, *a host*, *a user*);
+ *an*: used before words that begin with a vowel sound (e.g., *an example*, *an hour*, *an undefined variable*).

**anorack** is a specialized spell-checker
that finds incorrect indefinite articles.

Options
-------

--ipa
   Print phonemes using IPA (International Phonetic Alphabet)
   instead of ASCII phoneme mnemonics.
-h, --help
   Show help message and exit.
--version
   Show version information and exit.

Example
-------

::

   $ cat test
   a Ubuntu user
   a 8-byte word
   an username

   $ anorack test
   test:1: a Ubuntu -> an Ubuntu /u:b'u:ntu:/
   test:2: a 8 -> an 8 /'eIt/
   test:3: an username -> a username /j'u:z3n,eIm/

See also
--------

**espeak**\ (1)

.. vim:ts=3 sts=3 sw=3
