# CEJBSBDSL 0.0.1 Specification

## File Formatting

- CEJBSBDSL files follow the file extension pattern: `file.json` or `file.cejbsbdsl`
- White space does not matter as long as it constitutes valid JSON

## Syntax & Usage

Adheres to JSON ([ECMA-404](https://ecma-international.org/publications-and-standards/standards/ecma-404/))

Every file acts as a database of named command sequences.

Each sequence is stored as a key in the top-level JSON object.

Every sequence must either terminate or call another sequence.

Every CEJBSBDSL program starts from a command sequence called "the origin", the origin can be specified through the `--entry-point` parameter, although `init` is suggested as the standard entry point.

Arguments for commands can either be literals e.g. `!jump Bucharest` or as variables e.g. `!jump $country`. Arguments that can be both variables as well as literals will be indicated with `@`.

Smallest possible standard CEJBSBDSL program:
```json
{"init":[]}
```

## Commands

### I/O

Not calling a command with `!` automatically prints the contents of the string.

```json
{
    "init": [
        "Hello, World!"
    ]
}
```
```md
> python CEJBSBDSL.py -f script.json
Hello, World!
```

Input is done using `?`.

```md
{
    "init": [
        "What is your name?> ",
        "What is your quest?> ",
        "What is the airspeed velocity of an unladen swallow??> ",
        "# Well, you have to know these things when you're king, you know?"
    ]
}
```
```md
> python CEJBSBDSL.py -f script.json
What is your name? It is Arthur, king of the Britons.
What is your quest? To seek the holy grail.
What is the airspeed velocity of an unladen swallow?> What do you mean? An African or European swallow?
```
The value of the special variable `$output` is now `What do you mean? An African or European swallow?` (see [#special-values](#special-values)).

Note: getting a new input overwrites old inputs, so the value of `$output` was `It is Arthur, king of the Britons.`, then `To seek the holy grail.`, then finally the last value.


### Comments

Start strings with `#`.
```json
{
    "init": [
        "# comment...",
        "Not a comment..."
    ]
}
```
```md
> python CEJBSBDSL.py -f script.json
Not a comment...
```
### Data

#### Special Values

`$output` - Reserved for the output of terminal-input functions. Can be overwritten.


#### Data Commands

`${}` - Prints the value of a variable.
```json
{
    "init": [
        "!modify value + 1337",
        "$value"
    ]
}
```
```md
> python CEJBSBDSL.py -f script.json
1337.0
```

`!store @value-name @value` - Set value-name to value.
```json
{
    "init": [
        "?What is your name?> ",
        "!store name $output",
        "$name"
    ]
}
```
```md
> python CEJBSBDSL.py -f script.json
?What is your name?> Turing
Turing
```

`!modify @value-name operator @value` - Modify a value by an operator, operators include `+`, `-`, `/`, `//` (floor division), `%` (mod), `**` (pow).

```json
{
    "init": [
        "?Give me an input to double> ",
        "!modify var + $output",
        "!modify var + $output",
        "$var"
    ]
}
```
```md
> python CEJBSBDSL.py -f script.json
Give me an input to double> double
doubledouble
```


### Control Flow

`!jump @sequence` runs a sequence.

```json
{
    "init": [
        "Oi you know CEJBSBDSL init?",
        "!jump Birmingham"
    ],

    "Birmingham": [
        "Lemme get uh, fish and chip, with uh, brown sauce."
    ]
}
```
```md
> python CEJBSBDSL.py -f script.json
Oi you know CEJBSBDSL init?
Lemme get uh, fish and chip, with uh, brown sauce.
```

`!random_hop sequence1 sequence2 ...` - randomly jumps to one of the specified sequences, controlled using `--seed` command.

```json
[
  "!random_hop Wallachia Transylvania",
  "# Randomly hops to either Wallachia or Transylvania"
]
```

`!jump_switch` - Jumps to the contents of a variable, based on a dictionary, the key `\n` corresponds to else.

```json
{
  "init": [
    "?Beep Boop 1 or 0? ",
    "!jump_switch $output",
    {
      "1": "left",
      "0": "right",
      "\n": "else"
    }
  ],

  "left": ["You went left!"],
  "right": ["You went right!"],
  "else": ["Where did you go?"]
}
```
```md
> python CEJBSBDSL.py -f script.json
Beep Boop 1 or 0? 1
You went left!

> python CEJBSBDSL.py -f script.json
Beep Boop 1 or 0? North
Where did you go?
```

`!end` - Ends the program.

`!sleep @seconds` - Sleeps for specified time in seconds, floats allowed.

`!if @value1 operator @value2` - If statement. Comparators `==`, `=>`, `>`, `<`, `=<`.

```json
{
    "init": [
        "?Give me an input> ",
        "!if 5 <= $output",
        [
        "Output is greater than or equal to 5!"
        ],
        [
        "Output is less than 5!"
        ]
    ]
}
```
```md
> python CEJBSBDSL.py -f script.json
Give me an input> 5
Output is greater than or equal to 5!
```

# Have a nice day!
