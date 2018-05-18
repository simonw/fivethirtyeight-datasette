import glob
import markdown
import json
import os


def run():
    tables = {}
    metadata = {
        'title': 'Five Thirty Eight',
        'license': 'CC Attribution 4.0 License',
        'license_url': 'http://creativecommons.org/licenses/by/4.0/',
        'source': 'fivethirtyeight/data on GitHub',
        'source_url': 'https://github.com/fivethirtyeight/data',
        'databases': {
            'fivethirtyeight': {
                'tables': tables
            }
        }
    }
    for filepath in glob.glob('data/*/README.md'):
        filepath = filepath[len('data/'):]
        topdir = filepath.split('/')[0]
        # Render markdown to HTML
        markdown_txt = open(os.path.join('data', filepath)).read()
        # If first line is an h1, extract that into title
        title = None
        lines = markdown_txt.split('\n')
        if lines[0].startswith('# '):
            title = lines[0].lstrip('#').strip()
            markdown_txt = '\n'.join(lines[1:]).strip()
        html = markdown.markdown(
            markdown_txt,
            extensions=['markdown.extensions.tables']
        )
        # This folder contains data -> This TABLE ...
        html = html.replace(
            'This folder contains',
            'This table contains'
        )
        # Use this as the description_html for any CSVs
        for csv_filepath in glob.glob('data/{}/*.csv'.format(topdir)):
            table = csv_filepath.split('.')[0].split('data/')[1]
            tables[table] = {
                'description_html': html,
            }
            if title:
                tables[table]['title'] = '{}: {}'.format(
                    title, csv_filepath.split('/')[-1]
                )
    open('metadata.json', 'w').write(json.dumps(metadata, indent=4))


if __name__ == "__main__":
    run()
