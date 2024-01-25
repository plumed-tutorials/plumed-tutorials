import sys
import getopt
import yaml

def merge_counts( nreplicas ) :
    # Read the first yaml
    with open("_data/action_count-0.yml", "r") as stream:
        try:
            counts = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # Convert from list to dictionary
    dcounts = {}
    for item in counts :
        name = item["name"]
        dcounts[name] = item["number"]

    for i in range(1,nreplicas) :
        fname = "_data/action_count-" + str(i) + ".yml"
        with open(fname) as stream :
             try:
                 tcounts = yaml.safe_load(stream)
             except yaml.YAMLError as exc:
                 print(exc)
        for item in tcounts : 
            name = item["name"]
            dcounts[name] += item["number"]

    action_list = []
    for key, value in dcounts.items() : action_list.append( {'name': key, 'number': value } )
    with open("_data/actioncount.yml","w") as file : 
         yaml.safe_dump( action_list, file ) 

if __name__ == "__main__" : 
    nreplicas, argv = 1, sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"hn:",["nreplicas="])
    except:
       print('mergecounts.py -n <nreplicas>')

    for opt, arg in opts:
       if opt in ['-h'] :
          print('compile.py -n <nreplicas> -r <replica number>')
          sys.exit()
       elif opt in ["-n", "--nreplicas"]:
          nreplicas = int(arg)
    print("MERGING COUNTS FROM", nreplicas, "REPLICAS.")
    merge_counts( nreplicas )
