# Bruno Vinícius — Interior Design

Static multilingual one-page site + blog, generated via Python.

## Languages

EN  `/`       (default)
ES  `/es/`  
IT  `/it/`  
FR  `/fr/`  
PT  `/pt/`

## Build

```bash
python build.py
```

Output: `site/` (ready to deploy — drag to any static host).

## Structure

```
src/
├── assets/
│   ├── css/main.css
│   ├── js/main.js
│   ├── img/           (photos from Pexels via image-search MCP)
│   └── data/images.json (attributions)
├── scripts/
│   ├── content_site.py  (onepage copy, 5 langs)
│   ├── content_blog.py  (English blog articles)
│   ├── content_blog_es.py / it / fr / pt
│   └── fetch_images.py  (download + optimize)
site/                    **← output**
```

## To-do / setup notes

- Photos were fetched via `image-search-mcp` from [Pexels](https://pexels.com) and [Unsplash](https://unsplash.com). Attributions in `src/assets/data/images.json`.
- Bio, credentials, and testimonials should be updated with real data when available.
- Contact uses mailto, change to e.g. [Formspree](https://formspree.io) or [Netlify Forms](https://docs.netlify.com/forms/setup/) for a proper backend.
- To automatically fetch the latest Indiegogo design-category launches for the "Novidades" article, run `src/scripts/indiegogo_novidades.py` and replace the static `novidades.json` with fresh data.
- Backup URL structure for future CMS: `/en/ /es/ ...` already present.

## Credits

- SEO strategy: [loopexdigital.com/industries/seo-for-interior-design-companies](https://www.loopexdigital.com/industries/seo-for-interior-design-companies)
- Design inspiration: [flos.com](https://flos.com)  
- Image search: MCP image-search-mcp  
- Brand kit: MCP brandkit-mcp  
- Icons: inline SVG

Made with ❖ for Bruno.