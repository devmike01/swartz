from airium import Airium
import time
import webbrowser
import os
from model import result_popo as rp


class HtmlGenerator:
    airium = Airium()

    def __init__(self, result: list):
        self.generate(result)
        """
        <p>Department of the Prime Minister and Cabinet.
         (2017). <em>Understanding the needs of Aboriginal 
         and Torres Strait Islander women and girls:
          A joint project with the Australian Human Rights Commission</em>.
           Australian Government. https://pmc.gov.au/sites/default/files/publications/factsheet-supporting-indigenous-women-girls.pdf</p>
        """

    def to_html(self, json_results: list):
        airium = self.airium
        html: str = ''
        index = 0
        airium('<!DOCTYPE html>')
        with airium.html(lang="pl"):
            with airium.head():
                airium.meta(charset="utf-8")
                airium.title(_t='{} Reference'.format("json_result.title"))

            with airium.body():
                number = 0
                for json in json_results:
                    number += 1
                    json_result: rp.Result = json
                    author = ''
                    author_len = len(json_result.authors)
                    index = -1
                    # Trying to follow the APA 7 author\'s name guidelines
                    for a in json_result.authors:
                        index += 1
                        given = ''
                        m_given = a.given.split(' ')
                        for i in range(len(m_given)):
                            if i == len(m_given)-1:
                                given += '{} '.format(m_given[i])
                            else:
                                given += '{}. '.format(m_given[i])

                        _author = '{}, {}. '.format(a.family,   given if a.given is not None else '')
                        if author_len > 1:
                            if index == author_len-2:
                                _author = _author.rstrip() + ', & '
                            elif index < author_len:
                                _author = _author.rstrip() + ', '
                            else:
                                _author = _author.rstrip()
                        author += _author

                    with airium.p(id="id23409231", klass='main_header'):
                        airium('{}. {} {}. ({}). <em>{}</em>. {}'.format(
                            str(number),
                            author if author is not None else '',
                            json_result.title,
                            json_result.issued.year,
                            json_result.title,
                            json_result.url))
                    index += 1
                html += str(airium)  # casting to string extracts the value

        # or directly to UTF-8 encoded bytes:
        html_bytes = bytes(airium)  # casting to bytes is airium shortcut to str(airium).encode('utf-8')
        return html

    def generate(self, json_results: list):
        html = self.to_html(json_results)
        filename = 'reference_{}.html'.format(str(round(time.time() * 1000)))
        file = open(filename, 'w')
        file.write(html)
        file.close()
        filepath = '{}/{}'.format(os.getcwd(), filename)
        print(filepath)
        webbrowser.open('file://' + filepath)
