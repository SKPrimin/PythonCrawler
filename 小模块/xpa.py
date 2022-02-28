from lxml import etree

if __name__ == '__main__':
    parser = etree.HTMLParser(encoding="utf-8")
    tree = etree.parse('关雎.html',parser=parser)
    r = tree.xpath('/html/body/div[2]/div[1]/div[3]/div/div[2]/h2/span/text()')
    print(r)