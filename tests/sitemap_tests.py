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
    # Arbitrarily selected dive as they're not in the site map
    print(urls)
    urls.append('/mission60/glider637/dive12')
    print('Testing {} urls from sitemap...'.format(len(urls)), flush=True)
    # Hit a single representative page each of mission, glider adn dive. Will catch 99 % of b0rks.
    has_tested_gliders = False
    has_tested_missions = False
    for url in urls:
        if 'register' in url:
            # Additional test for sign up page that may redirect to login if not accepting new accounts
            print('Testing url at ' + url)
            resp: Response = client.get(url)
            assert resp.status_code == 200 or resp.status_code == 302
            continue
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
    res: Response = client.get("/sitemap.xml")
    text = res.data.decode("utf-8")
    text = text.replace('xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"', '')
    return text
