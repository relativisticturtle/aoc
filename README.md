# My AoC-adventures
Repo of my AoC-solutions and related material. (Unfortunately only partially restored 2017 - 2019).

The repository is mainly intended for myself and my own benefit - but made public to demonstrate automation compliance (below).

I'm flattered that you found your way here, though, and you are very much welcome to browse my solutions!

## Automation compliance
This repository has a tool in `aoc/utils.py` for download of inputs. (Main purpose is to reduce number of mouse-clicks and risk of copy&paste-errors, rather than saving ~10 seconds).

Download is triggered by requesting input which is not already cached. Requests are always made from manually started jobs (i.e., *not* scheduled). Even though the tool *should* not incur any more traffic than manually opening the input, it is an automation that needs to comply with [AoC's Rules for Automated Tools](https://www.reddit.com/r/adventofcode/wiki/faqs/automation).

### Statement

> This repo does follow the automation guidelines on the [/r/adventofcode](https://www.reddit.com/r/adventofcode/wiki/faqs/automation) community wiki. Specifically:
>
> Input is downloaded by `aoc.utils._download_input()`,
>
> ... but this function should only be called from `aoc.utils.get_input()` that caches downloaded data and returns *that* in subsequent calls.
>
> Remove the `<year>/input<day>.txt` file to clear the cache.
>
> The User-Agent header in `aoc.utils._download_input()` is set to me since I maintain this tool :)

