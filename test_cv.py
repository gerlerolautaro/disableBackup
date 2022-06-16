from cvpysdk.client import Clients
from cvpysdk.client import Client
from cvpysdk.agent import Agent
from cvpysdk.subclient import Subclient
from cvpysdk.commcell import Commcell
from cvpysdk.backupset import Backupset
import fuzzybunnies as fz
from cvpysdk.instance import Instance

console_name="x2qcvc01.ess.xomlab.com"

def get_CS_connection(console_name,u,p):
    # Creates and return a Commcell Connection 
    try:
        cs=Commcell(console_name,u,p)
        print("\n Connection created to: ",cs.commserv_name)
        
        
    except:
        print(0)
        print("\nCant connect to Commcell at get_CS_connection", console_name)
    
    return cs
    

if __name__ == "__main__":
    commserve = "x2qcvc01.ess.xomlab.com"
    user_name = fz.user_name
    pswd = fz.pswd
    cs = get_CS_connection(commserve, user_name, pswd)
    
    clients = Clients(cs) # Init commserve clients
    all_clients = clients.all_clients # Gather all the clients in the commserve
    bkp_clients = [client for client in all_clients if "bkp" in client and "ess" not in client] # Create a list of clients with "bkp" in the name
    for client in bkp_clients:
        bkp = Client(cs, client) # Init each client
        print(bkp)
        fs = Agent(bkp, "file system") # Init file system Agent
        print(fs)
        instance =  Instance(fs, "defaultinstancename") # Init File System instance
        print(instance)
        dBS = Backupset(instance, "defaultBackupSet") # Init defaultBackupSet
        print(dBS)
        subclient = Subclient(dBS, "default") # Init default subclient
        print(subclient)
        properties = subclient.properties # Gather the subclient properties
        if properties["commonProperties"]["enableBackup"] == True: # If has backup enabled
            properties["commonProperties"]["enableBackup"] = False # Then disable it 
            subclient.update_properties(properties) # And update properties
            #print(properties)
    
    cs.logout



    