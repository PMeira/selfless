selfless
========

A small experimental, work-in-progress, module for implicit "self" support in Python (in some restricted contexts), targeting Python 2.7 (if possible) and 3.6+.

Documentation and explicit examples will be added when the module is more mature. This is used as a dependency for another module; when that module is made public, the existence of this module will be justified.

What is this?
=============
If you don't know, you probably don't need it. It can be used as an example of AST transformer though.

In some contexts (this will be clarified in the future), writing and reading `self.` polutes the code and can be cumbersome. This module tries to alleviate that in some specific contexts.

How does it work?
=================

This module inspects the source code of a class, extracts its AST and inserts `self.` for variables in a list (if provided) or variables not in the global and local contexts at the time of import. 

Finally, the transformed AST is compiled and inserting into the original context of the class `selfless` was applied to.

*I'm also trying to restrict the transform to the `with` keyword but it's a work-in-progress.*

