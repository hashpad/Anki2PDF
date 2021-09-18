import re
import os
import sys

def bold(text):
    return ('<span style="font-weight: bold; font-size: 20px; padding-bottom: 5px; display: block; border-bottom: 1px solid gray;">{}</span>'.format(text))
def fix_img_srcs(text):
    pattern = re.compile(r"<img src='((.)*)' \/>")
    ret = re.sub(pattern, r"<img src='" + re.escape(os.environ['HOME']) + r"/.local/share/Anki2/User%201/collection.media/\1' \/>", text)
    return ret
def main():
    with open(sys.argv[1], "r") as doc:
        pattern = re.compile(r"^\"(((\n)*((?!\").)*(\n)*)*)\";\"(((\n)*(((?!\").)*)(\n)*)*)\"$", re.MULTILINE | re.DOTALL)
        data = doc.read()
        itera = re.finditer(pattern, data)
        content = ""
        for card in itera:
            div_def = ("<div style='border: 1px solid gray; background-color:#f9f4f4; margin:10px; padding:10;'>")
            front = (fix_img_srcs(bold(card.group(1))) + "<br />")
            back = (fix_img_srcs(card.group(6)) + "<br />")
            end_div = ("</div><br />")
            content+= div_def + front + back + end_div
    with open('/tmp/tmp_anki_html_file.html', "w") as out:
        out.write(content)
    os.system("wkhtmltopdf /tmp/tmp_anki_html_file.html " + sys.argv[2] + " && rm -rf /tmp/tmp_anki_html_file.html")

if __name__ == '__main__':
    main()
