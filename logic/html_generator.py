from airium import Airium
import time
import webbrowser
import os
from model import result_popo as rp
from threading import Thread


class HtmlGenerator:

    def __init__(self, result: list):
        #thread = Thread(target=)
        self.generate(result)

    def to_html(self, json_results: list):
        airium = Airium()
        html: str = ''
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
                        print(a.given)
                        for i in range(len(m_given)):
                            if i == len(m_given) - 1:
                                given += '{}'.format(m_given[i][0])
                            else:
                                given += '{}. '.format(m_given[i][0])

                        _author = '{}, {}. '.format(a.family, given if a.given is not None else '')
                        if author_len > 1:
                            if index == author_len - 2:
                                _author = _author.rstrip() + ', & '
                            elif index < (author_len - 2):
                                _author = _author.rstrip() + ', '
                            else:
                                _author = _author.rstrip()
                        author += _author

                    web_url = json_result.url
                    if web_url is not None:
                        web_url = '<a href={}>{}</a>'.format(web_url, web_url)
                    with airium.p(id="id23409231", klass='main_header'):
                        airium('{}. {} {}. ({}). <em>{}</em>. {}'.format(
                            str(number),
                            author if author is not None else '',
                            json_result.title,
                            json_result.issued.year,
                            json_result.title,
                            web_url))
                    index += 1
                html += str(airium)  # casting to string extracts the value

        # or directly to UTF-8 encoded bytes:
        html_bytes = bytes(airium)  # casting to bytes is airium shortcut to str(airium).encode('utf-8')

        return html

    def quicksort(self, unsorted_keys: list):

        if len(unsorted_keys) < 1:
            return []
        else:
            pivot = unsorted_keys[0]
            lesser = self.quicksort([x for x in unsorted_keys[1:] if x < pivot])
            greater = self.quicksort([x for x in unsorted_keys[1:] if x >= pivot])
            return lesser + [pivot] + greater

    def generate(self, json_results: list):
        final_res = list()
        unsorted_result_dict = {}
        unsorted_keys =[]
        for result in json_results:
            unsorted_result_dict[result.get_sort_key()] = result
            unsorted_keys.append(result.get_sort_key())

        for sorted_key in self.quicksort(unsorted_keys):
            final_res.append(unsorted_result_dict[sorted_key])

        html = self.to_html(final_res)

        filename = 'reference_{}.html'.format(str(round(time.time() * 1000)))
        file = open(filename, 'w')
        file.write(html)
        file.close()
        filepath = '{}/{}'.format(os.getcwd(), filename)
        print(filepath)
        webbrowser.open('file://' + filepath)

    def get_html(self, i: int, result: str, htmls):
        if i < len(htmls):
            print(i, len(htmls))
            result += '<p {}'.format(htmls[i])
            self.get_html(i + 1, result, htmls)
        return result
