#!/usr/bin/python3

import json 
import sys
import urllib
import requests
import os
import configparser
import jenkins
import tempfile
import xml.etree.ElementTree as ET
import argparse

# IMPORT CONFIG

config = configparser.ConfigParser()
config.read('/sources/config')


class jenkinsConf():

	def getUrl(self):
		return config['JENKINS']['ipv4_jenkins']
		
	def getToken(self):
		return config['JENKINS']['jenkins_api_token']
		
	def getUser(self):
		return config['JENKINS']['jenkins_user']
		
	def getPasswd(self):
		return config['JENKINS']['jenkins_passwd']
		
	def getGitlabName(self):
		return config['JENKINS']['gitlab_server_name_in_jenkins']
		
		

class gitlabConf():

	def getUrl(self):
		return config['GITLAB']['ipv4_gitlab']
		
	def getToken(self):
		return config['GITLAB']['gitlab_api_token']
		
	def getUser(self):
		return config['GITLAB']['gitlab_user']
		
	def getPasswd(self):
		return config['GITLAB']['gitlab_passwd']


# GITLAB

def get_project_id(projectName):
	r = requests.get('http://'+gitlabConf().getUrl()+'/api/v4/projects?name='+projectName, auth=(gitlabConf().getUser(),gitlabConf().getPasswd()), headers={'PRIVATE-TOKEN': gitlabConf().getToken()})
  
	for i in r.json():
		if i['name'] == projectName : 
			id = i['id']
	return id
  

def create_gitlab_project(projectName):
	r = requests.post('http://'+gitlabConf().getUrl()+'/api/v4/projects?name='+projectName+'&visibility=public', auth=(gitlabConf().getUser(),gitlabConf().getPasswd()), headers={'PRIVATE-TOKEN': gitlabConf().getToken()})
	return r.json()	


def delete_gitlab_project(projectName):
	id = get_project_id(projectName)
	r = requests.delete('http://'+gitlabConf().getUrl()+'/api/v4/projects/'+str(id), auth=(gitlabConf().getUser(),gitlabConf().getPasswd()), headers={'PRIVATE-TOKEN': gitlabConf().getToken()})
	return r


#JENKINS

def config_jenkins():
	server = jenkins.Jenkins('http://'+jenkinsConf().getUrl(), username=jenkinsConf().getUser(), password=jenkinsConf().getToken())
	user = server.get_whoami()
	version = server.get_version()
	print('Hello %s from Jenkins %s' % (user['fullName'], version))
	return server
  

def run_jenkins_build(projectName,branchName):
	os.system('curl --request POST -I -u '+jenkinsConf().getUser()+':'+jenkinsConf().getToken()+' http://'+jenkinsConf().getUser()+':'+jenkinsConf().getPasswd()+'@'+jenkinsConf().getUrl()+'/job/'+projectName+'/job/'+branchName+'/build?delay=0sec')
	return 0
  
def delete_jenkins_project(projectName):
	server = config_jenkins()
	if server.get_job_name(projectName)==projectName:
		server.delete_job(projectName)
		print('job removed')
	return 0
  
def create_blank_job(projectName):
	server = config_jenkins()
	if server.get_job_name(projectName)==projectName:
		print('Name already used')
	else:
		server.create_job('test',jenkins.EMPTY_CONFIG_XML)
		print('job created')
	return 0
    

def xml_generator(projectName):
	tree = ET.parse('/sources/xml_config')
	root = tree.getroot()
	for i in root.iter('credentialsId'):
		i.text = ('apidentification')
	for i in root.iter('serverName'):
		i.text = (jenkinsConf().getGitlabName())
	for i in root.iter('projectOwner'):
		i.text = (gitlabConf().getUser())
	for i in root.iter('projectPath'):
		i.text = ('root/'+projectName)
	for i in root.iter('sshRemote'):
		i.text = ('git@'+gitlabConf().getUrl()+':root/'+projectName+'.git')
	for i in root.iter('httpRemote'):
		i.text = ('http://'+gitlabConf().getUrl()+'/root/'+projectName+'.git')
	for i in root.iter('projectId'):
		i.text = (str(get_project_id(projectName)))

		
	tree.write(projectName+'_config.xml')
	return 0
	

def create_job(projectName):
	create_credential()
	xml_generator(projectName)
	
	os.system("CRUMB="+"$"+"(curl -s "+"'http://'"+jenkinsConf().getUrl()+"'/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,'+':'+',//crumb)' -u "+jenkinsConf().getUser()+":"+jenkinsConf().getToken()+")")
	os.system("curl -s -XPOST "+"'http://'"+jenkinsConf().getUrl()+"'/createItem?name='"+projectName+" -u "+jenkinsConf().getUser()+":"+jenkinsConf().getToken()+" --data-binary @"+projectName+"_config.xml -H "+"'Content-Type:text/xml'")
	print('Job created')
	os.system('rm '+projectName+'_config.xml')
	return 0


def create_credential():
	os.system("CRUMB="+"$"+"(curl -s "+"'http://'"+jenkinsConf().getUrl()+"'/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,'+':'+',//crumb)' -u "+jenkinsConf().getUser()+":"+jenkinsConf().getToken()+")")
	os.system("curl -s -XPOST \'http://"+jenkinsConf().getUser()+":"+jenkinsConf().getToken()
+"@"+jenkinsConf().getUrl()+"/credentials/store/system/domain/_/createCredentials\' --data-urlencode \'json={\"\": \"0\",\"credentials\": {\"scope\": \"GLOBAL\",\"id\": \"apidentification\",\"username\": \""+gitlabConf().getUser()+"\",\"password\": \""+gitlabConf().getPasswd()+"\",\"description\": \"api credential\",\"$class\": \"com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl\"}}\' ")
	return 0

def connect_intlib(version):
	return 0

def disconnect_intlib(version):
	return 0	

#server = config_jenkins()
#delete_jenkins_project('st-helloworld-local') 
#create_job('st-helloworld-local')
#print(get_project_id('st-helloworld-local'))



def control_remote():
	parser = argparse.ArgumentParser(description = 'Process API commands')
	parser.add_argument('projectName',type=str, help='the name of the project')
	parser.add_argument('-g , --create-gitlab', dest='create_gitlab', action='store_true', help='create Gitlab project')
	parser.add_argument('-j , --create-jenkins', dest='create_jenkins', action='store_true', help='create Jenkins project')
	parser.add_argument('--delete-gitlab', dest='delete_gitlab', action='store_true', help='delete Gitlab project')
	parser.add_argument('--delete-jenkins', dest='delete_jenkins', action='store_true', help='delete Jenkins project')
	parser.add_argument('-b, --build-job', dest='build_job', action='store_true', help='build Jenkins job')
	parser.add_argument('--blank-project', dest='blank_project', action='store_true', help='create Jenkins blank project')
	
	parser.add_argument('branchName',type=str, help='the name of the project')
	
	
	
	args = parser.parse_args()
	
	
	if args.create_gitlab==True: 
		create_gitlab_project(args.projectName)
	if args.delete_gitlab==True:
		delete_gitlab_project(args.projectName)
	if args.create_jenkins==True:
		create_job(args.projectName)
	if args.delete_jenkins==True:
		delete_jenkins_project(args.projectName)
	if args.build_job==True:
		run_jenkins_build(args.projectName,args.branchName)
	if args.blank_project==True:	
		create_blank_job(args.projectName)


control_remote()

