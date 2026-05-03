# CEJBSBDSL
*We were so pre-occupied with whether or not we could, we never stopped to think if we should.*

CEJBSBDSL (Pronounced "See-Jizz-Bull") is a mistake. 
May the Code Efficent JSON-Based Story-Boarding Domain Specific language serve as a harrowing example for any aspiring programmer. Never make new infrastructure when it was made *for* you and can meet your needs.
We *already* had a lightweight scripting language to write our game in; Python! We should have just used Python.
Instead, we chose to invent a DSL specifically for [The Space Trail](https://github.com/TheSpaceTrail/TheSpaceTrail), we spent so much time making this language, all encompasing, expandable and flexible when we could have made a much better and content-rich game using a few functions in Python.

To learn to use the language, or to force an AI to use it read [CEJBSBDSL.spec.md](CEJBSBDSL.spec.md). You are free to make your own projects in it! Although I would not wish that on my worst enemy. I would strongly suggest reading the specification even if you are not planning to use it, just to know the pain and effort put into The Space Trail.

If you want to look at some beatiful syntax sugar take a look at our modified implementation for our game [here](https://github.com/TheSpaceTrail/TheSpaceTrail/blob/main/src_tst/storyline.json) (*because our language is so deeply terrible, we had to write a modified shim for the parser so that we could add functionality, so you need to run it through the parser file, although, in theory, it should be entirely possible to implement what we did using the base language and ANSI escape codes).

The entire CEJBSBDSL language can be accessed in [CEJBSBDSL.py](/CEJBSBDSL.py).
```
python CEJBSBDSL.py --file script.json
```

Example:

`demo.json`
```json
{
    "init": [
        "Hello, World!"
    ]
}
```

```md
> python CEJBSBDSL.py --file demo.json 
Hello, World!
```

Help:
```md
> python .\CEJBSBDSL.py --help
usage: CEJBSBDSL.py [-h] [-f FILE] [-e ENTRY_POINT] [-s SEED] [-v] [-dw] [-de]

options:
  -h, --help            show this help message and exit
  -f, --file FILE       path to script
  -e, --entry-point ENTRY_POINT
                        program entry point (default: "init")
  -s, --seed SEED       random seed (default: 42, "random" for random)
  -v, --version         show program's version number and exit
  -dw, --disable-warnings
                        disables warnings
  -de, --disable-errors
                        disables errors and exits quietly and successfully
```
