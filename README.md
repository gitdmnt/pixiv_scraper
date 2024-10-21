# pixiv-scraper

This scrapes Pixiv posts by tag for each month from January 2021 to December 2024.

```zsh
rye sync
. .venv/bin/activate
python src/pixiv_scraper/__init__.py
```

| file     | desc                                             |
| -------- | ------------------------------------------------ |
| data.csv | total posts for each tag in each specified month |
| name.csv | umamusume names                                  |

