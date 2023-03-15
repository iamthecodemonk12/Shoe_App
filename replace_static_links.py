# replace links to point to a static django url
import bs4
import os
import shutil

def external_link(url):
    return url.startswith('http://') or url.startswith('https://')


def static_url(attr):
    return "{{% static 'NiceAdmin/{}' %}}".format(attr)


class Replace:
    def __init__(self, tag, attr):
        self.tag, self.attr = tag, attr


replacements = [
    Replace('script', 'src'),
    Replace('link', 'href'),
    Replace('img', 'src'), Replace('a', 'href'),]


def start(fileText):
    soup = bs4.BeautifulSoup(fileText, 'html.parser')
    for replace in replacements:
        for tag in soup.findAll(replace.tag):
            formertag_attr = str(tag.get(replace.attr))
            if (not external_link(formertag_attr)) and formertag_attr.strip() and (not formertag.startswith('#')) and (not formertag.startswith('{%')):
                tag[replace.attr] = static_url(formertag_attr)         # replacement!
                print(tag)
    return soup


def makecopy(file):
    if os.path.exists(file) and os.path.isfile(file):
        dir, fname = os.path.split(file)
        f, ext = os.path.splitext(fname)
        fname = '%s-newcopy%s'%(f, ext)
        path = os.path.join(dir, fname)
        if os.exists(path):
            return path
        return shutil.copy(file, path)
    #print(file, 'does not exists')

    
f = r"C:\Users\williams\Documents\uncle andrew\SHOEAPP\customadmin\templates\customadmin\index.html"

def getText():
    with open(f) as x:
        htmlText = x.read()
    return htmlText


def main():
    global text
    text = getText()
    soup = start(text)

    # save copy
    makecopy(f)
    with open(f, 'w') as opened:
        opened.write(str(soup))
    
#main()
