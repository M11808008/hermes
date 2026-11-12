import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('builder', Path(__file__).with_name('build-knowledge-base.py'))
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

class LinkifyTests(unittest.TestCase):
    def test_markdown_chinese_suffix(self):
        self.assertEqual(builder.linkify('[固定版本](https://example.com/index.html)以點擊'), '<a href="https://example.com/index.html" target="_blank" rel="noopener">固定版本</a>以點擊')
    def test_balanced_parentheses(self):
        self.assertIn('href="https://en.wikipedia.org/wiki/Foo_(bar)"', builder.linkify('https://en.wikipedia.org/wiki/Foo_(bar)。'))
        self.assertIn('href="https://example.com/(a(b))"', builder.linkify('[x](https://example.com/(a(b)))中文'))
    def test_bare_punctuation_and_chinese(self):
        self.assertEqual(builder.linkify('（https://example.com/x）中文'), '（<a href="https://example.com/x" target="_blank" rel="noopener">https://example.com/x</a>）中文')
        self.assertTrue(builder.linkify('https://example.com/a?q=x&v=2,').endswith('</a>,'))
    def test_escaping_and_unicode_explicit(self):
        out = builder.linkify('[中文](https://example.com/中文?a=1&b=2) <script>')
        self.assertIn('href="https://example.com/中文?a=1&amp;b=2"', out)
        self.assertTrue(out.endswith('&lt;script&gt;'))
        self.assertIn('href="https://example.com/[中文]"', builder.linkify('[食記](https://example.com/[中文])'))
    def test_list_and_paragraph(self):
        self.assertIn('>標題</a>後文', builder.mdhtml('- [標題](https://example.com/)後文'))
        self.assertIn('>標題</a>後文', builder.mdhtml('[標題](https://example.com/)後文'))

if __name__ == '__main__': unittest.main()
