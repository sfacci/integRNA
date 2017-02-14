# A class project to demonstrate data warehousing interfaced with REST API calls
The target audience for the site would be a researcher who'd like to find out more information about target genes for small non-coding RNAs (ncRNA, miRNA, siRNA).
-Experimentally supported miRNA target data from TarBase was obtained via their REST interface
-Data about predicted targets was downloaded from miRDB and subsequently loaded into SQLite DB
-Further information about target genes is looked up from the Ensembl API service, NCBI, and Uniprot, if available
-HUGO (Human Genome Organisation) was used to get gene ontology and nomenclature
-OMIM (Online Mendelian Inheritance in Man) was used to get information about the gene and its phenotypes

- Some basic validation is done on the input form before submission
- If a term has already been looked up, the program will retrieve from the database instead of making additional API calls.
- Yes, it is very ugly. The project was mostly to work on backend funtionality. Hopefully in the future I can practice some responsive design on it.


The original Heroku readme for deploying the Django project is below


# python-getting-started

A barebones Python app, which can easily be deployed to Heroku.

This application support the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).  Also, install the [Heroku Toolbelt](https://toolbelt.heroku.com/).

```sh
$ git clone git@github.com:heroku/python-getting-started.git
$ cd python-getting-started
$ pip install -r requirements.txt
$ python manage.py syncdb
$ foreman start web
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master
$ heroku run python manage.py syncdb
$ heroku open
```

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)

