# Peak Ambition

A demo for [Picovision](https://shop.pimoroni.com/products/picovision) by jtruk.

In case this readme gets separated, the [repository lives here](https://github.com/creativenucleus/picovision-peakambition/).

There's a [video recording here](https://www.youtube.com/watch?v=-l3pBx9a-Zc) but beware... my video capture card is cheap and did bad stuff to the sound, so please don't judge the hardware on this video!

# Running

Copy all these files into the root of your Picovision with Thonny.

Run the `peak_ambition.py` file.

# Info

Peak Ambition is an entry to [Pimoroni's Picovision Party #000](https://shop.pimoroni.com/pages/win-a-500-gift-card-in-our-picovision-competition#picovision-party-000), submitted 17th November 2023.

Quite a short turnaround, but also quite a bit stuffed into this... hence the title - I felt I flew close to the sun!

Things to look out for:

- Classes and imports.
- A pretty cleanly architected effect system, with demo runner.
- Some likely reusable 3D geometry code.
- A fakey tracker for music. It's limited, but includes some nice features like arpeggio, vibrato, volume, multiple simultaneous effect triggering.
- Threaded execution, with some cross-thread communication.

Known issues 

- Framerate is variable, and not great. He flew too close to the sun. I decided pretty was better than bare. I'll try C++ for the next demo!
- Some colour transitions between effect states and the main vector text are not slick.
- Transitions between letters and effects could be better integrated.
- Notes sometimes hang around longer than they should. I've got a feeling the Picosynth library doesn't always respect triggerAttack and triggerRelease requests?
- Some sounds (esp. hi-hat) sound like they hit a little late. Not sure if that's a mistake in my code, or a product of variable frame rate.

# Licence

Attributed license: Pirate's Honour.

- Please feel welcome to adapt this demo if it helps you figure out some stuff. Please [let me know](https://mastodon.social/@jtruk) if so, I'd love to hear from you!
- You're also very welcome to take any code to incorporate into your own game or demo. I only ask that you give me a little acknowledgement (please credit: jtruk).
