# Ship Index Grow

AI-native product launch school.

Production: https://shipindexgrow.top/

## Blog

Articles live in `tools/blog/posts/en/` and `tools/blog/posts/uk/`. Each file starts with a JSON
metadata comment (title, SEO title, description, dates, FAQ, and `translation`, the slug of the
other-language version for hreflang), followed by the article HTML. Put `<!--cta-->` where the
"Join the course" block should appear.

After adding or editing a post, run:

```sh
python3 tools/blog/build.py
```

It regenerates `blog/`, `blog/uk/`, both RSS feeds, `sitemap.xml` (with hreflang alternates) and
the latest-posts block on the home pages. Commit the result. On push to `main`, the IndexNow
workflow notifies Bing and other IndexNow search engines about every URL in the sitemap.
