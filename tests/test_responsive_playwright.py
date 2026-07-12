"""Teste Playwright opcional: execute com pytest após instalar browsers."""
import os
try:
 import pytest
except ImportError:
 pytest=None
if pytest:
 URL=os.getenv('PROSPECTOR_TEST_URL')
 pytestmark=pytest.mark.skipif(not URL, reason='defina PROSPECTOR_TEST_URL')
 @pytest.mark.parametrize('width',[360,375,768,1024,1280,1440])
 def test_no_horizontal_overflow(page,width):
  page.set_viewport_size({'width':width,'height':900}); page.goto(URL); assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
