================================================
What kinds of features will be for fabricate.py
================================================

For my interest, I am using fabricate.py for data processing with
> 100MB and > 100 files with one script file.

I appreciate all of developers of fabricate.py for providing such a nice
solution to automate a massive number of data processing.
It it is easier to write rather than write Makefile 
(After using fabricate, syntax of makefile seems complicated and
 hard to master).

I am satisfied with current spec of fabricate.py. But I am writing,
what could I request for update or improvement for fabricate.py.

Save .dep file during the task
==============================

.dep cache does not saved when any run aborted.
It may loses much time when fabricate manages long or large number of tasks.

It seems that this will be solved by adding self.save_deps() method in build.done() but may causes performance degradation.

On the other hand, I do not understand whether the operations on build._deps build.hash_cache, build.save_deps are thread-safe.

control runner and hasher for each fabricate.run
=================================================

StraceRunner and md5_hasher seems the best to confirm identity of files, but it may takes long time.

So I would like to control runner and hasher applied on each fabricate.run()
by giving hasher and runner options like

.. code-block :: python

    # proc1, filter and pickup elements from 'largefile??'
    # and join and output to 'proc1out'
    # largefile?? is very large so I would like to run md5_hasher 
    #  instead of md5_hasher

    fabricate.run('proc1', '-o', 'proc1out',
      'largefile01', 'largefile02', 'largefile03',
      group='proc1out', hasher=fabricate.mtime_hasher)

    # proc2 get statistical info from pro1out and write to 
    fabricate.run('proc2', '-o', 'proc2out', 'proc1out',
      group='proc2out', after='proc1out', hasher=fabricate.md5_hasher)

    # proc3, I would like run this always and anyway
    fabricate.furn('cat', 'proc2out', after='proc2out',
      runner=fabricate.AlwaysRunner)

runner
------

It would be easy to implement, to add runner option in Builder._run() method

hasher
------

On the other hand, It seems to take some amount of modification in order to allow changing hash algorithm for each run in one build,

Currently, Build.hash_cache consists of {'filename':{some kind of hash value}
}, there is no information on hash algorithm. It may cause,

.. code-block:: python

    run('proc1', 'file', hasher=md5_hasher) # hash_cache['file'] 
                                            #   <- md5_hasher('file')
    run('proc2', 'file', hasher=mtime_hasher) # hash_cache['file']
                                              #  <-mtime_hasher('file')
    run('proc3', 'file', hasher=md5_hasher) # md5_hash value for 'file'
                                            # has been lost lost

Additionally, _deps (and .deps file) does not include information on hash_algorithm neither. This means that discussion will be needed how to ver-up .deps file structure

manage stdout, stderr, redirection
==================================

Is it possible to specify stdin and stdout for the argument of fabricate.run()

For example, how to embed 'cat a.txt b.txt > c.txt' ?

pass python code to fabricate.run
=================================

.. code-block:: python

	import fabricate
	import json

	def dump_json():
	    """ split and make dict consists of (1st_column, rest) """
	    d = {}
	    for line in open('output.txt', 'r'):
	       sps = line.split()
	       d[sps[0]] = sps[1:]
	    
	   with open('dict.json') as f:
	       json.dump(d, f)

	def build():
	     # run external program to make output.txt
	    fabricate.run('mkoutput', 'output.txt', group='output')
	    # run embedded function
	    fabricate.run(__file__, 'dump_json', after='output')

	if __name__ == '__main__':
	    # fabricate.main() simply applies 'eval' for each cmdline args 
	    fabricate.main()


