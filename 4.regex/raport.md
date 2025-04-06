# Topic: Regular expressions

### Course: Formal Languages & Finite Automata
### Author: Cretu Dumitru and kudos to the Vasile Drumea with Irina Cojuhari

### Made by George Rabus

----

# Objectives:

1. Write and cover what regular expressions are, what they are used for;

2. Below you will find 3 complex regular expressions per each variant. Take a variant depending on your number in the list of students and do the following:

    a. Write a code that will generate valid combinations of symbols conform given regular expressions (examples will be shown). Be careful that idea is to interpret the given regular expressions dinamycally, not to hardcode the way it will generate valid strings. You give a set of regexes as input and get valid word as an output

    b. In case you have an example, where symbol may be written undefined number of times, take a limit of 5 times (to evade generation of extremely long combinations);

    c. **Bonus point**: write a function that will show sequence of processing regular expression (like, what you do first, second and so on)

Write a good report covering all performed actions and faced difficulties.

## Variant 3:

```
O(P|Q|R)+2(3|4)
A*B(C|D|E)F(G|H|i)^2
J+K(L|u|N)*O?(P|Q)^3
```

Examples of what must be generated:

{OPP23, OQQQQ24, ...}
{AAABCFGG, AAAAAABDFHH, ...}
{JJKLOPPP, JKNQQQ, ...}

# Evaluation:

1. Project must be located in a *public* repository on a GitHub;

2. Explain performed work in details and cover how the code works;

3. Present your work to see the program works and to ask questions if necessary;

4. **Upload link to the ELSE** (I understand that you're giving access mostly to the same repo as previous labs, but it eases my experience to verify all your labs and assignment on ELSE is closed - all win);

5. Deadline is 30-th March, 2025, 23:59

6. You have to present the lab and in case if you don't - max grade decreases by 1 per week of delay.
