from ..crawler.css_and_xpaths import xpath_paths, css_paths

def test_xpaths():
    assert 'titles' and 'links' in xpath_paths.keys()

