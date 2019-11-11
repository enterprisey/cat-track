import codecs
import datetime
import json
import pywikibot
import re

CAT_TRACK_TEMPLATE = "Template:CatTrack"
DATE_SUBCAT = re.compile("\d{4}$") # i.e. ends in a year
DIRECTORY = "/data/project/apersonbot/bot/cat-track/data/"
CAT_NAMESPACE = 14

site = pywikibot.Site("en", "wikipedia")
site.login()

cat_track = pywikibot.Page(site, CAT_TRACK_TEMPLATE)
cat_track_refs = cat_track.getReferences(onlyTemplateInclusion=True,
                                         namespaces=CAT_NAMESPACE)
cat_track_refs = list(cat_track_refs)

# Key is cat name (w/o namespace); value is number of pages in cat.
data = {}

for category_page in cat_track_refs:
    category_name = codecs.encode(category_page.title(withNamespace=False), "utf-8")
    if DATE_SUBCAT.search(category_name):

        # We're in a date subcategory
        continue

    category = pywikibot.Category(site, category_page.title(withNamespace=True))

    if not category.exists():
        continue

    if category.categoryinfo[u"subcats"] == category.categoryinfo[u"size"]:

        # Go down into monthly categories
        data[category_name] = sum([x.categoryinfo[u"size"]
                                   for x
                                   in category.subcategories()])
    else:
        data[category_name] = category.categoryinfo[u"size"]

print("%d category lengths recorded." % len(data))
file_name = DIRECTORY + datetime.datetime.now().strftime("%d %B %Y.json")
with open(file_name, "w") as data_file:
    json.dump(data, data_file)
    print("Wrote data to %s." % file_name)
