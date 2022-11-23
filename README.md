# Scraper

This is a small scraper, aimed at providing an offline copy of a website, that looks at the provided sitemaps and crawls the individual pages in the sitemap, instead of trying to figure out what needs to be crawled next by inspecting the html.

Output is saved by default in the /output directory, where it tries to mimic the same structure as the sitemaps that it parsed.

To preserve the same URL structure as the site that's crawled, /some-page/index.html is created for each of the pages, with page assets being stored in /some-page/assets.

If you do want to serve this up, as e.g. a failover site, ensure that your webserver serves up index.html in a directory by default.
For apache, this would be:

```
DirectoryIndex index.html
```

It's been tested with a Webflow website.

## To get started

```
cp .env.example .env
```

Change the list of sitemaps to crawl by setting SITEMAP_URLS in .env

```
make up
make in
python go.py
```

Crawled pages should be available in the /output directory.

You should be able to view the site by going to:

```
http://localhost
```
