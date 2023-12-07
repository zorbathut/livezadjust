Are you tired of sitting there and messing with calibration for live-Z adjustments? I know I sure am! Every live-Z system involves sitting there and fiddling with a knob manually, and I figured there was a better solution.

Now there is!

Mostly!

The first step still involves sitting there and fiddling with a knob manually, but it's fast.

----

### Steps, Along With Examples:

-   **You will want a fresh plastic razor for this**. Trust me, you're going to dislike the results if you don't have a *really* good way to remove stuff from your print bed. (If you're new to printing, you want plastic razors anyway, you will not regret this, they're really cheap.)
-   Grab the relevant gcode files. At the moment this is available with PLA or PETG, in 0.25, 0.4, and 0.6 nozzle sizes. See the Notes if you want more.
-   Adjust your Live-Z offset to higher than you think it should be. If this is the first time you've done this, 0.000 is completely fine.
-   Put in filament, ideally one that's visible on your print bed. I'm choosing black, because this black is very shiny, and I had it set up anyway, and I'm lazy. White would probably have been a better choice.
-   Print `1_initial_adjust`. Once it starts, it's knob-fiddlin' time! Change the Live-Z (it's near the top of the main menu). Your goal is to make the Z-adjust *too low*, without hitting the bed with your nozzle. Make the adjustment more negative until the line starts fading out. If you set it to a nice round number it'll make future steps easier. I just did this and ended up with -2.400. Don't copy my number - get your own! - that's just for example's sake.
-   This is the last time you'll be fiddling with the knob in realtime! Congratulations.
-   Once you've reached this point, don't stop the print! Just walk away and let it finish. If you stop it now it will be basically impossible to get it off the bed *even with* a plastic razor. It'll layer some more plastic on top of the previous lines to give you more leverage.
-   Remove the lines, toss 'em, remove the purge line, toss it, clean your bed if you like.
-   Print `2_coarse_adjust`. Walk away and let it finish, you don't need to pay attention right now.
-   Once it's done, come back and remove all the little tags off the print bed. If any of them fall apart while you're removing it, throw them away.
-   Rub the surface finish with your fingers. Is it rough and unpleasant? That means the nozzle was too low. Throw those away.
-   Try pulling the remaining tags apart with your fingers. If you can do so easily, the nozzle was too high up. Throw those away too.
-   You'll end up with one to four tags left. Pick the one you like the most. Throw the others away.
-   If all of them fell apart, or the best tag is +0.100, you didn't bring the Live-Z down far enough originally. Go back to Initial Adjustment and be more aggressive this time.
-   Each tag has, printed into it, the exact adjustment you need to make. Make that adjustment! While your printer isn't printing, the Live-Z adjustment is now *deep* inside the Settings menu. Sorry, you'll have to go hunting.
-   Note that the tag has a plus sign printed on it, and Live-Z adjustments are always negative. **This means that you are going to adjust the Live-Z to be closer to 0. Do not make the number larger. Make the number smaller. This is important.** In my case, I had -2.400 before, and my best tag said +0.350. -2.400 + 0.350 = -2.050. I adjust it to -2.050.
-   Throw the remaining plastic away, clean the purge line off, clean your bed if you like.
-   **Optional, but recommended:** Print `3_fine_adjust`.
-   You probably know what to do this time around. It's the same process, except the differences will be smaller.
-   One important note: They aren't all going to be + values! You may end up with a - tag. **If you get a - tag, make your Live-Z larger**. I just did this! I had -2.050 before, and my best tag was -0.020. -2.050 - 0.020 = -2.070.
-   **Optional, but not recommended:** Print `4_ultrafine_adjust`. Do the same thing again. I've never found this to be particularly useful, but this will get you right down to the accuracy limit of the Live-Z system. Doesn't hurt! Don't be surprised if you end up with an entire array of indistinguishable tags, though.
-   Depending on the exact value you ended up on, you may end up with a slight rounding error; the system will calibrate to 0.0025 points, but it's only capable of showing three decimal places, so it tends to round, and the tags may not have the same rounding. Just pick the closest one.

Congratulations, you're done! Your printer is now perfect! *You will never have printing problems of any sort again.*

That's a lie. But at least this problem is thoroughly solved!

----

### Some Notes

**Can I generate my own Gcode?**

You *may*.

It's a bit less clear if you *can*.

The actual process of doing this requires significant postprocessing; no slicer I'm aware of is able to do the specific things needed to build this gcode. Because I'm not completely insane, I wrote a program to do this for me. The program and all necessary input files [are available on Github](https://github.com/zorbathut/livezadjust).

However, this was never really built for anyone besides me. In its current form, it assumes you have openscad installed in the path and PrusaSlicer installed via flatpak, which you have, because you're running on Linux, right?

You are unlikely to be able to get this working unless you're a programmer. Also the code sucks. Sorry.

If you *are* a programmer, and you make it more flexible or clean it up, please send a pull request!

**I have a 0.80 nozzle and I'm using it to print ASA. Can you generate Gcode for me?**

Sure! Pester me on Discord (ZorbaTHut). You can drop me a note but I probably won't see it.

**I have a custom 0.69 nozzle and I'm using it to print a fancy new filament named PONKBORT that is available only to a specific village of superintelligent crabs in northeast Malaysia. Can you generate Gcode for me?**

No.

But pester me on Discord anyway and I'll help you get the scripts working on your computer.

**0.60-nozzle tags are kind of hard to read.**

Yeah, they are. The problem is that they need to be bigger to be more legible, but if I make them bigger, they don't fit on the bed. I *should* be generating two rows, but I haven't done that yet. Known issue.
