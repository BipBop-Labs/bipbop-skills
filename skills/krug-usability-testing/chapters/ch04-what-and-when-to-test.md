# Chapter 4: What do you test, and when do you test it?

## Core Idea
The hardest part is starting early enough. You can test every artifact, from a sketch on a napkin to a competitor's live site. **Early testing is cheaper and catches problems that later can't be fixed at all**, so start before it feels reasonable.

## Frameworks Introduced
- **Maxim: "Start earlier than you think makes sense."** The paradox: *the worse shape it's in, the less you want to show it, and the more you gain if you do.*
- **Three excuses for waiting, and the rebuttals**:
  - *"We don't have enough done yet."* It's never too early. Start with your first rough sketches.
  - *"It's too rough."* Users often comment *more* candidly on rough work because they know it can still change.
  - *"Why show something we'll change anyway?"* You'll hit known problems, but you're there **for the surprises**: what you didn't think of because you're too close to it, or because you don't understand your users as well as you think.
- **What to test at each stage** (artifact → how → what you learn):

| Artifact | How to test | What you get |
|---|---|---|
| **Your existing site** (before a redesign) | Full process (ch05–09) | What you're doing wrong, so the redesign avoids it. Fix the worst problems now, since users shouldn't suffer until the redesign ships. You also learn how people actually use it |
| **Other people's sites** (competitors, same content, same users, or features you're considering) | Full process. Give your key tasks, maybe the same task on 2–3 competitor sites. **The debrief becomes a lunch discussion of what worked, what didn't, and what lessons apply**, not a fix list | Learn from a "full-scale working prototype someone built and left lying around". Hooks marketing and management. Low-pressure first round because nobody's ego is at stake |
| **Sketch on a napkin** (concept drawings) | **Napkin test**: under 5 minutes, with almost anyone, anywhere users gather (see protocol below) | Whether people "get" the concept, before you build anything |
| **Wireframes** | Navigation tasks: "How would you find ___?" "What would you expect to see if you clicked this?" Usually combined with other tests in the same session | Whether your **categorization and naming** make sense. You may discover you've organized by your org chart and users don't think that way |
| **Page designs / comps** | Walk them through the comps, starting at the Home page, asking for a narrative of each | Whether the visual design introduced usability issues. Can people tell how each page "works"? |
| **Working prototypes onward** | Full process | Everything else |

- **The napkin test protocol**:
  1. Approach almost anyone.
  2. "Can you do me a favor? Take a look at this?"
  3. Hand them the sketch.
  4. "**Can you tell me what you make of this? What do you think this is supposed to be?**"
     - You're *not* asking for opinion ("Do you like it?") or feedback ("What do you think of it?"). You're asking them to **figure out what the thing is**.
  5. Listen. Optionally probe ("What do you think 'Incentives' might mean?").
  - If they describe what you intended, get a bigger napkin and keep drawing. Usually something doesn't make sense to them, and you've learned it before building anything.

## Key Concepts
- **Sketch on a napkin**: any early concept drawing, sometimes literally a napkin.
- **Wireframe**: a page schematic showing content placement, relative prominence, and navigation.
- **Comp**: the visual treatment of a unique page or a template.
- **Narrative**: the participant describes what they make of a page (see the Home page tour, ch08).

## Mental Models
- **Other people's products are free prototypes.** Someone already built a working version of an approach to your problem. Test it before designing your own.
- **Wireframes test information architecture; comps test visual clarity.** Match the question to the artifact.
- **The concept test asks "what is this?", never "do you like it?"** Understanding is observable. Liking is opinion.

## Anti-patterns
- **Waiting until it works.** Waiting to test until launch is the most common practice and the worst one.
- **Asking for opinions on a sketch.** That gets you taste instead of comprehension.
- **Organizing by org chart.** Wireframe tests expose it quickly.
- **Holding a "which competitor problems do we fix" debrief.** You can't fix their site, so extract the lessons instead.

## Worked Example: Krug's own book title
For years Krug planned to call this book *Krug's Field Guide to Users*, designed like a bird-watching field guide with the same size, shape, and look. He loved it and kept a mock cover on his wall. Then he napkin-tested it. The results were unanimous: everyone "got" the bird-guide idea and thought it was neat, **and everyone assumed it was a book about the different kinds of Web users.** When told it was about usability testing, they all went "Oh…" They weren't upset; the cover just set the wrong expectation. "I couldn't see it because I was too close to it. I knew how it was supposed to work." Five minutes per person caught a positioning failure before any production cost.

## Key Takeaways
1. Start testing before you think you're ready, with sketches or competitors' products.
2. Before a redesign, test the current product and fix its worst problems now.
3. Test competitors early. It's cheap learning, and it recruits management as observers.
4. Napkin tests ask "what is this supposed to be?", never "do you like it?"
5. Use wireframes to test navigation and naming, and comps to test whether pages read correctly.
6. You're testing for the surprises, not the known issues.

## Connects To
- **Ch 5–9**: the full process referenced by most rows in the table.
- **Ch 8**: the Home page tour is the napkin test applied to a live page.
- **Ch 9**: testing competitors first spares the team's egos.
- **Ch 12**: "getting off on the wrong foot" is what concept and Home page tests catch.
