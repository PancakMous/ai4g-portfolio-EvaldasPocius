# Ethical reflection

**Project:** NS Rail Live Pulse: passenger sentiment radar for Dutch rail (SDG 9)

My stream is public Mastodon posts (almost all from mastodon.nl) plus a few Reddit posts, so it only hears from people who are online, post publicly and use these platforms. Passengers who are stuck without data, older travellers and people who write in other languages are largely absent. A calm dashboard could mean they could not post, not that they are happy.

The model is also weakest where it matters. RobBERT was trained on Dutch book reviews and has no neutral label, so 472 of my 620 stored posts (76%) come out "positive" in a stream about train disruptions. Factual alerts such as an "overwegstoring" notice were read as positive in 4 of 16 test cases. That is false calm. About 29% of stored items (178 of 620) are not tagged Dutch and still pass through a Dutch-only model. My test also showed it missing implicit complaints ("de melding komt nu pas binnen") and hashtag-only posts. I did not test dialect, sarcasm or capital-letter anger separately.

Bots are a real issue here. 138 stored posts (22%) are automated "STORING:" or "Storing voorbij:" alerts, and I do not store author IDs, so I cannot detect or cap one very active account.

For privacy, I do not store usernames, display names, avatars or account IDs, and I replace @mentions with [USER]. However, each stored `url` still contains the Mastodon handle for 577 of 620 posts, so the data is pseudonymised, not anonymous, and it must not be used to look up individuals. Mastodon timelines are public and I only read them, but I have not checked each instance's terms, and Reddit's terms for automated use are less clear than my README suggests.

**What I did about these risks:** I show item volume next to the sentiment score so a score built on few posts is visible, I dropped author data, and I documented the language mix and the missing neutral class.

**What could go wrong:** the decision is Maaike dispatching help only when net sentiment falls below -30. With 76% of posts scored positive, that threshold may almost never trigger, so she could miss a real disruption. The tool should only be a supplement to her own judgement, never the trigger.
