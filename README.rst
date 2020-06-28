=========
LCMLUtils
=========

^^^^^^^^^^^^^^^^^^
What is LCMLUtils?
^^^^^^^^^^^^^^^^^^

LCMLUtils  is a library created to facilitate the use of the FAO LCML standard for the management of geospatial land cover data. 

The library is written in Python, using the Django framework, and offers several features including:

  - Data structures for the representation of land cover classes and legends based on the LCML standard;
  - Introspection mechanisms of Basic Elements, as defined in the XSD validator
  - Graphical representation of land cover classes.

The library also implements the similarity assessment described in the article "Object-based similarity assessment using Land Cover Meta Language (LCML): concept, challenges and implementation", oriented to the comparison between different land cover legends.

For reproducing the experiments in the article, please go to the "Similarity Assessment" tab, use "Cox's Bazar" as reference legend and "SEEA" as query legend, leaving similarity threshold at 50%. Similarity assessment is triggered by pushing the "Query/Remap..." button. Please wait a few seconds for the results to appear.

^^^^^^^^^^^^^^^^^
Try out LCMLUtils
^^^^^^^^^^^^^^^^^

If you want to try out LCMLUtils, visit the demo at http://www2.lcmlutils.eu


^^^^^^^^^^
References
^^^^^^^^^^

If you have used LCMLUtils in a scientific publication, we would like citations to the following paper:
N. Mosca, A. D. Gregorio, M. Henry, R. Jalal and P. Blonda, "Object-based similarity assessment using Land Cover Meta Language (LCML): concept, challenges and implementation," in IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, doi: 10.1109/JSTARS.2020.3003888.




^^^^^^^^^^^^
Dependencies
^^^^^^^^^^^^
 * Django==1.8.7
 * django-bootstrap3==11.0.0
 * djangorestframework==2.4.8
 * lxml==4.2.5
 * requests==2.21.0
 * certifi==2018.11.29
 * openpyxl==2.5.12

^^^^^^^^^^^^^^^^^^^^^
Frontend dependencies
^^^^^^^^^^^^^^^^^^^^^
 * Bootstrap3 is used in the frontend (https://getbootstrap.com/docs/3.3/).
 * Bootstrap-tour (https://github.com/sorich87/bootstrap-tour)
 * Class graph visualization uses a customized version of d3.js-class-diagram-example (https://github.com/hnakamur/d3.js-class-diagram-example)

^^^^^^^^^^^^^^^^^^^^^
Data sources
^^^^^^^^^^^^^^^^^^^^^
 * for information about Sylhet and Cox's Bazar land cover classes please refer to Rashed et al., "Toward Efficient Land Cover Mapping: An Overview of the National Land Representation System and Land Cover Map 2015 of Bangladesh", IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, Volume 12 No 10, DOI: 10.1109/JSTARS.2019.2903642
 * SEEA land cover classes provided by Antonio di Gregorio, for additional information please refer to https://seea.un.org/content/land-accounts


^^^^^^^
Install
^^^^^^^
 * Using virtualenv package is optional but recommended
 * Install LCMLUtils by typing the following commands (optional commands starts with #) to the terminal::

     git clone https://github.com/cnr-stiima-vci/LCMLUtils.git
     cd LCMLUtils
     # optional: virtualenv myenv
     # optional: source myenv/bin/activate
     pip3 install -r requirements.txt
     python3 manage.py migrate
     python3 manage.py createsuperuser
     python3 manage.py runserver
     
 * Launch a web browser on http://localhost:8000/






