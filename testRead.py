import cPickle
from Catalogue import Catalogue
r = cPickle.load( open( "save.p", "rb" ) )
print r.s
print r.t 
print r.u