## 7. Ethical reflection and data card

### Data card

| | |
|---|---|
| **Source** | Our own phone photos and videos; no images from the internet or other datasets |
| **Collected by** | Haki Abdulovski |
| **Where and when** | Leidschendam, The Hague and Rijswijk, October 2026, in day and night, in autumn |
| **What** | Pavement, gutters, drains, grass edges and verges |
| **Size** | 601 images uploaded (photos + frames from 7 videos), 599 labelled and used |
| **Labels** | One class, `cigarette_butt`, as bounding boxes; drafted by Gemini 4 Argon, every image reviewed by hand |
| **Split** | 419 / 120 / 60, random (frames of one video can be in several splits) |
| **Storage** | Private Roboflow project; COCO export in this repository |
| **Known gaps** | Few photos in grass and on dark surfaces; no rain or snow; only three municipalities; autumn leaves everywhere |

### Risks, and who could be harmed

The biggest risk is that the tool **undercounts exactly where it matters most for SDG 15**. It misses more butts in grass, leaves and dark corners than on light pavement. A municipality that trusts the numbers could conclude that parks and verges are clean and send its cleaning effort to the streets, while butts keep leaking into soil and water in the green areas. The same goes for comparisons: if the "after" photo is taken on a darker, wetter day, the model finds fewer butts and a measure looks successful when it isn't. Butts are only roughly counted (recall 72%), and the test scores are probably optimistic because of the random split. A second risk is **misuse for enforcement**: counts per spot could be used to target places where certain groups gather (a shelter, a coffee shop, a youth hangout), or photos could show people who never agreed to be photographed. Finally, municipalities can claim cleaning costs from producers under UPV; our counts are **not reliable enough for financial claims**.

### What we did about it
- **The app shows every box, not just a number,** so the user can see what was counted and spot misses or false alarms.
- **The confidence slider is visible,** and the README states the threshold our results are based on (0.40–0.42).
- **We documented the weak spots** (grass, dark surfaces, tiny and white butts, double boxes) and the optimistic split, instead of only reporting the best score.
- **No personal data:** we avoided faces and number plates, the Roboflow project is private, and the app stores no photos, locations or results.
- **We advise a fixed protocol:** compare the same spots, at the same distance and in similar light, and check a few photos by hand.

### What it must not be used for
- Fining or identifying **individual smokers**, or targeting places because of **who** spends time there.
- **Exact counts** for official reports or **cost claims** under UPV.
- Concluding that **green areas are clean**: the model is weakest there.
- Photos of **people**: point the camera at the ground.

### Next steps
More training photos in grass, on dark surfaces and with white filters; tiling for tiny butts; merging overlapping boxes in the app; a location-and-date log so a municipality can track spots over time; and a split by video, so frames of one clip never end up in both train and test.
