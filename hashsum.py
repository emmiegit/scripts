import hashlib, sys

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        try:
            algorithms = hashlib.algorithms_guaranteed
        except AttributeError:
            algorithms = hashlib.algorithms
        
        print("Usage: hashsum.py [algorithm] [file1] [file2] [file3] ...")
        print("Supported algorithms: " + ', '.join(sorted(algorithms)))
        exit(1)
    else:
        try:
            hash = getattr(hashlib, sys.argv[1].lower().replace("-", ""))
        except:
            print("Hash algorithm \"%s\" not found." % sys.argv[1])
        
        for fn in sys.argv[2:]:
            try:
                fh = open(fn, 'rb')
                digest = hash(fh.read()).hexdigest()
                print("%s: %s" % (fn, digest))
                fh.close()
            except Exception as ex:
                print("%s: %s" % (fn, ex))
