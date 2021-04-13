#!/bin/python3
import os
import json
import subprocess

SERVICENODE = 'MPInode'

def getnodeID(s):
  nodeslist = []
  sresult = json.loads(s)
  for items in (sresult['SERVICE']['roles']):
    if items['name'] == SERVICENODE:
      for nodes in items['nodes']:
        nodeID = nodes['deploy_id']
        nodeslist.append(str(nodeID))
  return(nodeslist)

def getnodeIP(i):
  iresult = json.loads(i)
  for items in (iresult['VM']['TEMPLATE']['NIC']):
    if items['NETWORK'] == 'vmprivnet0':
      nodeIP = items['IP']
  return(nodeIP)

def main():
  nodeIPlist = []
  serviceshow = ['onegate', 'service', 'show', '--json']
  serviceresult = subprocess.run(serviceshow, stdout=subprocess.PIPE).stdout.decode('utf-8')
  nodeID = getnodeID(serviceresult)
  for node in nodeID:
    vmshow = ['onegate', 'vm', 'show', node, '--json']
    vmresult = subprocess.run(vmshow, stdout=subprocess.PIPE).stdout.decode('utf-8')
    nodeIPlist.append(getnodeIP(vmresult))

  print('Discovered IPs for nodes in Service:')
  for nodeIP in nodeIPlist:
    print(nodeIP)

if __name__ == '__main__':
  main()
