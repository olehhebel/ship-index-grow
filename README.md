# Ship Index Grow

AI-native product launch school.

Production: https://shipindexgrow.top/

## Hosting and publication

Production hosting is GitHub Pages, served at the custom domain in `CNAME`.
Vercel is no longer used. A Vercel commit status is not proof of production publication.
Develop changes in `main`, then merge them into `github-pages-pilot` to publish.
The `github-pages` environment permits deployments from `github-pages-pilot` only.
Check the **pages build and deployment** workflow for that release commit and verify
the updated content on https://shipindexgrow.top/ before reporting it live.
Keep the existing custom domain and DNS settings unchanged.

The homepage offer lives directly below the headline in `index.html` and `uk.html`,
with shared responsive styles in `styles.css`. Keep both language versions and their
course prices consistent with the existing enrollment form.

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
the latest-posts block on the home pages. Commit the result. After changes reach `github-pages-pilot`, the IndexNow workflow waits until the public sitemap
matches the release before notifying Bing and other IndexNow search engines. A matching sitemap
does not prove every page has finished deploying, and IndexNow does not guarantee indexing.
