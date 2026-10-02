## 9. Ethical reflection

| Risk | What it would mean for our viewers | What we did about it |
|---|---|---|
| **The footage gets taken for real documentary footage.** It looks photoreal, but it isn't any real reef. | A viewer screenshots shot 05, shares it as "the Great Barrier Reef right now", and someone debunks it. Fake images in climate communication give deniers an easy argument, and they can make viewers distrust *real* reef footage too. | We never name or suggest a real location. The film ends with a card that says **"AI-generated imagery & voice · Data: ICRI 2025"**, and the same note is in the YouTube description and at the top of this README. The images show *how* bleaching works, while the one hard number (84%) comes from a cited source, so viewers can check the claim without trusting the pictures. |
| **The voice sounds like a real narrator.** | Viewers might assume a real expert or organisation is speaking. | The voice is a stock Kokoro TTS voice generated in ComfyUI, not a clone of a real person. It's disclosed on the same end card. |
| **Emotional manipulation.** Shot 05 is designed to feel bleak. | Climate despair makes young people tune out. That's the opposite of what we want from this audience. | Shots 06–07 end on *partial, conditional* recovery: realistic hope without a fake happy ending. The bleakness is backed by a real, sourced number, so it's persuasion based on facts, not exaggeration. |
| **The training data was used without consent.** | Wan 2.2 learned from imagery scraped from the web, likely including underwater photographers' work, without paying or asking them. | We can't fix this ourselves. We kept the project non-commercial and state it openly here. |

No people appear in the film, so there are no issues with anyone's face or likeness.

**Energy cost:** To get 7 usable shots we generated **15 clips**, and **8 of them were thrown away**. Before that we also ran a few tests with a different video model (LTX) and abandoned it. Everything ran locally on one PC with an **AMD Radeon RX 6950 XT** (16 GB, up to 335 W) and an i5-12600K. The ComfyUI log shows how long each render took:

| | Clips | Kept | GPU time |
|---|---|---|---|
| LTX tests (different model, abandoned) | – | 0 | ≈ 35 min |
| Wan 2.2 setup runs that never produced a clip | – | 0 | ≈ 75 min |
| Wan 2.2 short test clips (49 frames, `00001`–`00003`) | 3 | 0 | not logged (earlier session) |
| Wan 2.2 shot renders (`00004`–`00015`) | 12 | 7 | ≈ 64 min (≈ 4 min per clip once set up) |
| **Total** | **15** | **7** | **≈ 2.9 hours** |

Of the 12 shot renders, the 5 we threw away were all failed attempts at shot 04 (see §5).

At roughly 400 W for the whole PC, that comes to about **1.2 kWh**, or about **0.3 kg CO₂** on the Dutch grid (0.27 kg/kWh). That's about the same as one washing-machine cycle, or driving 2 km in a petrol car.

We think that's a small, defensible cost for a film meant to reach thousands of people. But it's still extra energy spent making a film about climate, and most of it was wasted. **Only about a quarter of the GPU time (≈ 44 of 174 min) went into the 7 clips that are in the film.** The rest went into an abandoned model, setup runs, and five tries at shot 04. Next time we would settle on one model first and test prompts as short, low-resolution clips before rendering at full length. That would have caught the shot 04 prompt problem after one cheap test instead of five full renders.
