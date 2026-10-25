from kit import bars, c, chips, compare, cycle, flow, grid, part, ph, row, scatter, seq, stack, topic

TOPICS = [
    topic(
        "embeddings", "Embeddings", "Models",
        "Words and passages become points in space. Things used in similar ways land close together, so distance can stand in for meaning.",
        "An embedding turns text into a list of numbers: a point in space. Similar meanings land near each other, so closeness becomes something you can measure.",
        "Imagine a giant map where every word and sentence has its own spot, and the rule for placing them is simple: things that mean similar things sit close together. \"Puppy\" sits next to \"dog\", \"kitten\" is nearby, and \"spreadsheet\" is miles away. An embedding is the address of a piece of text on that map, written as a list of numbers (real maps use hundreds or thousands of directions, not just two). Once text has an address, a computer can measure meaning with a ruler: close means similar. That is how search can find \"cheap flights\" when you typed \"budget airfare\", even though not a single word matches.",
        [
            part(
                "embed",
                "Picture 1 · words become points",
                "Neighbours share meaning",
                "You cannot subtract \"diesel\" from \"petrol\". Strings have no distance. An embedding model maps each piece of text to a vector, and it learns that mapping from how words are used. Words that appear in similar places, like diesel, petrol and fuel, end up in the same region.",
                "\"gasoline\" was never in the list. Embed it the same way and it lands next to the fuel cluster. Its nearest neighbours are its closest meanings. That is the whole trick behind semantic search.",
            ),
            part(
                bars(
                    ["kitten", "dog", "lion", "carpet", "spreadsheet"],
                    [
                        ph("Compare", "How close is 'cat' to each of these? Score from 0 (unrelated) to 1 (same meaning).", 2800, values=[None, None, None, None, None]),
                        ph("Close", "'kitten' and 'dog' score high: they are used in very similar ways.", 2800, values=[92, 78, None, None, None], pick=[0, 1]),
                        ph("Far", "'carpet' and 'spreadsheet' score low.", 3400, values=[92, 78, 70, 21, 6], pick=[0, 1], foot="Similarity between embeddings, usually called cosine similarity."),
                    ],
                    title="similarity to 'cat' (illustrative)", unit="", div=100,
                ),
                "Picture 2 · closeness as a number",
                "A ruler for meaning",
                "The distance between two embeddings becomes a single similarity score. That number powers search, recommendations, duplicate detection and grouping documents by topic, all without any keyword matching.",
            ),
            part(
                compare(
                    "Keyword search", "Embedding search",
                    [
                        ph("Query", "Someone searches for 'budget airfare'.", 2600, l=[c("query: budget airfare", "code")], r=[c("query: budget airfare", "code")]),
                        ph("Search", "Keywords look for those exact words. Embeddings look for nearby meaning.", 3000, l=[c("query: budget airfare", "code"), c("'Cheap flights to Rome'", v="no match")], r=[c("query: budget airfare", "code"), c("'Cheap flights to Rome'", v="0.89")]),
                        ph("Result", "Same document, two outcomes.", 3400, l=[c("query: budget airfare", "code"), c("'Cheap flights to Rome'", "bad", v="missed")], r=[c("query: budget airfare", "code"), c("'Cheap flights to Rome'", "good", v="found")], win="r"),
                    ],
                ),
                "Picture 3 · finding meaning, not matching words",
                "What to watch for",
                "Use the same embedding model for stored text and queries; points from different models do not share a map. And close is not identical: \"refund\" and \"no refund\" can sit uncomfortably near each other, so important searches still deserve a check.",
            ),
        ],
        "An embedding is text turned into a point on a map of meaning, so similarity becomes distance.",
        "vector semantic search similarity cosine meaning",
    ),
    topic(
        "context-window", "Context window", "Models",
        "A model reads through a fixed-size window. When new tokens arrive the oldest fall out, and anything outside the window is simply not there.",
        "Everything a model can use at once lives in its context window. It has a hard size, and what falls outside it is gone.",
        "A model has no memory in the way you do. Each time it answers, it reads one block of text from top to bottom, and that block is the context window: your instructions, the chat so far, any documents, and the reply it is writing. Think of it as a desk. Whatever is on the desk the model can use. Whatever is not on the desk does not exist for it. Desks have a fixed size, measured in tokens. Modern windows are big, often hundreds of thousands of tokens, roughly a few novels, but they still fill up in long chats or with big documents. When they do, something has to come off the desk, and whatever leaves is gone.",
        [
            part(
                "window",
                "Picture 1 · old tokens fall out",
                "One fixed window",
                "The prompt, the conversation, retrieved documents and the answer being written all share one window. In the picture it holds six tokens. Real windows hold many thousands, but the rule is the same.",
                "When the window is full, the oldest tokens drop off the front in a simple setup. Ask about something that fell out and the model has nothing to read the answer from. It may still answer, which is worse.",
            ),
            part(
                bars(
                    ["instructions", "chat history", "documents", "room for the answer"],
                    [
                        ph("Start", "A fresh chat. Lots of room left.", 2600, values=[10, 5, 0, 85], pick=3),
                        ph("Chat", "Every message adds to the history.", 2600, values=[10, 35, 0, 55], pick=3),
                        ph("Docs", "Paste in a long document and it takes a big share.", 2800, values=[10, 35, 45, 10], pick=3),
                        ph("Full", "Now there is barely room for the answer. Something has to give.", 3400, values=[10, 40, 48, 2], pick=3, foot="Long chats get trimmed or summarised behind the scenes."),
                    ],
                    title="share of the window used",
                ),
                "Picture 2 · everything shares one window",
                "Everything competes for space",
                "Instructions, history, documents and the reply itself all come out of the same budget. That is why apps quietly trim or summarise long conversations, and why a very long chat can start forgetting what you said at the beginning.",
            ),
            part(
                compare(
                    "Let it slide", "Manage it",
                    [
                        ph("Long", "Two very long conversations.", 2600, l=[c("200 messages, nothing trimmed")], r=[c("200 messages, summarised as it goes")]),
                        ph("Ask", "Ask about something from the very start.", 2800, l=[c("200 messages, nothing trimmed"), c("'What was my budget?'")], r=[c("200 messages, summarised as it goes"), c("'What was my budget?'")]),
                        ph("Answer", "One lost it. The other kept the key facts in a short summary near the top.", 3600, l=[c("200 messages, nothing trimmed"), c("'What was my budget?'"), c("fell out of the window", "bad")], r=[c("200 messages, summarised as it goes"), c("'What was my budget?'"), c("'£1,500, from the summary'", "good")], win="r"),
                    ],
                ),
                "Picture 3 · managing the window",
                "What to watch for",
                "Put what matters near the question. Summarise long histories deliberately instead of letting them slide. And fetch facts when they are needed rather than hoping they survived from earlier.",
            ),
        ],
        "The context window is the model's whole world for one answer. If it is not in the window, it does not exist.",
        "context length tokens memory limit long context",
    ),
    topic(
        "temperature", "Temperature", "Models",
        "One setting reshapes the model's next-token scores. Low temperature makes it repeat its top pick; high temperature spreads the choices out.",
        "Temperature does not change what the model knows. It changes how boldly it picks from the options it already has.",
        "Remember that a model picks each next token from a list of options with scores. Temperature is a dial on how adventurous that pick is. Turn it down low and the model almost always takes the top option, so it says the same thing every time: steady, predictable, a bit dull. Turn it up and the less likely options get a real chance, so the writing becomes more varied and surprising, and eventually random. It is like asking a friend to recommend a restaurant: at low temperature they always name their favourite; at high temperature they might name anywhere they have ever eaten. Neither setting makes the model smarter or more correct.",
        [
            part(
                "temp",
                "Picture 1 · same scores, different boldness",
                "Same scores, different shape",
                "Before a token is chosen, the scores are adjusted by temperature. Low values sharpen them: the favourite gets almost everything. High values flatten them: the long tail gets a real chance.",
                "At 0.2, five draws give \"hold\" five times. At 1.0, mostly \"hold\" with the odd \"be\". At 1.8, every draw is different. The model and the prompt never changed.",
            ),
            part(
                chips([
                    ph("Prompt", "Same prompt, run three times at two settings.", 2600, rows=[row("prompt", [c("Name a cat")])]),
                    ph("Low", "At low temperature you get the same answer every time.", 3000, rows=[row("prompt", [c("Name a cat")]), row("temperature 0.2", [c("Luna", "dark"), c("Luna", "dark"), c("Luna", "dark")])]),
                    ph("High", "At high temperature each run is different.", 3400, rows=[row("prompt", [c("Name a cat")]), row("temperature 0.2", [c("Luna", "dark"), c("Luna", "dark"), c("Luna", "dark")]), row("temperature 1.2", [c("Biscuit", "hot"), c("Admiral Whiskers", "hot"), c("Mochi", "hot")])]),
                ]),
                "Picture 2 · steady versus surprising",
                "Picking a setting",
                "Low temperature suits extraction, SQL, classification and anything that must be repeatable. Higher suits brainstorming, names and first drafts, where variety is the point.",
            ),
            part(
                compare(
                    "Low temperature", "High temperature",
                    [
                        ph("Good", "Each end has jobs it is good at.", 3000, l=[c("write a SQL query", "good"), c("pull dates from an email", "good")], r=[c("ten slogan ideas", "good"), c("a story opening", "good")]),
                        ph("Bad", "And jobs it is bad at.", 3400, l=[c("write a SQL query", "good"), c("pull dates from an email", "good"), c("ten slogan ideas: all the same", "bad")], r=[c("ten slogan ideas", "good"), c("a story opening", "good"), c("a SQL query: creative syntax", "bad")]),
                    ],
                ),
                "Picture 3 · match the dial to the job",
                "What to watch for",
                "Low temperature makes answers consistent, not true. A model that is confidently wrong at 0.2 will be confidently wrong every single time.",
            ),
        ],
        "Temperature sets how boldly the model picks words: low for steady, high for varied. It never adds knowledge.",
        "sampling randomness creativity top-p deterministic",
    ),
    topic(
        "hallucination", "Hallucination", "Models",
        "When a model states something false with full confidence. It is not lying: it is producing the most plausible-sounding text, and plausible is not the same as true.",
        "A hallucination is a fluent, specific, confident answer that happens to be made up.",
        "A model is always predicting what text would most likely come next. Ask it who wrote a famous book and the most likely continuation is the right name. Now ask about a book that does not exist. The most likely-sounding continuation is still a confident name, a year and a neat summary, because that is what answers to that kind of question look like. That is a hallucination. The model is not lying; it has no built-in alarm that says \"I don't actually know this\", because it learned to sound like text, not to check facts. The fixes come from outside the model: give it real sources to read, let it look things up, ask it to cite, and test it.",
        [
            part(
                chips([
                    ph("Ask", "Ask about a book that does not exist.", 2600, rows=[row("question", [c("Who wrote 'The Glass Orchard'?")])]),
                    ph("Invent", "The model answers anyway, with confident details.", 3200, rows=[row("question", [c("Who wrote 'The Glass Orchard'?")])], out="Maria Ellison wrote it in 1994. It follows a family of fruit growers…", outCap="sounds sure · entirely made up", outC="bad"),
                    ph("Ground", "Give it a source to read, and it can say so honestly.", 3400, rows=[row("question", [c("Who wrote 'The Glass Orchard'?")]), row("library search result", [c("no book with that title found", "dark")], box=True)], out="I can't find a book called 'The Glass Orchard'. Could the title be slightly different?", outCap="answer from the source"),
                ]),
                "Picture 1 · a confident answer about nothing",
                "Plausible, not true",
                "Hallucinations are rarely random nonsense. They are specific and well formed, with names, dates and quotes, which is exactly what makes them dangerous. The more an answer looks like typical text, the more convincing a made-up one is.",
            ),
            part(
                bars(
                    ["Maria", "James", "Sarah", "Thomas", "everything else"],
                    [
                        ph("Scores", "Inside the model, no author name is a strong favourite. It is unsure.", 3000, values=[14, 12, 11, 10, 53]),
                        ph("Pick", "But a name still has to be picked. Once written, everything after builds on it.", 3600, values=[14, 12, 11, 10, 53], pick=0, foot="Low confidence inside, confident tone outside."),
                    ],
                    title="next-token scores for the author's first name (illustrative)",
                ),
                "Picture 2 · unsure inside, sure outside",
                "Why it happens",
                "The model always produces something. When no option is strong, it still picks one, and the rest of the sentence is written to fit. The uncertainty never shows up in the tone of the answer.",
            ),
            part(
                compare(
                    "Answer from memory", "Answer from sources",
                    [
                        ph("Memory", "Relying only on what the model absorbed in training.", 2800, l=[c("no source given"), c("cannot be checked"), c("wrong but confident", "bad")]),
                        ph("Sources", "Fetching documents and answering from them.", 3000, l=[c("no source given"), c("cannot be checked"), c("wrong but confident", "bad")], r=[c("searches the catalogue"), c("cites [1]"), c("says when it is not found", "good")]),
                        ph("Better", "Grounding does not remove hallucination entirely, but it makes it far rarer and easy to catch.", 3600, l=[c("no source given"), c("cannot be checked"), c("wrong but confident", "bad")], r=[c("searches the catalogue"), c("cites [1]"), c("says when it is not found", "good")], win="r"),
                    ],
                ),
                "Picture 3 · grounding the answer",
                "How to reduce it",
                "Give the model the facts (retrieval). Let it check live systems (tools). Ask it to quote or cite and to say \"I don't know\" when the source is silent. And measure hallucination with evals, rather than trusting how sure the answers sound.",
            ),
        ],
        "A model cannot tell what it knows from what merely sounds right, so give it sources and check.",
        "made up false confident grounding fabrication",
    ),
    topic(
        "pre-training", "Pre-training", "Training",
        "Stage one of making an LLM: read a huge slice of the internet and learn to predict the next token. The result knows a lot but is not yet an assistant.",
        "Pre-training is the long, expensive first stage, where a model learns language and the world by predicting text.",
        "Pre-training is a model's general education. It starts as random weights and is fed trillions of tokens of text: web pages, books, articles, code. Its only task is the next-token game: guess what comes next, check, adjust. After weeks of this on thousands of powerful chips, it has absorbed grammar, facts, writing styles and patterns of reasoning. But the result, called a base model, is an autocomplete, not an assistant. Ask it \"What is the capital of France?\" and it might carry on with \"What is the capital of Germany?\", because that is what a page of quiz questions looks like. Turning it into a helpful assistant is what the later stages are for.",
        [
            part(
                flow(
                    [("Raw text", "web, books, code"), ("Cleaning", "remove junk"), ("Next-token game", "weeks on GPUs"), ("Base model", "knows a lot")],
                    [
                        ph("Collect", "Gather an enormous amount of text.", 2600, at=0, packet="trillions of tokens"),
                        ph("Clean", "Remove spam, duplicates and low-quality pages. Data quality matters as much as size.", 3000, at=1, packet="filtered"),
                        ph("Train", "Play the predict-the-next-token game, at huge scale.", 3000, at=2, packet="guess · check · adjust"),
                        ph("Result", "Out comes a base model: broad knowledge, no manners yet.", 3200, at=3, packet="base model", say="Smart autocomplete, not yet an assistant."),
                    ],
                ),
                "Picture 1 · the pre-training pipeline",
                "Learning by reading everything",
                "Nobody labels this data. The text itself provides the answers, because the next word is always right there. That is what makes it possible to learn from so much material.",
            ),
            part(
                compare(
                    "Base model", "Assistant",
                    [
                        ph("Ask", "Ask both the same question.", 2600, l=[c("What is the capital of France?", "code")], r=[c("What is the capital of France?", "code")]),
                        ph("Reply", "The base model continues the text. The assistant answers it.", 3600, l=[c("What is the capital of France?", "code"), c("What is the capital of Spain? What is…", "bad")], r=[c("What is the capital of France?", "code"), c("Paris.", "good")], win="r"),
                    ],
                ),
                "Picture 2 · knows the answer, does not answer",
                "Knowledge without manners",
                "The base model probably \"knows\" Paris, but it was never taught that a question deserves an answer. Fine-tuning and feedback training teach that behaviour on top of the knowledge pre-training provides.",
            ),
            part(
                bars(
                    ["Pre-training", "Fine-tuning", "Feedback training"],
                    [
                        ph("Stages", "Three stages make a chat model.", 2600, values=[None, None, None]),
                        ph("Share", "Almost all of the computing effort goes into the first.", 3600, values=[95, 3, 2], pick=0, foot="Rough picture. The later stages are small but change behaviour a lot."),
                    ],
                    title="rough share of computing effort",
                ),
                "Picture 3 · where the effort goes",
                "Why it is so expensive",
                "Pre-training is why only a handful of organisations build frontier models from scratch. Everyone else starts from a pre-trained model and adapts it, which costs a tiny fraction.",
            ),
        ],
        "Pre-training gives a model its knowledge by predicting text at enormous scale. Later stages teach it to be an assistant.",
        "base model foundation model corpus training data",
    ),
    topic(
        "fine-tuning", "Fine-tuning", "Training",
        "Taking a model that already knows language and training it a little more on a small, focused set of examples, so it picks up a style, a format or a job.",
        "If pre-training is a general education, fine-tuning is job training.",
        "You take a model that already understands language and show it a few thousand carefully chosen examples of exactly what you want: questions paired with good assistant answers, or customer messages paired with the right category. The model's weights are nudged a little toward those examples. It does not need to relearn English, just the new habit, which is why fine-tuning costs a tiny fraction of pre-training. It is great for teaching form: a tone, a format, a narrow task done the same way every time. It is a poor way to add fresh facts. Those are better handled by handing the model documents at the moment it answers.",
        [
            part(
                chips([
                    ph("Examples", "Fine-tuning data is just pairs: an input and the output you want.", 3000, rows=[row("example 1", [c("'Where is my refund?'"), c("→"), c("billing", "hot")])]),
                    ph("More", "A few thousand of them, all in the same style.", 3000, rows=[row("example 1", [c("'Where is my refund?'"), c("→"), c("billing", "hot")]), row("example 2", [c("'App crashes on login'"), c("→"), c("bug", "hot")]), row("example 3", [c("'Love the new update!'"), c("→"), c("praise", "hot")])]),
                    ph("Habit", "The model learns the habit, not the facts in the examples.", 3400, rows=[row("example 1", [c("'Where is my refund?'"), c("→"), c("billing", "hot")]), row("example 2", [c("'App crashes on login'"), c("→"), c("bug", "hot")]), row("example 3", [c("'Love the new update!'"), c("→"), c("praise", "hot")])], out="New message → one short label, every time.", outCap="what it learns"),
                ]),
                "Picture 1 · teaching by example",
                "Small, focused data",
                "The examples are the whole lesson, so quality beats quantity. A few hundred clean, consistent examples often beat thousands of messy ones.",
            ),
            part(
                compare(
                    "Before fine-tuning", "After fine-tuning",
                    [
                        ph("Ask", "Classify a customer message.", 2600, l=[c("'Card charged twice'", "code")], r=[c("'Card charged twice'", "code")]),
                        ph("Reply", "The general model chats. The tuned one does the job.", 3600, l=[c("'Card charged twice'", "code"), c("'That sounds frustrating! There are several reasons this might…'", "bad")], r=[c("'Card charged twice'", "code"), c("billing · urgent", "good")], win="r"),
                    ],
                ),
                "Picture 2 · the same model, trained for one job",
                "Behaviour, not knowledge",
                "After fine-tuning, the model reliably produces the right shape of answer without long instructions in every prompt. That makes it cheaper and more consistent for repetitive tasks.",
            ),
            part(
                compare(
                    "Fine-tuning", "Retrieval",
                    [
                        ph("Fine", "Good for how the model behaves.", 2800, l=[c("tone and style", "good"), c("output format", "good"), c("a narrow task", "good")]),
                        ph("RAG", "Retrieval is better for what the model knows.", 3000, l=[c("tone and style", "good"), c("output format", "good"), c("a narrow task", "good")], r=[c("today's prices", "good"), c("your documents", "good"), c("facts that change", "good")]),
                        ph("Both", "Many systems use both: fine-tune the manner, retrieve the facts.", 3400, l=[c("tone and style", "good"), c("output format", "good"), c("a narrow task", "good"), c("new facts", "bad", v="weak")], r=[c("today's prices", "good"), c("your documents", "good"), c("facts that change", "good"), c("a new habit", "bad", v="weak")]),
                    ],
                ),
                "Picture 3 · fine-tune or retrieve?",
                "Choosing the right tool",
                "A common mistake is fine-tuning a model on company documents and expecting it to quote them accurately. It will pick up the style and vocabulary but blur the details. For facts, retrieval wins.",
            ),
        ],
        "Fine-tune for behaviour. Retrieve for knowledge.",
        "finetuning supervised lora adapt train custom model",
    ),
    topic(
        "rlhf", "Learning from feedback (RLHF)", "Training",
        "People compare pairs of answers and pick the better one. A reward model learns their taste, and the LLM is trained to score well with it.",
        "RLHF teaches a model the difference between an answer and a good answer, using human preferences.",
        "After fine-tuning, a model can answer questions, but \"an answer\" and \"a good answer\" are different things. RLHF, short for reinforcement learning from human feedback, teaches the difference. The model writes two answers to the same question. A person picks the better one: clearer, more honest, more helpful, safer. Thousands of these choices are used to train a second, smaller model called a reward model, which learns to predict what people will prefer. Then the main model practises against it: write an answer, get a score, adjust towards higher scores. Think of a chef cooking two versions of a dish for tasters, learning their taste, then cooking to it. It is a big part of why chatbots feel polite and helpful.",
        [
            part(
                compare(
                    "Answer A", "Answer B",
                    [
                        ph("Two", "The model writes two answers to 'How do I boil an egg?'", 3000, l=[c("Eggs have been eaten for millennia. The ancient…")], r=[c("Boil water, lower in the egg, 9 minutes, then cool.")]),
                        ph("Pick", "A person picks the one they prefer. That choice is the data.", 3400, l=[c("Eggs have been eaten for millennia. The ancient…")], r=[c("Boil water, lower in the egg, 9 minutes, then cool.", "good")], win="r"),
                    ],
                ),
                "Picture 1 · which answer is better?",
                "Preferences, not perfect answers",
                "It is much easier for people to compare two answers than to write a perfect one. RLHF takes advantage of that: the training signal is simply \"this one, not that one\", repeated many thousands of times.",
            ),
            part(
                flow(
                    [("Two answers", "same question"), ("Person picks", "A or B"), ("Reward model", "learns taste"), ("LLM practises", "aims high"), ("Better replies", "helpful")],
                    [
                        ph("Draft", "The model drafts pairs of answers.", 2400, at=0, packet="A · B"),
                        ph("Choose", "People choose the better of each pair.", 2400, at=1, packet="B wins"),
                        ph("Reward", "A reward model learns to predict those choices.", 2800, at=2, packet="B → 8/10"),
                        ph("Practise", "The LLM writes, gets scored, and adjusts towards higher scores.", 2800, at=3, packet="write · score · adjust"),
                        ph("Result", "Over time its answers drift towards what people prefer.", 3200, at=4, packet="clearer, kinder", say="Taste, learned from thousands of choices."),
                    ],
                ),
                "Picture 2 · from choices to a better model",
                "A judge that never gets tired",
                "People cannot score millions of practice answers, so the reward model stands in for them. It is a learned judge. The main model then improves through trial and error against that judge, which is the reinforcement learning part.",
            ),
            part(
                bars(
                    ["round 1", "round 10", "round 100", "round 1,000"],
                    [
                        ph("Start", "Early on, answers score middling with the reward model.", 2400, values=[42, None, None, None], pick=0),
                        ph("Up", "Practice pushes scores up.", 2400, values=[42, 61, None, None], pick=1),
                        ph("Up", "And up.", 2400, values=[42, 61, 78, None], pick=2),
                        ph("Careful", "Push too far and the model learns to please the judge rather than the person, for example by being wordy or flattering.", 3800, values=[42, 61, 78, 93], pick=3, foot="Called reward hacking. Training stops before it gets there."),
                    ],
                    title="average reward score (illustrative)",
                ),
                "Picture 3 · chasing the score",
                "What to watch for",
                "The reward model is only an approximation of human taste. Optimise against it too hard and the model finds its blind spots: overly long answers, agreeing with everything, sounding confident. Good RLHF knows when to stop.",
            ),
        ],
        "RLHF turns many 'this one, not that one' choices into a model that writes the answers people prefer.",
        "reinforcement learning human feedback reward model preference alignment dpo",
    ),
    topic(
        "prompt-engineering", "Prompt engineering", "Prompting",
        "Writing instructions so the model cannot misunderstand: who it is for, what to do, what good looks like, and what to hand back.",
        "A model can only work from what you put in front of it. Prompt engineering is the craft of putting the right things there.",
        "Imagine briefing a brilliant new colleague who knows nothing about your situation. If you say \"write about dogs\", they have to guess everything: how long, for whom, in what tone, for what purpose. They will produce something generic. Prompt engineering is simply writing a better brief. Good prompts usually cover a role (\"you are a vet\"), the task, the context (who it is for, what is already known), the constraints (length, tone, things to avoid) and the format you want back. Each piece removes a guess, and fewer guesses means better answers. It is less about magic phrases and more about being clear.",
        [
            part(
                chips([
                    ph("Vague", "A vague prompt gets a generic answer.", 2800, rows=[row("prompt", [c("write about dogs")])], out="Dogs are loyal companions that have lived alongside humans for thousands of years…", outCap="generic", outC="bad"),
                    ph("Role", "Add who should answer.", 2400, rows=[row("prompt", [c("write about dogs"), c("as a vet", "hot")])]),
                    ph("Reader", "Add who it is for.", 2400, rows=[row("prompt", [c("write about dogs"), c("as a vet", "hot"), c("for first-time owners", "hot")])]),
                    ph("Format", "Add what shape you want back.", 3600, rows=[row("prompt", [c("write about dogs"), c("as a vet", "hot"), c("for first-time owners", "hot"), c("5 tips, one line each", "hot")])], out="1. Book a vet check in the first week. 2. Start socialising early…", outCap="useful"),
                ]),
                "Picture 1 · each detail removes a guess",
                "Specific beats clever",
                "Most prompt problems are missing information, not missing tricks. If a colleague would need to ask a follow-up question, the model needed that information too. It just guessed instead of asking.",
            ),
            part(
                stack(
                    [("Role", "who is answering"), ("Task", "what to do"), ("Context", "what it needs to know"), ("Constraints", "limits and rules"), ("Format", "the shape of the output")],
                    [
                        ph("Role", "Who should the model act as?", 2600, at=0, title="Role", side="'You are a patient maths tutor.' Sets tone and expertise."),
                        ph("Task", "What exactly should it do?", 2600, at=1, title="Task", side="'Explain fractions.' One clear verb."),
                        ph("Context", "What does it need to know that it cannot guess?", 2600, at=2, title="Context", side="'The student is 10 and finds pizza examples helpful.'"),
                        ph("Limits", "What should it avoid, and how long should it be?", 2600, at=3, title="Constraints", side="'Under 120 words. No jargon.'"),
                        ph("Format", "What should the answer look like?", 3000, at=4, title="Format", side="'Three short steps, then one practice question.'"),
                    ],
                ),
                "Picture 2 · the parts of a good prompt",
                "A simple checklist",
                "Not every prompt needs all five parts, but running through them catches most gaps. Examples of good output (few-shot prompting) and asking for step-by-step reasoning are the next two tools to reach for.",
            ),
            part(
                bars(
                    ["task only", "+ context", "+ an example", "+ format"],
                    [
                        ph("Task", "Just the task.", 2200, values=[35, None, None, None], pick=0),
                        ph("Context", "Add context.", 2200, values=[35, 60, None, None], pick=1),
                        ph("Example", "Add an example of a good answer.", 2200, values=[35, 60, 78, None], pick=2),
                        ph("Format", "Add the output format.", 3200, values=[35, 60, 78, 90], pick=3, foot="Test prompts on several inputs, not just one."),
                    ],
                    title="answers usable without edits (illustrative)",
                ),
                "Picture 3 · each addition helps",
                "What to watch for",
                "A prompt that works once is not a prompt that works. Try it on ten different inputs, including awkward ones, and keep the ones that break as test cases. That is the beginning of an eval.",
            ),
        ],
        "A good prompt is a good brief: role, task, context, constraints and format.",
        "prompting instructions prompt design tips",
    ),
    topic(
        "system-prompts", "System prompts", "Prompting",
        "Hidden instructions set before the conversation starts. They set the model's role, rules and tone for every message that follows.",
        "The system prompt is the job description you never see, written by whoever built the app.",
        "When you chat with an AI app, there is usually a message you never see, placed at the very start: the system prompt. It is written by the people who built the app, and it says things like \"You are a friendly cooking assistant. Keep answers short. Never give medical advice.\" Every message you send is read with that in mind. That is how the same underlying model can be a cooking helper in one app and a coding tutor in another. Think of it as the brief handed to an actor before the play: the audience only sees the performance, but the role was set in advance. Models are trained to give the system prompt more weight than ordinary messages.",
        [
            part(
                seq(
                    ["App", "Model", "You"],
                    [
                        (0, 1, "System: You are a cooking helper. Be brief.", "code"),
                        (2, 1, "What can I make with eggs?"),
                        (1, 2, "Omelette, frittata or egg fried rice."),
                    ],
                    [
                        ph("System", "Before you type anything, the app sends its instructions.", 2800, upto=0),
                        ph("You", "Then your message arrives.", 2400, upto=1),
                        ph("Reply", "The model answers in the role it was given: short and about cooking.", 3200, upto=2),
                    ],
                ),
                "Picture 1 · the message before your message",
                "Set once, applies to everything",
                "The system prompt sits at the top of the context window for the whole conversation. Every reply is written in its light, without the user ever needing to repeat it.",
            ),
            part(
                compare(
                    "System: fitness coach", "System: barista",
                    [
                        ph("Ask", "Same model, same question, two different system prompts.", 2800, l=[c("'Is coffee bad for me?'", "code")], r=[c("'Is coffee bad for me?'", "code")]),
                        ph("Reply", "The role changes the whole angle of the answer.", 3600, l=[c("'Is coffee bad for me?'", "code"), c("Up to 3–4 cups a day is fine. Avoid it close to bedtime.")], r=[c("'Is coffee bad for me?'", "code"), c("In moderation it's fine. Have you tried a flat white?")]),
                    ],
                ),
                "Picture 2 · same model, different role",
                "One model, many products",
                "Most AI products are not separate models. They are the same few models with different system prompts, tools and documents around them.",
            ),
            part(
                stack(
                    [("System prompt", "set by the app"), ("Earlier messages", "the chat so far"), ("Your new message", "just typed"), ("The reply", "being written")],
                    [
                        ph("Top", "The system prompt always comes first.", 2600, at=0, title="System prompt", side="Role, rules, tone. Hidden from you, highest priority for the model."),
                        ph("History", "Then the conversation so far.", 2400, at=1, title="History", side="Everything said before, as long as it fits in the window."),
                        ph("New", "Then your latest message.", 2400, at=2, title="Your message", side="Read in the context of everything above it."),
                        ph("Reply", "The reply is written underneath all of it.", 3000, at=3, title="The reply", side="Predicted token by token from the whole stack."),
                    ],
                ),
                "Picture 3 · what the model actually reads",
                "What to watch for",
                "A system prompt is guidance, not a lock. Clever users can sometimes talk a model out of its instructions, so anything that really matters, like who can see what data, belongs in code, not just in the prompt.",
            ),
        ],
        "The system prompt quietly sets the role and rules for the whole conversation.",
        "system message instructions persona role",
    ),
    topic(
        "few-shot", "Few-shot prompting", "Prompting",
        "Instead of describing what you want, show two or three examples. The model copies the pattern.",
        "Sometimes showing is easier than explaining. Few-shot prompting puts examples of the answer right in the prompt.",
        "Say you want product reviews labelled as happy, angry or mixed. You could write a page of rules, or you could just show a few: \"Love it!\" → happy. \"Broke in a day.\" → angry. \"Great sound, awful battery.\" → mixed. Then give the new review and leave the answer blank. The model spots the pattern and fills it in the same way, including the exact format. That is few-shot prompting: a few examples, called shots, inside the prompt. Nothing is retrained; the examples simply sit in the context window while the model answers. No examples is called zero-shot, one is one-shot.",
        [
            part(
                chips([
                    ph("One", "First example: a review and its label.", 2400, rows=[row("example", [c("'Love it!'"), c("→"), c("happy", "hot")])]),
                    ph("Two", "Second example.", 2400, rows=[row("example", [c("'Love it!'"), c("→"), c("happy", "hot")]), row("example", [c("'Broke in a day.'"), c("→"), c("angry", "hot")])]),
                    ph("Three", "Third example.", 2400, rows=[row("example", [c("'Love it!'"), c("→"), c("happy", "hot")]), row("example", [c("'Broke in a day.'"), c("→"), c("angry", "hot")]), row("example", [c("'Great sound, awful battery.'"), c("→"), c("mixed", "hot")])]),
                    ph("New", "Now a new review with the answer left blank.", 2600, rows=[row("example", [c("'Love it!'"), c("→"), c("happy", "hot")]), row("example", [c("'Broke in a day.'"), c("→"), c("angry", "hot")]), row("example", [c("'Great sound, awful battery.'"), c("→"), c("mixed", "hot")]), row("your turn", [c("'Fast delivery, wrong colour.'"), c("→"), c("?", "gap")])]),
                    ph("Fill", "The model follows the pattern, format and all.", 3200, rows=[row("example", [c("'Love it!'"), c("→"), c("happy", "hot")]), row("example", [c("'Broke in a day.'"), c("→"), c("angry", "hot")]), row("example", [c("'Great sound, awful battery.'"), c("→"), c("mixed", "hot")]), row("your turn", [c("'Fast delivery, wrong colour.'"), c("→"), c("mixed", "dark")])]),
                ]),
                "Picture 1 · show, then ask",
                "The pattern is the instruction",
                "The examples teach several things at once: the task, the possible labels, the exact format (one lowercase word, no explanation) and where the line between categories sits.",
            ),
            part(
                bars(
                    ["zero-shot", "one-shot", "few-shot (3)"],
                    [
                        ph("Zero", "With no examples, the model guesses the format and the labels.", 2600, values=[62, None, None], pick=0),
                        ph("One", "One example helps a lot.", 2600, values=[62, 76, None], pick=1),
                        ph("Few", "A few well-chosen examples help more.", 3200, values=[62, 76, 87], pick=2, foot="Varied examples beat many similar ones."),
                    ],
                    title="labels correct out of 100 (illustrative)",
                ),
                "Picture 2 · examples improve accuracy",
                "Choose examples carefully",
                "The model copies everything about the examples, including their quirks. If all three examples are short, it will assume reviews are short. If two of three say happy, it may lean happy. Cover the tricky cases.",
            ),
            part(
                compare(
                    "Describe it", "Show it",
                    [
                        ph("Describe", "Writing the rules out in words.", 3000, l=[c("a page of rules"), c("edge cases forgotten", "bad"), c("format drifts", "bad")]),
                        ph("Show", "Showing three examples instead.", 3400, l=[c("a page of rules"), c("edge cases forgotten", "bad"), c("format drifts", "bad")], r=[c("three examples"), c("pattern picked up", "good"), c("format copied exactly", "good")], win="r"),
                    ],
                ),
                "Picture 3 · describing versus showing",
                "When to use it",
                "Few-shot shines for classification, extraction and anything with a strict format. It costs tokens, since the examples are sent with every request, so when a task becomes routine it may be worth fine-tuning instead.",
            ),
        ],
        "Show a few examples of the answer you want, and the model will follow the pattern.",
        "few shot zero shot one shot examples in-context learning",
    ),
    topic(
        "chain-of-thought", "Chain of thought", "Prompting",
        "Asking the model to work through the steps before answering. Writing the steps out gives it room to get the answer right.",
        "Thinking out loud helps models for the same reason it helps people: each written step becomes something to build on.",
        "Try this: a bat and a ball cost £1.10 together, and the bat costs £1 more than the ball. How much is the ball? Most people blurt out 10p, which is wrong. It is 5p. Slow down and write the steps, and you get it right. Models behave similarly. Because a model writes one token at a time, every token it writes becomes something it can read and build on. If it jumps straight to the answer, all the thinking has to happen inside one step. If it writes out the reasoning first, each step supports the next. That is chain of thought. Newer reasoning models do this on their own, thinking at length before they reply.",
        [
            part(
                compare(
                    "Answer straight away", "Think step by step",
                    [
                        ph("Puzzle", "Bat and ball cost £1.10. The bat costs £1 more than the ball. How much is the ball?", 3400),
                        ph("Rush", "Rushing gives the intuitive, wrong answer.", 2800, l=[c("ball = 10p", "bad")]),
                        ph("Step 1", "Writing it out: call the ball x.", 2600, l=[c("ball = 10p", "bad")], r=[c("ball = x, bat = x + £1")]),
                        ph("Step 2", "Together they cost £1.10.", 2600, l=[c("ball = 10p", "bad")], r=[c("ball = x, bat = x + £1"), c("x + x + £1 = £1.10")]),
                        ph("Answer", "So 2x = 10p, and the ball is 5p.", 3400, l=[c("ball = 10p", "bad")], r=[c("ball = x, bat = x + £1"), c("x + x + £1 = £1.10"), c("ball = 5p", "good")], win="r"),
                    ],
                ),
                "Picture 1 · rushing versus reasoning",
                "Room to think",
                "A model spends roughly the same amount of computation on every token. Asking for steps gives it more tokens, and so more computation, before it commits to the answer.",
            ),
            part(
                flow(
                    [("Question", "the puzzle"), ("Step 1", "name it"), ("Step 2", "write the sum"), ("Step 3", "solve"), ("Answer", "5p")],
                    [
                        ph("Ask", "The question arrives.", 2400, at=0, packet="bat + ball = £1.10"),
                        ph("Name", "First written step.", 2400, at=1, packet="ball = x"),
                        ph("Sum", "The next step reads the first one.", 2400, at=2, packet="2x + £1 = £1.10"),
                        ph("Solve", "And builds on it.", 2400, at=3, packet="2x = 10p"),
                        ph("Answer", "The answer rests on all the steps before it.", 3200, at=4, packet="ball = 5p", say="Each step is context for the next."),
                    ],
                ),
                "Picture 2 · each step feeds the next",
                "Why it works",
                "The written reasoning becomes part of the context window. The model is effectively leaving notes for itself, so a hard problem becomes a chain of easy ones.",
            ),
            part(
                bars(
                    ["answer directly", "think step by step"],
                    [
                        ph("Direct", "On multi-step maths word problems, answering directly often fails.", 2800, values=[25, None], pick=0),
                        ph("Steps", "Simply asking for steps can lift the score dramatically.", 3400, values=[25, 65], pick=1, foot="Biggest gains on maths, logic and planning; little gain on simple lookups."),
                    ],
                    title="multi-step word problems solved (illustrative)",
                ),
                "Picture 3 · a big jump on hard problems",
                "What to watch for",
                "Steps cost time and tokens, so they are wasted on simple questions. And the written reasoning is not a guaranteed window into what the model really did; it can still reach a wrong answer through neat-looking steps. Check the answer, not just the explanation.",
            ),
        ],
        "Asking a model to reason step by step gives it room to solve problems it would otherwise rush.",
        "cot reasoning step by step thinking reasoning models",
    ),
]
