import xml.etree.ElementTree
import pytest
from flask import Response

def test_int_site_mapped_urls(client):
    text = get_sitemap_text(client)
    x = xml.etree.ElementTree.fromstring(text)
    urls = [
        href.text.strip().replace('http://127.0.0.1:5006', '').replace('http://localhost', '')
        for href in list(x.findall('url/loc'))
    ]
    urls = [
        u if u else '/'
        for u in urls
    ]
    # Arbitrarily selected dive as thy're not currenlty in the site map
    urls.append('/mission60/glider637/dive12')
    print('Testing {} urls from sitemap...'.format(len(urls)), flush=True)
    # Hit a single representative page each of mission, glider adn dive. Will catch 99 % of b0rks.
    has_tested_gliders = False
    has_tested_missions = False
    for url in urls:
        if '/gliders/' in url and has_tested_gliders:
            continue
        if '/gliders/' in url:
            has_tested_gliders = True
        if '/mission' in url and has_tested_missions and 'dive' not in url:
            continue
        if '/mission' in url:
            has_tested_missions = True
        print('Testing url at ' + url)
        resp: Response = client.get(url)
        assert resp.status_code == 200


def get_sitemap_text(client):
    # <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    #     <url>
    #         <loc>http://talkpython.fm/episodes/show/37/python-cybersecurity-and-penetration-testing</loc>
    #         <lastmod>2015-12-08</lastmod>
    #         <changefreq>weekly</changefreq>
    #         <priority>1.0</priority>
    #     </url>
    #     <url>
    #         ...
    #     </url>
    res: Response = client.get("/sitemap.xml")
    text = res.data.decode("utf-8")
    text = text.replace('xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"', '')
    return text
