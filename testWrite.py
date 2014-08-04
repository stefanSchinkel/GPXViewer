import cPickle
from Catalogue import Catalogue

r = Catalogue()

cPickle.dump( r, open( "save.p", "wb" ) )
