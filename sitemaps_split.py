import os

split_by = 1000
split_by_ask = input('Urls count per file [1000]: ')
if split_by_ask.isdigit():
    split_by = int(split_by_ask)

sitemaps_server_url = 'https://grata.store/files/sitemaps/'
last_mod = '2021-05-15T17:54:48+03:00'
priority = '0.5'
change_freq = 'weekly'


urls = []
for file in os.listdir('sitemaps_read'):
    print(file)
    with open('sitemaps_read/' + file, 'r') as fr:
        for line in fr.readlines():
            if '<loc>' in line:
                urls.append(line)

sitemaps_counter = 0
while True:
    will_brake = False
    if len(urls) > (sitemaps_counter+1)*split_by:
        urls_part = urls[sitemaps_counter*split_by:(sitemaps_counter+1)*split_by]
    else:
        urls_part = urls[sitemaps_counter*split_by:]
        will_brake = True
    with open('sitemaps_done/' + f'sitemap{sitemaps_counter}.xml', 'a') as fw:
        fw.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fw.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for url in urls_part:
            fw.write('\t<url>\n')
            fw.write(f'{url}\n')
            fw.write(f'\t\t<lastmod>{last_mod}</lastmod>\n')
            fw.write(f'\t\t<priority>{priority}</priority>\n')
            fw.write(f'\t\t<changefreq>{change_freq}</changefreq>\n')
            fw.write('\t</url>\n')
        fw.write('</urlset>')
    sitemaps_counter += 1
    if will_brake:
        break

with open('sitemaps_done/' + 'sitemap-all.xml', 'a') as fw:
    fw.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    fw.write('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for c in range(sitemaps_counter):
        fw.write('\t<sitemap>\n')
        fw.write(f'\t\t<loc>{sitemaps_server_url}sitemap{c}.xml</loc>\n')
        fw.write(f'\t\t<lastmod>{last_mod}</lastmod>\n')
        fw.write('\t</sitemap>\n')
    fw.write('</sitemapindex>')
