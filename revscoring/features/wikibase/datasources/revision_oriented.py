import json
import csv
import os
from urllib.parse import urlencode
import urllib.request
import pywikibase
from ....datasources import Datasource 
from ....dependencies import DependentSet
from .diff import Diff

class Revision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)

        self.item_doc = Datasource(
            name + ".item_doc", _process_item_doc,
            depends_on=[revision_datasources.text]
        )
        """
        A JSONable `dict` of content for a Wikibase content.
        """

        self.item = Datasource(
            name + ".item", _process_item,
            depends_on=[self.item_doc]
        )
        """
        A `~pywikibase.Item` for the Wikibase content
        """

        self.sitelinks = Datasource(
            name + ".sitelinks", _process_sitelinks, depends_on=[self.item]
        )
        """
        A `dict` of wiki/sitelink pairs in the revision
        """

        self.labels = Datasource(
            name + ".labels", _process_labels, depends_on=[self.item]
        )
        """
        A `dict` of lang/label pairs in the revision
        """

        self.aliases = Datasource(
            name + ".aliases", _process_aliases, depends_on=[self.item]
        )
        """
        A `set` of unique aliases in the revision
        """

        self.descriptions = Datasource(
            name + ".descriptions", _process_descriptions,
            depends_on=[self.item]
        )
        """
        A `dict` of lang/description pairs in the revision
        """

        self.properties = Datasource(
            name + ".properties", _process_properties, depends_on=[self.item]
        )
        """
        A `set` of properties in the revision
        """

        self.claims = Datasource(
            name + ".claim", _process_claims, depends_on=[self.item]
        )
        """
        A `set` of unique claims in the revision
        """

        self.sources = Datasource(
            name + ".sources", _process_sources, depends_on=[self.item]
        )
        """
        A `set` of unique sources in the revision
        """

        self.qualifiers = Datasource(
            name + ".qualifiers", _process_qualifiers, depends_on=[self.item]
        )
        """
        A `set` of unique qualifiers in the revision
        """

        self.badges = Datasource(
            name + ".badges", _process_badges, depends_on=[self.item]
        )
        """
        A `set` of unique badges in the revision
        """
		
        self.external_sources_ratio = Datasource(
			name + ".external_sources_ratio", _process_external_sources_ratio, depends_on=[self.item]
		)
        """
	A `float` of the ratio between number of external references and number of claims that have references in the revision
	"""
		
        self.unique_sources = Datasource(
	        name + ".unique_sources", _process_unique_sources, depends_on=[self.item]
        )

        """
        A `set` of unique sources in the revision
        """
		
        self.complete_translations = Datasource(
	        name + ".complete_translations", _process_complete_translations, depends_on=[self.item]
        )

        """
        A `list` of completed translations (a pair of completed label and description) in the revision
        """
		
        self.complete_important_translations = Datasource(
	        name + ".complete_important_translations", _process_important_translations, depends_on=[self.item]
        )

        """
        A `float` of the ratio of completed important translations (a pair of completed label and description) in the revision
        """
		
        self.image_quality = Datasource(
	        name + ".image_quality", _process_image_quality, depends_on=[self.item]
        )

        """
        A `float` of the image megapixels in the revision
        """
	
	self.all_sources = Datasource(
	        name + ".all_sources", _process_all_sources, depends_on=[self.item]
        )

        """
        A `list` of all sources in the revision
        """
		
        self.all_wikimedia_sources = Datasource(
	        name + ".all_wikimedia_sources", _process_wikimedia_sources, depends_on=[self.item]
        )

        """
        A `list` of all sources which come from Wikimedia projects in the revision
        """
		
        self.all_external_sources = Datasource(
	        name + ".all_external_sources", _process_external_sources, depends_on=[self.item]
        )

        """
        A count of all sources which do not come from Wikimedia projects in the revision
        """
	
        if hasattr(revision_datasources, "parent") and \
           hasattr(revision_datasources.parent, "text"):
            self.parent = Revision(
                name + ".parent",
                revision_datasources.parent
            )

            if hasattr(revision_datasources, "diff"):
                self.diff = Diff(name + ".diff", self)


def _process_item_doc(text):
    if text is not None:
        return json.loads(text)
    else:
        return None


def _process_item(item_doc):
    item = pywikibase.ItemPage()
    item.get(content=item_doc or {'aliases': {}})
    return item


def _process_properties(item):
    return item.claims

def _process_claims(item):	
	return set(
		(property, _claim_to_str(claim)) 
		for property in item.claims
		for claim in item.claims[property] 
	)


def _process_aliases(item):
    return item.aliases


def _process_sources(item):
	
	return set(
		(property, _claim_to_str(claim), i) 
		for property in item.claims 
		for claim in item.claims[property] 
		for i, source in enumerate(claim.sources) 
		
	)

def _process_all_sources(item):

	list_sources_in_JSON = []
	
	try:
		for property in item.claims:
			list_of_properties = property
			for claim in item.claims[list_of_properties]:
				list_of_claims = claim
				for i, source in enumerate(list_of_claims.sources):
					for index_list_1, index_list_2 in source.items(): 
						sources_in_JSON = index_list_2[0].toJSON()
						list_sources_in_JSON.append(sources_in_JSON['datavalue']['value'])
		
		return list_sources_in_JSON
	except:
		return 0 #if the revision does not contain any sources, return 0

def _process_wikimedia_sources(item):

	list_sources_in_JSON = []
	list_wikimedia_sources = []
	
	try:
		for property in item.claims:
			list_of_properties = property
			for claim in item.claims[list_of_properties]:
				list_of_claims = claim
				for i, source in enumerate(list_of_claims.sources):
					for index_list_1, index_list_2 in source.items(): 
						sources_in_JSON = index_list_2[0].toJSON()
						list_sources_in_JSON.append(sources_in_JSON['datavalue']['value'])
		
		wdir_path = os.path.dirname(os.path.realpath(__file__)) #get the current working directory path
		csv_path = os.path.join(wdir_path, 'excluded_qids.csv')
		
		for list_sources_in_JSON_content in list_sources_in_JSON: 
			with open(csv_path) as csvfile:
				readCSV = csv.reader(csvfile, delimiter=',')
				for line in readCSV:				
					try:
						if(list_sources_in_JSON_content['numeric-id'] == int(line[0])): #if a source comes from Wikimedia projects and DBpedia (i.e. DBpedia collects data from Wikipedia), append that source to the list
							list_wikimedia_sources.append(list_sources_in_JSON_content)
							break
					except:
						continue
		return list_wikimedia_sources
	except:
		return 0 #if the revision does not contain any wikimedia projects sources, return 0

def _process_external_sources(item):
	try:
		count_all_sources = len(_process_all_sources(item))
		count_wiki_sources = len(_process_wikimedia_sources(item))
		return count_all_sources - count_wiki_sources
	except:
		return 0 #if the revision does not contain any external sources, return 0

def _process_external_sources_ratio(item):
	
	try:
		count_external_sources = len(_process_external_sources(item))
		count_claims_with_sources = len(_process_sources(item))
		return count_external_sources/count_claims_with_sources
	except:
		return 0.0 #if the revision does not contain any sources, return 0
	
def _process_unique_sources(item):
	
	list_sources_in_JSON = []
	result_set = set()
	
	for property in item.claims:
		list_of_properties = property
		for claim in item.claims[list_of_properties]:
			list_of_claims = claim
			for i, source in enumerate(list_of_claims.sources):
				for index_list_1, index_list_2 in source.items(): 
					sources_in_JSON = index_list_2[0].toJSON()
					list_sources_in_JSON.append("property : " + str(sources_in_JSON['property']) + " & value : " + str(sources_in_JSON['datavalue']['value']))
	
	#eliminate duplicates
	for value in list_sources_in_JSON:
		result_set.add(value)
	
	return result_set
	
def _process_qualifiers(item):

	return set(
		(property, _claim_to_str(claim), qualifier) 
		for property in item.claims 
		for claim in item.claims[property]
		for qualifier in claim.qualifiers
	)



def _process_badges(item):
    return item.badges


def _process_labels(item):
    return item.labels


def _process_sitelinks(item):
	return item.sitelinks


def _process_descriptions(item):
    return item.descriptions

def _process_complete_translations(item):
	item_labels_dict = item.labels
	item_desc_dict = item.descriptions
	combined_dict = {}
	result_set = []
	
	#merging item label dictionary and item description dictionary
	for key in (item_labels_dict.keys() | item_desc_dict.keys()):
		if key in item_labels_dict: combined_dict.setdefault(key, []).append(item_labels_dict[key])
		if key in item_desc_dict: combined_dict.setdefault(key, []).append(item_desc_dict[key])
	
	#if a language consists of both item label and item description exist, add the language into result_set
	for value in combined_dict.items():
		if(len(value[1]) == 2): 
			result_set.append(value[0])
			
	return result_set

def _process_important_translations(item):
	item_labels_dict = item.labels
	item_desc_dict = item.descriptions
	combined_dict = {}
	result_set = []
	
	#merging item label dictionary and item description dictionary
	for key in (item_labels_dict.keys() | item_desc_dict.keys()):
		if key in item_labels_dict: combined_dict.setdefault(key, []).append(item_labels_dict[key])
		if key in item_desc_dict: combined_dict.setdefault(key, []).append(item_desc_dict[key])
	
	#if an important language consists of both item label and item description exist, add the language into result_set
	for value in combined_dict.items():
		if((len(value[1]) == 2) and (value[0] == 'en' or value[0] == 'de' or value[0] == 'ar' or value[0] == 'zh' or value[0] == 'es' or value[0] == 'pt' or value[0] == 'ru' or value[0] == 'fr')): 
			result_set.append(value[0])
            
	return len(result_set)/8

def _process_image_quality(item):
	
	image_filename = ''
	claims = list(set(
		(property, _claim_to_str(claim)) 
		for property in item.claims
		for claim in item.claims[property]) 
	)
	
	try:
		#find the image filename in P18 (image)
		for x in claims:
			if(x[0] ==  'P18'):
				image_filename = x[1]
				break
		
		image_filename = image_filename.replace(' ', '_').strip()

		#access the Commons API, retrieve the JSON response		
		params = {'action': 'query', 'titles': 'Image:'+ image_filename, 'prop': 'imageinfo', 'iiprop': 'dimensions', 'iimetadataversion': 'latest','format': 'json'}
		url = "https://commons.wikimedia.org/w/api.php?{}".format(urlencode(params))
		url_request = urllib.request.urlopen(url)
		data = url_request.read()
		json_result = json.loads(data.decode("utf-8"))

		#get the image weight and height from the JSON result
		list_json_image_values = list(json_result['query']['pages'].values())
		image_width = list_json_image_values[0]['imageinfo'][0]['width']
		image_height = list_json_image_values[0]['imageinfo'][0]['height']

		return (image_width*image_height)/1000000
		
	except (KeyboardInterrupt, SystemExit):
		raise
	except:
		return 0.0 #if the revision does not have an image, return 0
	
def _claim_to_str(claim):
    if isinstance(claim.target, pywikibase.ItemPage):
        return str(claim.target.id)
    elif isinstance(claim.target, pywikibase.WbTime):
        return claim.target.toTimestr()
    elif isinstance(claim.target, pywikibase.WbQuantity):
        return repr(claim.target)
    else:
        return str(claim.target)

