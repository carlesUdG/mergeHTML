import base64
import io
import sys
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
    else:
        fileName = input('Enter the name of the html file\n')

    html_doc = open(fileName, "r")
    soup = BeautifulSoup(html_doc, 'html.parser')
    html_doc.close()

    for link in soup.findAll('link'):
        cssFile = open(link.get('href'), "r")
        cssContent = """<style type="text/css">""" + cssFile.read() + """</style>"""
        cssSoup = BeautifulSoup(cssContent, 'html.parser')
        cssFile.close()
        link.replace_with(cssSoup)

    for script in soup.findAll('script'):
        if script.get('src') != None:
            jsFile = open(script.get('src'), "r")
            jsContent = """<script type="text/javascript">""" + jsFile.read() + """</script>"""
            jsSoup = BeautifulSoup(jsContent, 'html.parser')
            jsFile.close()
            script.replace_with(jsSoup)

    for img in soup.findAll('img'):
        if img.get('src') != None:
            image = Image.open(img.get('src'))
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            buffer.seek(0)

            data_uri = base64.b64encode(buffer.read()).decode('ascii')
            imgContent = '<img src="data:image/png;base64,{0}">'.format(data_uri)
            imgSoup = BeautifulSoup(imgContent, 'html.parser')
            img.replace_with(imgSoup)

f = open("out.html","w+")
f.write(soup.prettify())