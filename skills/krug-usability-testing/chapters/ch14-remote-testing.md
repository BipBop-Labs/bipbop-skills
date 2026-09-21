# Chapter 14: Teleportation made easy

## Core Idea
Remote testing (screen sharing plus voice) gives **about 80% of the benefit of in-person testing for about 70% of the effort**. It widens recruiting and eases scheduling. Unmoderated services are even faster and cheaper, but you can't probe. **Do in-person tests first.**

## Frameworks Introduced
- **Moderated remote testing**: the same process (tasks, scenarios, script, think-aloud, probing, observers), with you connected electronically instead of sitting alongside.
  - **Why**: easier recruiting (anyone with a fast connection, which helps for specific profiles); no travel (an hour of the participant's time instead of two); flexible hours (run it at 11 pm if that's when they're free); and **roughly the same kinds and amounts of problems found**.
  - **What you lose (the 20%)**: the in-person richness; it's harder to know what they're thinking; misunderstandings through the tech layer, as with phone vs. face-to-face, so you spend more time clarifying; **less control** over interruptions and walk-ins, and you can't use body language to rein in tough customers.
  - **How**: test screen sharing during the confirmation call. **Prefer sharing their screen** (they use the product on their machine, which avoids lag). Share yours only if the thing exists only on your machine, and then tell them to hide private windows. Pick a tool with **setup under a minute, that works through corporate firewalls, and needs no app install** (IT departments often block installs). Use VOIP or a conference line, with the participant on speakerphone or headset rather than holding a phone for 50 minutes; ask them to minimize interruptions but expect some. Record on your side. Adjust the script slightly and send incentives electronically.
- **Unmoderated remote testing** (services like UserTesting): give a URL, one or two short tasks, participant count, and simple demographics. Screened testers do about 15 minutes of think-aloud, and you get recordings, often by the next day. It's cheap (about $29 per user when the book was written) and low-effort (you only write the task). **You can't ask questions or probe**, but participants are practiced thinkers-aloud.
  - **Use it for**: quick-and-dirty questions not worth or not able to wait for the monthly round, and **cheap retests of a fix** using an already-written task.
- **Sequencing rule**: *"You shouldn't try remote testing until you have some in-person tests under your belt."* Wait for about **three monthly in-person rounds** before running public remote sessions, because remote needs more concentration and losing visual cues hurts beginners most. Private experiments earlier are fine.
- **Keep the observation room.** Observers watch via screen share in both cases, so their experience is identical, and you keep the "clubhouse" effect of shared notes.

## Key Concepts
- **Moderated vs. unmoderated**: a facilitator is present live, or the participant is alone with written tasks.
- **80/70 rule**: Krug's (admittedly made-up) estimate of remote benefit vs. effort.

## Mental Models
- **Remote is a recruiting and scheduling tool, not a replacement.** Reach for it when location, profile, or cadence (Agile) is the constraint.
- **Unmoderated is a probe-less spot check.** Great for narrow, well-specified questions and verifying tweaks. Weak for discovering *why*.

## Anti-patterns
- Starting your testing practice remotely.
- Tools that need installs or fail behind firewalls.
- Sharing your screen by default, which adds lag.
- Dropping observers because "it's remote anyway".
- Using unmoderated tests where probing is essential.

## Key Takeaways
1. Remote moderated testing finds about the same problems with less logistics.
2. Expect more clarifying and less control. Adjust by prompting more.
3. Participants share their own screen with a zero-install tool, and you test the connection beforehand.
4. Use unmoderated services for quick questions and fix verification.
5. Do about three in-person rounds before running remote sessions publicly.
6. Still gather observers in one room.

## Connects To
- **Ch 3**: remote rounds make "a morning a sprint" feasible.
- **Ch 5**: remote standby participants and hard-to-find profiles.
- **Ch 11**: unmoderated tests as tweak verification.
