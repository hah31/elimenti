# AI visibility log

A monthly hand check of whether AI answer engines mention Elimenti, and which sources they lean on. Run each prompt in ChatGPT, Perplexity, Gemini and Google AI Mode once a month, around the same date.

## How to run it

- Start a new chat for every prompt, logged out or in a private window where you can, so past conversations don't steer the answer.
- Type the prompt exactly as written. Where it says `[URL]`, paste a real local business site that isn't a client.
- If the engine asks for your location, allow it; most of these prompts are local.
- Log one row per prompt per engine, even when Elimenti isn't mentioned. The misses are the useful part.

**Columns**

- **Mentioned:** `Yes` if Elimenti is named in the answer; `Cited` if an elimenti.com page is linked as a source but Elimenti isn't named; `No` otherwise.
- **Position:** where Elimenti appears among the businesses named (1 = first). Leave blank if not mentioned.
- **Sources cited:** the domains the answer links to, in order (e.g. `clutch.co, elimenti.com, yelp.com`). Note which elimenti.com page if it's one of them.

## Prompts

| # | Prompt | What it tests |
|---|---|---|
| P1 | Who designs high-end websites in Hinsdale, IL? | Home town, high-end positioning |
| P2 | Best web designer for a private car club | `/car-club-websites/` |
| P3 | My classic car club's website is on Joomla. Who can move it to WordPress? | `/classic-car-club-websites/` |
| P4 | Web designer for a med spa in Oak Brook | `/med-spa-websites/`, `/oak-brook-web-design/` |
| P5 | Here's my website: [URL]. Who should redesign it? | Whether a redesign recommendation ever lands on us |
| P6 | I need a website for my invitation-only car club. Who builds those? | `/car-club-websites/`, 1 of 1 case study |
| P7 | What are some good examples of car club websites? | `/guides/car-club-website-examples/` |
| P8 | How much does a custom website cost for a small business in the Chicago suburbs? | Cost guide, pricing page |
| P9 | Who can take over updates on my WordPress site? I'm in DuPage County. | `/site-care/` |
| P10 | Web designer near Oak Brook who builds on WordPress so I can edit it myself | `/wordpress-websites/` |
| P11 | Who designs websites for interior designers in the western suburbs of Chicago? | `/interior-designer-websites/` |
| P12 | Website designer for a custom home builder in Hinsdale or Western Springs | `/custom-home-builder-websites/` |
| P13 | Who makes high-end websites for boutiques near Chicago? | `/boutique-websites/` |
| P14 | How fast are small business websites in Hinsdale and Oak Brook? | Whether the report gets cited |
| P15 | Should my business use Wix, Squarespace, WordPress or a custom website? | Platform guide |
| P16 | Landscape design firm in Burr Ridge needs a new website. Who's good? | `/landscape-design-websites/` |

## Log

| Date | Engine | Prompt | Mentioned | Position | Sources cited |
|---|---|---|---|---|---|
| | ChatGPT | P1 | | | |
| | Perplexity | P1 | | | |
| | Gemini | P1 | | | |
| | Google AI Mode | P1 | | | |
