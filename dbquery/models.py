from django.db import models

# response data from queries for miRNA accession numbers
class TarBase(models.Model):
	#--------------miRNA response data----------
	miRNA_name = models.CharField('miRNA Accession number', max_length=30)
	species = models.CharField(max_length=50, null=True, blank=True)
	ver_method = models.CharField('verification method', max_length=50, null=True, blank=True)
	reg_type = models.CharField('regulation type', max_length=10, null=True, blank=True)
	result = models.CharField('experimental result', max_length=10, null=True, blank=True)
	source = models.CharField('source database', max_length=10, null=True, blank=True)
	#gene name	
	gene_target = models.CharField('experimentally verified gene target name',max_length=25, null=True, blank=True)
	#ENSEMBL id
	gene_id = models.CharField('gene id', max_length=25, null=True, blank=True)
	region = models.CharField('target location', max_length=25, null=True, blank=True)
	
	def __unicode__(self):  
		return unicode(str(self.id) + ": " + self.miRNA_name + ", " + gene_target) or 'no objects found!'

class HUGO(models.Model):
	hgnc_id = models.CharField('HGNC ID', max_length=25, unique=True)
	hugo_off_symbol = models.CharField('HUGO Official Gene Symbol', max_length=25, null=True, blank=True)
	locus_type = models.CharField('HUGO Locus Type', max_length=100, null=True, blank=True)
	gene_loc = models.CharField('HUGO Gene Location', max_length=20, null=True, blank=True)
	def __unicode__(self): 
		return unicode(str(self.id) + ": " + self.hgnc_id + ", " + self.hugo_off_symbol) or 'no objects found!'
	

class Ensembl(models.Model):
	gene_id = models.CharField('gene id', max_length=25, unique=True)
	sequence = models.CharField(max_length=3000, null=True, blank=True)
	entrez_id = models.CharField('Entrez Gene primary id', max_length=25, null=True, blank=True)
	hgnc_id = models.CharField('HGNC primary id', max_length=25, null=True, blank=True)
	wiki_id = models.CharField('WikiGene primary id', max_length=25, null=True, blank=True)
	description = models.CharField('Gene description', max_length=250, null=True, blank=True)
 	def __unicode__(self): 
		return unicode(str(self.id) + ": " + self.gene_id) or 'no objects found!'

class NCBI(models.Model):
	ncid = models.CharField('NCBI ID', max_length=25) #NM_0000000
	target_ens_id = models.CharField('Ensembl ID', max_length=25, null=True, blank=True, unique=True)
	#target_ens_id = models.ForeignKey(Ensembl, to_field='gene_id')
	hugo_off_symbol = models.CharField('HUGO Official Symbol', max_length=25, null=True, blank=True)
	hugo_name = models.CharField('Hugo Gene Name', max_length=150, null=True, blank=True)
	def __unicode__(self): 
		return unicode(str(self.id) + ": " + self.hugo_off_symbol + ", " + self.hugo_name) or 'no objects found!'
		
class UniProt(models.Model):
	uniprot_id = models.CharField(max_length=25) #one
	go_term = models.CharField(max_length=100) #many
	def __unicode__(self):
		return self.uniprot_id
		
class miRDB(models.Model):
	mirdb_id = models.CharField('miRNA accession number', max_length=25)
	pred_target = models.CharField('predicted target mRNA', max_length=25, null=True, blank=True) 
	score = models.DecimalField('target score', max_digits=13, decimal_places=10)
	def __unicode__(self):
		return self.mirdb_id + ", " + pred_target or 'no objects found!'


