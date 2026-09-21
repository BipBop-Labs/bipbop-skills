# Chapter 12: The usual suspects

## Core Idea
The same problems show up in test after test. Two of the most damaging are **users getting off on the wrong foot** (a wrong first impression that snowballs) and **failure to shout** (important things too subtle to notice).

## Frameworks Introduced
- **Getting off on the wrong foot**
  - *The problem*: people start with a misapprehension and head confidently in wrong directions, often not realizing it for a long time. Like people who get lost in cities (Erik Jonsson, *Inner Navigation*), **people who start off lost tend to stay lost.**
  - **The Big Bang Theory of Web Usability**: in the first few seconds on a new page or site, users (1) form an overall, mostly visual impression (professional? reliable? This happens within about 50 ms, per Lindgaard et al. 2006); (2) parse the page into regions and assume what's where; (3) identify the site: what it is, who publishes it, what's there. Those **working assumptions become the Rosetta Stone for everything after.** If they're wrong, users force later evidence to fit, and "the lost get… loster."
  - *How to think about fixing it*: the usual culprit is **a Home page that fails to orient**. Do visitors get the big picture (what this is, how it's organized, what they can find and do) **in a few seconds, with little effort?** Home pages decay as stakeholders add things (**kitchen-sink syndrome**; "I see stakeholders"). **Do a Home page tour in every test session.** "You can never test your Home page too many times." It also lets stakeholders hear strangers say "There's an awful lot here."
- **Failure to shout**
  - *The problem*: designers, especially those trained in print, love subtle distinctions (hairline vs. half-point rules, tiny low-contrast type). Web users move fast on lower-fidelity screens and **almost always miss subtle visual cues.**
  - *How to think about fixing it*: if people must notice something, **make it stand out more than you think necessary, and more than your designer would like.** That doesn't mean ugly. Amazon's two bright buttons are spottable from 50–75 feet, and a navigation system built by usability professionals went unnoticed until its cues were made less subtle. "If you want people to use something you've built, they have to notice it first."

## Key Concepts
- **Big Bang Theory of Web Usability**: first-seconds assumptions govern the rest of the visit.
- **Kitchen-sink syndrome**: the overcrowded, unfocused Home page.
- **Subtle visual distinction**: a cue that looks sophisticated but goes unnoticed.

## Mental Models
- **Orientation is a prerequisite for everything else.** A navigation fix can't help someone who misidentified the site.
- **The Home page still matters in a search-first world.** Visitors who "teleport" into an interior page and don't find what they want bob up to the Home page, then often to About Us, to learn who you are and whether you're credible. The Home page's job is to answer that fast. About Us should open with a plain explanation of who you are and what you do, **not a mission statement**.

## Anti-patterns
- Adding every stakeholder's item to the Home page.
- Distinguishing important controls by hairlines, faint color, or small type.
- Assuming the Home page is irrelevant because traffic enters from search.
- Opening About Us with a mission statement.

## Key Takeaways
1. Watch for wrong first assumptions, which compound silently.
2. Make identity, purpose, and organization obvious within seconds.
3. Run a Home page tour in every session. It's cheap regression testing for orientation.
4. Things that must be noticed need to shout, and they can still look good.
5. Guard the Home page against stakeholder accretion.

## Connects To
- **Ch 4**: napkin tests catch wrong-foot concepts before they're built.
- **Ch 8**: the Home page tour protocol.
- **Ch 11**: "louder" tweaks fix failure to shout, and "take something away" fixes kitchen-sink pages.
