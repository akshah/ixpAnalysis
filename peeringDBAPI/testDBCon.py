# unauthenticated to default URL (unless ~/.peeringdb/config.yaml exists)
from peeringdb import PeeringDB
import pprint
pdb = PeeringDB()
#net = pdb.type_wrap('net')
#val=net.all(asn=6762)
pp=pprint.PrettyPrinter()
#pp.pprint(val)
pp.pprint(pdb.asn(17676))
