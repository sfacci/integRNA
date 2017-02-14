from scripts import tbase_req, ensembl_req, ncbi_req
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from dbquery.models import TarBase, Ensembl, miRDB, NCBI
from dbquery.forms import SearchMainForm
from dbquery.custom_tables import TarBaseTable, EnsemblTable, miRDBTable, NCBITable
from xml.dom import minidom
import django_tables2 as tables
from django_tables2 import RequestConfig
import re
        
def index(request):
	return redirect('dbquery:search')
	
#main user /search/ form view
def search(request):
    if request.method == 'POST': #the form has been submitted
        #form has been defined in models.py
        form = SearchMainForm(request.POST) #bound form
        if form.is_valid(): #validations have passed
			#get user data
			miRNA = form.cleaned_data['miRNA_name']
			
			#get xml
			success = tbase_req(miRNA)
			if success == True:
				return redirect('dbquery:mirnaresults', search_id=miRNA)
			else:
				return HttpResponse("something went wrong with the query to TarBase.")
    
    else: #create an unbound instance of the form
        form = SearchMainForm(initial={'miRNA_name':'hsa-let-7a-5p'})
    # render the form according to the template, context = form
    return render(request, 'dbquery/search.html', {'form':form})


#display results page: /search/<search_id>/mirnaresults/ from requested search
def mirna_results(request, search_id):

	#search_id is a TarBase/miRDB miRNA accession number
	if re.match(r'^([a-z]{3}\-){2}', search_id):
		kwargs = {'miRNA_name__contains':search_id}
		queryset = TarBase.objects.filter(**kwargs)
		table1 = TarBaseTable(queryset)

		#retrieve data from the db and create an HTML table
		kwargs = {'mirdb_id__contains':search_id}
		queryset = miRDB.objects.filter(**kwargs)
		table2 = miRDBTable(queryset)
	else:
		return HttpResponse("Could not find any matches.")
	#create table to display in template
	#table1.paginate(page=request.GET.get('page', 1), per_page=25)
	#table2.paginate(page=request.GET.get('page', 1), per_page=25)
	RequestConfig(request).configure(table1)
	RequestConfig(request).configure(table2)
	return render(request, 'dbquery/mirnaresults.html', {'table1':table1, 'table2':table2, 'search_id':search_id} )

#display results page: /search/<search_id>/generesults/ from requested search
def gene_results(request, search_id):

	#search_id is an Ensembl ID
	if re.match(r'^ENSG[0-9]+', search_id):
		#query the Ensembl REST service
		success = ensembl_req(search_id)
		#retrieve data from the db and create an HTML table
		kwargs = {'gene_id__contains':search_id}
		queryset = Ensembl.objects.filter(**kwargs)#.select_related('hgnc_symbol')
		table = EnsemblTable(queryset)
	
	#search_id is an NCBI_gene mRNA accession number
	elif re.match(r'^[N|X]M_[0-10\(\)]+', search_id):
		success = ncbi_req(search_id)
		if success == True:
			kwargs = {'ncid__contains':search_id}
			queryset = NCBI.objects.filter(**kwargs)
			table = NCBITable(queryset)
		else:
			message = "No results were found."
			return render(request, 'dbquery/generesults.html', {'message':message, 'search_id':search_id} )		
		
	else:
		message = "We're sorry, this feature has not been implemented yet."
		return render(request, 'dbquery/generesults.html', {'message':message, 'search_id':search_id} )
	#create table to display in template
	#table.paginate(page=request.GET.get('page', 1), per_page=25)
	RequestConfig(request).configure(table)
	return render(request, 'dbquery/generesults.html', {'table':table, 'search_id':search_id} )
	
#display page: /search/<search_id>/ of requested search
#detail is skipped over by form submission but can be accessed later
def detail(request, search_id):
	return render(request, 'dbquery/detail.html', {'search_id':search_id} )
	#return HttpResponse("This is the detail page. Here is what you searched for.")
	

