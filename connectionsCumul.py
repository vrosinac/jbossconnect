#!/usr/bin/env python
import re
import sys

linenumber=0

#initialize the pool counters
i = 1
pool =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
ThreadInError=10000000   
timeStamp="."

with open(sys.argv[1], "r") as inputfile :
    line1 = inputfile.readline()
    linenumber = linenumber+1

    while line1:
        match0 =  re.search("(.*)\[org.jboss.jca.core.connectionmanager.pool.strategy(.*)", line1)
        if match0:
            timeStamp = match0.group(1)
            match1 =  re.search("(.*)default task-(.*)\) (.*)getConnection(.*)", match0.group(2))  
            if match1:
                taskId = int(match1.group(2))  
                pool[taskId] = pool[taskId] +1
                #print("match1")
               
            else:
                match2 =  re.search("(.*)default task-(.*)\) (.*)returnConnection(.*)", match0.group(2))  
                if match2:
                    taskId = int(match2.group(2)) 
                    pool[taskId] = pool[taskId] -1
                    #print("match2")
                
                else:
                    match3 =  re.search("(.*)Thread-(.*) \((.*)getConnection(.*)", match0.group(2))  
                    if match3:
                        taskId = int(match3.group(2)) 
                        pool[taskId] = pool[taskId] +1
                        #print("match3")
                    else:
                        match4 =  re.search("(.*)Thread-(.*) \((.*)returnConnection(.*)", match0.group(2))  
                        if match4:
                            taskId = int(match4.group(2)) 
                            pool[taskId] = pool[taskId] -1
                           # print("match4")
                    
                        else:
                            matchError =  re.search("(.*)Thread-(.*) \((.*)Throwable while attempting to get a new connection(.*)", match0.group(2))  
                            if matchError:
                                ThreadInError = int(matchError.group(2))
                                pool[ThreadInError] = pool[ThreadInError] -1
                                #print("matchErrror")
                            
                        
                            
        i=1 
        cumul=0        
        while i <  35:
            if (pool[i]) == 0:
                print ".",
            else:
                print str(pool[i] ) ,
                cumul=cumul +  pool[i]   
            i += 1
        if (ThreadInError > 100000):    
            print "   "  +str(cumul) +"                    line: " +str(linenumber) + "   " + timeStamp,
        else:
            print "   "  +str(cumul) +"                    line: "  +str(linenumber) + "   " + timeStamp +"         **************  " + "thread " + str(ThreadInError) + " **************" ,
        
        print                      
        
        line1 = inputfile.readline()
        linenumber = linenumber+1
        ThreadInError=10000000