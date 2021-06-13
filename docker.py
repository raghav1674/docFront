#!/usr/bin/python3 

from datetime import datetime 
import subprocess as sp
import json 
import enum


# representing the state of container
class STATUS(enum.Enum):

    STOPPED = 'STOPPED'
    RUNNING = 'RUNNING'
    INACTIVE = 'INACTIVE'
    EXITED = 'EXITED'
    REMOVED = 'REMOVED'


# docker representation
class Docker:
    

    # List of all containers 
    __containers = [] 
    
    # constructor

    def __init__(self,name,image,port_mapping=None):

        self.id = len(Docker.__containers) + 1 
        self.created_at = datetime.now().isoformat() 
        self.name = name 
        self.image = image 
        self.port_mapping = port_mapping
        self.status = STATUS.INACTIVE.value
        self.deleted_at = ''

    # serialize Docker object to json format
    def __serialize(self):
    
        container = {

            "name": self.name,
            "image": self.image,
            "status": self.status,
            "createdAt": self.created_at,
            

        }

        if self.deleted_at:

            container["deletedAt"] = self.deleted_at 

        return json.dumps(container)
    

    # run the container in background 
    def run(self):

        cmd = "sudo docker container run -dit --name {} {}".format(self.name,self.image) 

        status,output = sp.getstatusoutput(cmd) 
        
        if status == 0:
            
            self.status = STATUS.RUNNING.value  

            Docker.__containers.append({ "_id": self.id, "data": self.__serialize()})

            return self.__serialize()
        else:
            
            self.status = STATUS.EXITED.value
            
            return self.__serialize() 
    

    # stop and remove the container
    def delete(self):

        cmd_to_stop  = "sudo docker container stop {}".format(self.name) 
        
        cmd_to_rm = "sudo docker container rm {}".format(self.name)
        
        stop_status,output = sp.getstatusoutput(cmd_to_stop) 
        
        if stop_status == 0:
            
            self.status = STATUS.STOPPED.value  
            
            removed_status,output = sp.getstatusoutput(cmd_to_rm)

            if removed_status == 0:
                
                self.status = STATUS.REMOVED.value 
                
                self.deleted_at = datetime.now().isoformat()
                
                Docker.__containers = list(filter(lambda container: container["_id"] != self.id,Docker.__containers))

                return self.__serialize() 
            
        
        else:
            self.status = STATUS.EXITED.value
            
            return self.__serialize() 
    
    # get all the containers 
    @classmethod
    def get_all(cls):

        return json.dumps(cls.__containers)

    # get a container 
    @classmethod
    def get(cls,pk):

        return json.dumps({}) if pk > len(Docker.__containers) else cls.__containers[pk-1]["data"] 






   
