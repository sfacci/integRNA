import django_tables2 as tables
from django.utils.safestring import mark_safe
from dbquery.models import TarBase, miRDB, Ensembl, NCBI, HUGO

#for miRNA results page
class TarBaseTable(tables.Table):
	#override gene id column with links
	gene_id = tables.TemplateColumn('<a href="/search/{{record.gene_id}}/generesults/">{{record.gene_id}}</a>')
	class Meta:
		model = TarBase
		fields = ('gene_id','gene_target','region','ver_method','result','reg_type','species','source')


#for miRNA results page
class miRDBTable(tables.Table):
	#override gene id column with links
	pred_target = tables.TemplateColumn('<a href="/search/{{record.pred_target}}/generesults/">{{record.pred_target}}</a>')
	class Meta:
		model = miRDB
		fields = ('pred_target','score')
				
#div wrapped to control column width
class DivWrappedColumn(tables.Column):
    def __init__(self, classname=None, *args, **kwargs):
        self.classname=classname
        super(DivWrappedColumn, self).__init__(*args, **kwargs)
    def render(self, value):
        return mark_safe("<div class='" + self.classname + "' >" +value+"</div>")


#for gene results page
class HUGOTable(tables.Table):
	class Meta:
		model = HUGO
		
#for gene results page
class EnsemblTable(tables.Table):
	entrez_id = tables.TemplateColumn('{{record.entrez_id}}<br/><a href="http://www.ncbi.nlm.nih.gov/gene/?term={{record.entrez_id}}">View record at Entrez Gene</a>')
	hgnc_id = tables.TemplateColumn('{{record.hgnc_id}}<br/><a href="http://www.genenames.org/cgi-bin/gene_symbol_report?hgnc_id={{record.hgnc_id}}">View record at HUGO</a>')
	######################
	#hgnc_official_symbol = tables.Column(accessor='HUGO')
	######################
	wiki_id = tables.TemplateColumn('{{record.wiki_id}}<br/><a href="http://www.wikigenes.org/e/gene/e/{{record.wiki_id}}.html">View record at Wiki Gene</a>')
	sequence = DivWrappedColumn(classname='narrow_seq')
	class Meta:
		model = Ensembl
		fields = ('entrez_id','description','hgnc_id','wiki_id','sequence')
		attrs = {'classname': 'ensembl'}

#for gene results page
class NCBITable(tables.Table):
	target_ens_id = tables.TemplateColumn('<a href="/search/{{record.target_ens_id}}/generesults/">{{record.target_ens_id}}</a>')
	#foreigncolumn = tables.Column(accessor='Ensembl.gene_id')
	class Meta:
		model = NCBI
		fields = ('target_ens_id','hugo_off_symbol','hugo_name')

