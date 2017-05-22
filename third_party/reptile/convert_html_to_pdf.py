#!/usr/bin/python
# -*-coding:utf-8-*-

"""
Copyright (c) 2017 CGRnDStudio.

Convert www.liaoxuefeng.com to pdf file
Author: andy
WeChat: CGRnDStudio
E-mail: andyvfxtd@gmail.com
Last edited: May 2017
"""

import os
import re
import requests
import pdfkit

from bs4 import BeautifulSoup
from urlparse import urlparse

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""


def response(url):
    """
    requests url
    :param url: web page
    :return: web data
    """
    return requests.get(url)


def parse_menu(res_, main_url):
    """
    yield url list
    :param res_: main web page requests
    :param main_url: main web page
    :return: None
    """
    soup = BeautifulSoup(res_.content, "html.parser")
    menu = soup.find_all(class_="uk-nav uk-nav-side")[1]

    for li in menu.find_all("li"):
        url = li.a.get("href")
        print url
        if not url.startswith("http"):
            url = "".join([main_url, url])
        yield url


def parse_body(res_, main_url):
    """
    analyze url body data
    :param res_: web page requests
    :param main_url: main web page
    :return: html data
    """
    soup = BeautifulSoup(res_.content, "html.parser")
    body = soup.find_all(class_="x-wiki-content")[0]
    title = soup.find("h4").get_text()
    center_tag = soup.new_tag("center")
    title_tag = soup.new_tag("h1")
    title_tag.string = title
    center_tag.insert(1, title_tag)
    body.insert(1, center_tag)

    html_ = str(body)

    pattern = "(<img .*?src=\")(.*?)(\")"

    def func(m):
        if not m.group(3).startswith("http"):
            return "".join([m.group(1), main_url, m.group(2), m.group(3)])
        else:
            return "".join([m.group(1), m.group(2), m.group(3)])
    html_ = re.compile(pattern).sub(func, html_)
    html_ = html_template.format(content=html_)
    # html_ = html_.encode("utf-8")
    return html_


def domain(url):
    """
    http://www.liaoxuefeng.com
    :param url: main web page
    :return: address
    """
    return "{uri.scheme}://{uri.netloc}".format(uri=urlparse(url))

if __name__ == "__main__":
    name = "test"
    start_url = "http://www.liaoxuefeng.com/wiki/001434446689867b27157e896e74d51a89c25cc8b43bdb3000"
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'outline-depth': 10,
    }
    print urlparse(start_url)
    print domain(start_url)
    index_url = domain(start_url)
    # res = response(start_url)
    html_list = []
    for index, url_ in enumerate(parse_menu(response(start_url), index_url)):
        print index, url_
        html = parse_body(response(url_), index_url)
        # print html
        file_name = ".".join([str(index), "html"])
        if not os.path.isfile(file_name):
            with open(file_name, "wb") as fid:
                fid.write(html)
        html_list.append(file_name)
    print html_list
    pdfkit.from_file(html_list, name + ".pdf", options=options)
    for html in html_list:
        os.remove(html)
