# -*- coding: utf-8 -*-
import re


def add_refs(base_string=""):
    urls = re.findall(r'(https?://[^\s]+)', base_string)
    url_dict = {}
    for url in urls:
        url_dict[url] = "[ref={}]".format(url) + url + "[/ref]"
    final_string = base_string
    for key, value in url_dict.iteritems():
        final_string = final_string.replace(key, value)
    gopher_urls = re.findall(r'gopher://[^\s]+', final_string)
    gopher_url_dict = {}
    for gopher in gopher_urls:
        gopher_url_dict[gopher] = "[ref={}]".format(gopher) + gopher + "[/ref]"
    for key, value in gopher_url_dict.iteritems():
        final_string = final_string.replace(key, value)
    return final_string


