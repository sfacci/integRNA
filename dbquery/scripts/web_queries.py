import urllib,urllib2
import requests, sys
import json
import re
from xml.dom import minidom
from dbquery.models import TarBase, Ensembl, NCBI
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
import xml.etree.ElementTree as ET

def tbase_req(query):
	url = 'http://62.217.127.8/DianaTools/tarbaseApi?'
	if(re.match(r'[a-z]{3}-.+',query)): #query input is in miRNA format
		params = "mirnas={}".format(query)
	elif(re.match(r'ENSG.+',query)): #query input is in Ensembl gene format
		params = "genes={}".format(query)
	else:
		#error message about bad request			
		return HttpRedirect("Badly formatted request.")

	url = url + params
	request = urllib2.Request(url)
	contact = "sarah.e.facci@gmail.com"
	request.add_header('User-Agent', 'Python %s' % contact)
	response = urllib2.urlopen(request)

	#response is in xml format
	xml = minidom.parse(response)
	
	#parse xml
	if xml is None:
		return HttpRedirect("No results were found.")
	
	#loop through all results
	results = xml.getElementsByTagName('interaction')
	for interaction in results:
		#parse xml into fields
		rank = interaction.getAttribute('rank')
		orgName = interaction.getAttribute('orgName')
		geneName = interaction.getAttribute('geneName')
		geneId = interaction.getAttribute('geneId')
		papers = interaction.getElementsByTagName('paper')
		for paper in papers:
			source = paper.getAttribute('source')
			method = paper.getAttribute('method')
			valid = paper.getAttribute('valid')
			regulation = paper.getAttribute('regulation')
			region = paper.getAttribute('region')
	
			#check if object exists in table first
			result_count = TarBase.objects.filter(miRNA_name=query, species=orgName, ver_method=method, reg_type=regulation, result=valid, source=source, gene_target=geneName, gene_id=geneId, region=region).count()
			if result_count > 0:
				continue
			else:
				#create TarBase objects (entry in table)
				t = TarBase.objects.create(miRNA_name=query, species=orgName, ver_method=method, reg_type=regulation, result=valid, source=source, gene_target=geneName, gene_id=geneId, region=region)
				#commit to database
				t.save()
	return True
	
def ensembl_req(query):
	url = 'http://rest.ensembl.org/'

	#get sequence
	service = 'sequence/id/'
	params = '{}?content-type=text/plain'.format(query)
	url_seq = url + service + params
	request = urllib2.Request(url_seq)
	contact = "sarah.e.facci@gmail.com"
	seq = urllib2.urlopen(request).read()	#response is in plain text
	
	#get ids in other databases
	service = 'xrefs/id/'
	params = '{}?content-type=application/json'.format(query)
	url_ids = url + service + params
	request = urllib2.Request(url_ids)
	contact = "sarah.e.facci@gmail.com"
	response = urllib2.urlopen(request)	#text json format
	data = json.load(response) 
	for record in data: #each dict in response - should be only one

		#Entrez gene	
		if record.get('dbname',None) == 'EntrezGene':
			Entrez_id = record.get('primary_id',None)
			desc = record.get('description', None)
		#HGNC symbol
		elif record.get('dbname',None) == 'HGNC':
			HGNC_id = record.get('primary_id',None)
		#Wikigene (link)
		elif record.get('dbname',None) == 'WikiGene':
			Wiki_id = record.get('primary_id',None)
	
	#check if object exists
	result_count = Ensembl.objects.filter(gene_id=query, sequence=seq,entrez_id=Entrez_id,hgnc_id=HGNC_id,wiki_id=Wiki_id,description=desc).count()
	if result_count == 0: #object not already in database
		#create object
		e = Ensembl.objects.create(gene_id=query, sequence=seq,entrez_id=Entrez_id,hgnc_id=HGNC_id,wiki_id=Wiki_id,description=desc)
		#commit to database
		e.save()
	return True 
	
def ncbi_req(query):
	database = 'gene'
	
	#esearch gives the count of results and the gene id
	url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
	service = 'esearch.fcgi?db={}&term={}&usehistory=y'.format(database,query)
	url_complete = url + service
	request = urllib2.Request(url_complete)
	response = urllib2.urlopen(request)
	xml = minidom.parse(response)
	
	node = xml.getElementsByTagName('Id')
	gene_id = xml.getElementsByTagName('Id')[0].firstChild.data
	query_key = xml.getElementsByTagName('QueryKey')[0].firstChild.data
	web_env = xml.getElementsByTagName('WebEnv')[0].firstChild.data
	
	#efetch gets all the details
	service = 'efetch.fcgi?db={}&query_key={}&webenv={}&rettype=xml'.format(database, query_key, web_env)
	url_complete = url + service
	request = urllib2.Request(url_complete)
	response = urllib2.urlopen(request)

	if response == None:
		return False
	xml = ET.parse(response)
	
	ens_id=''
	for node in xml.findall(".//Gene-ref_db/Dbtag"):
		for x in node.findall(".//Dbtag_db"):
			if x.text == "Ensembl":
				#get Ensembl id
				ens_id = node.find(".//Dbtag_tag/Object-id/Object-id_str").text
			
	#get HUGO Official symbol
	hugo = ''
	gene_name = ''
	for prop in xml.findall(".//Entrezgene_properties/Gene-commentary/Gene-commentary_properties"):
		for comment in prop.findall(".//Gene-commentary"):
			for label in comment.findall(".//Gene-commentary_label"):
				if label.text == "Official Symbol":
					hugo = comment.find(".//Gene-commentary_text").text
				if label.text == "Official Full Name":
					gene_name = comment.find(".//Gene-commentary_text").text
				
	#get omim disease descriptions, etc?
	
	#check if object exists
	result_count = NCBI.objects.filter(ncid=query, target_ens_id=ens_id, hugo_off_symbol=hugo, hugo_name=gene_name).count()
	if result_count == 0: #object not already in database
		#create object
		n = NCBI.objects.create(ncid=query, target_ens_id=ens_id, hugo_off_symbol=hugo, hugo_name=gene_name)
		#commit to database
		n.save()
		
	return True
	
#search HUGO for HGNC:#### id
def hugo_req(query):
	#parse query
	m = re.match(r'^HGNC:(\d+)',query)
	parsed_query = m.group(1)
	#set info
	url = 'http://rest.genenames.org/fetch/hgnc_id/{}'.format(parsed_query)
	request = urllib2.Request(url)
	request.add_header('content-type','text/xml')
	response = urllib2.urlopen(request)
	#get xml
	xml = ET.parse(response)
	gene_symbol = ''
	locus_type = ''
	loc = ''
	for str in xml.findall(".//str"):
		if str.attrib.get('name') == symbol:
			gene_symbol = str.text
		if str.attrib.get('name') == locus_type:
			locus_type = str.text
		if str.attrib.get('name') == location:
			loc = str.text
				
	#check if object exists
	result_count = HUGO.objects.filter(hgnc_id=query, hugo_off_symbol=gene_symbol, locus_type=locus_type, gene_loc=loc).count()
	if result_count == 0: #object not already in database
		#create object
		n = HUGO.objects.create(hgnc_id=query, hugo_off_symbol=gene_symbol, locus_type=locus_type, gene_loc=loc)
		#commit to database
		n.save()
	return True

def uniprot_req(self,acc_id,format):
	url = 'http://www.uniprot.org/uniprot/'

	accession = acc_id
	format = 'xml'

	url += "?format={0}&query=accession:{1}".format(format, accession)

	request = urllib2.Request(url)
		#example request: http://www.uniprot.org/uniprot/?format=xml&query=accession:P13368

	 # Please set your email address here to help us debug in case of problems.
	contact = "sarah.e.facci@gmail.com"
	request.add_header('User-Agent', 'Python {}'.format(contact))
	response = urllib2.urlopen(request) #contains xml string
	xmldoc = minidom.parse(response)
	return xmldoc.toxml()
