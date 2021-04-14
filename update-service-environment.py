#!/bin/python3
import os
import json
import shutil
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

def createknownhosts(n, k):
  kh = ['ssh-keyscan', n]
  khrun = subprocess.run(kh, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8')
  f = open(k, 'a')
  f.write(str(khrun))
  f.close

def createnodelist(n, nl):
  f = open(nl, 'a')
  f.write(n + '\n')
  f.close

def main():
  nodeIPlist = []
  serviceshow = ['sudo', 'onegate', 'service', 'show', '--json']
  serviceresult = subprocess.run(serviceshow, stdout=subprocess.PIPE).stdout
  nodeID = getnodeID(serviceresult)
  for node in nodeID:
    vmshow = ['sudo', 'onegate', 'vm', 'show', node, '--json']
    vmresult = subprocess.run(vmshow, stdout=subprocess.PIPE).stdout.decode('utf-8')
    nodeIPlist.append(getnodeIP(vmresult))

  print('Backing up ~/.ssh/known_hosts if present.')
  khpath = '~/.ssh/known_hosts'
  khexppath = os.path.expanduser(khpath)
  if os.path.isfile(khexppath):
    shutil.move(khexppath, khexppath + '.bak')
  nlpath = os.path.expanduser('~/node-list.txt')
  if os.path.isfile(nlpath):
    os.remove(nlpath)

  print('Discovered IPs for nodes in Service:')
  for nodeIP in nodeIPlist:
    print(nodeIP)
    createknownhosts(nodeIP, khexppath)
    createnodelist(nodeIP, nlpath)
  print('List of nodes updated in ~/node-list.txt')

if __name__ == '__main__':
  main()
