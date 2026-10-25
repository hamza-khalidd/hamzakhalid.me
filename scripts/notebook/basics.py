from kit import bars, c, chips, compare, cycle, flow, grid, part, ph, row, scatter, stack, topic

TOPICS = [
    topic(
        "ai-ml-dl", "AI, ML and deep learning", "Basics",
        "Three words people use as if they meant the same thing. They are circles inside circles: AI is the goal, machine learning is one way to reach it, deep learning is one kind of machine learning.",
        "AI, machine learning and deep learning are not rivals. Each one sits inside the one before it.",
        "Think of Russian dolls. The biggest doll is artificial intelligence: any computer program that does something we would call smart, like playing chess or understanding speech. Inside it sits machine learning. Instead of a person writing every rule by hand, the computer is shown lots of examples and works the rules out for itself. Inside that sits deep learning: machine learning done with very large networks of simple maths units stacked in layers, loosely inspired by brain cells. ChatGPT, Claude and Gemini live in the smallest doll. They are deep learning models, which makes them machine learning, which makes them AI. The reverse is not true. A 1990s chess program that only follows hand-written rules is AI, but it learned nothing.",
        [
            part(
                stack(
                    [("Artificial intelligence", "the goal"), ("Machine learning", "learns from examples"), ("Deep learning", "many-layer networks"), ("Language models", "deep learning on text")],
                    [
                        ph("AI", "The outer circle. Any program that behaves in a way we would call smart.", 3000, at=0, title="Artificial intelligence", side="Chess engines, route planners, spam filters. Even a program of hand-written if-then rules counts."),
                        ph("ML", "One way to build AI: learn the rules from examples instead of writing them.", 3000, at=1, title="Machine learning", side="Show it thousands of examples with answers and it finds the pattern itself."),
                        ph("Deep", "One kind of machine learning: huge networks with many layers.", 3000, at=2, title="Deep learning", side="Layers of tiny calculators. Each layer builds bigger ideas out of the layer before."),
                        ph("LLMs", "Today's chatbots sit in the smallest circle, inside all the others.", 3200, at=3, title="Large language models", side="Deep learning trained on a huge amount of text. ChatGPT, Claude and Gemini live here."),
                        ph("All", "Every inner circle is also part of the outer ones.", 3000, at=[0, 1, 2, 3], title="Circles inside circles", side="An LLM is deep learning, which is machine learning, which is AI."),
                    ],
                ),
                "Picture 1 · circles inside circles",
                "Four words, one family",
                "AI is the broad goal: make computers do things that look intelligent. Machine learning is the most successful route to that goal so far. Deep learning is the most successful kind of machine learning. Large language models are deep learning models trained on text.",
                "So when someone says \"we use AI\", it could mean anything from a few rules in a spreadsheet to a model with billions of learned settings. Asking \"does it learn from data?\" is the quickest way to find out which.",
            ),
            part(
                compare(
                    "Rules written by hand", "Rules learned from examples",
                    [
                        ph("Start", "Two ways to build a spam filter.", 2800, l=[c("if subject says 'FREE' → spam")], r=[c("10,000 emails, each marked spam or not")]),
                        ph("Build", "One person writes rules. The other lets the computer find them.", 3000, l=[c("if subject says 'FREE' → spam"), c("if sender is unknown → spam")], r=[c("10,000 emails, each marked spam or not"), c("model finds its own patterns")]),
                        ph("New trick", "Spammers change 'FREE' to 'Fr€e'. The written rule misses it. The learned one has seen enough to catch it.", 3600, l=[c("if subject says 'FREE' → spam"), c("if sender is unknown → spam"), c("'Fr€e prize!'", "bad", v="missed")], r=[c("10,000 emails, each marked spam or not"), c("model finds its own patterns"), c("'Fr€e prize!'", "good", v="caught")], win="r"),
                    ],
                ),
                "Picture 2 · written rules versus learned rules",
                "Why learning won",
                "Hand-written rules are clear but brittle. The world keeps producing cases nobody wrote a rule for. A learned model picks up patterns too subtle or too numerous for a person to list, and it can be retrained when the world changes.",
                "The cost is that learned rules are harder to read. You cannot open a model and find the line that says \"Fr€e means spam\". That trade, power for transparency, comes up again and again in AI.",
            ),
        ],
        "All deep learning is machine learning, and all machine learning is AI. Not the other way round.",
        "artificial intelligence machine learning deep learning difference basics",
    ),
    topic(
        "machine-learning", "Machine learning", "Basics",
        "Instead of writing the rules, you show the computer examples with answers and let it find the pattern. Then it uses that pattern on cases it has never seen.",
        "Machine learning means learning a pattern from examples, then using it on something new.",
        "Think about how a child learns what a cat is. Nobody hands them a rulebook that says \"four legs, whiskers, pointy ears\". You point at cats and say \"cat\", point at dogs and say \"not a cat\", and after enough examples they just get it. Machine learning works the same way. You collect examples where you already know the answer: house sizes with their prices, or emails marked spam or not spam. The computer searches for a pattern that links each example to its answer. Once it has found a good one, you give it a new example without an answer, and it predicts one. The pattern it learned is called a model, and the learning step is called training.",
        [
            part(
                scatter(
                    [["apple", 22, 30, "a"], ["apple", 30, 22, "a"], ["apple", 16, 40, "a"], ["apple", 34, 36, "a"], ["lemon", 70, 62, "b"], ["lemon", 80, 52, "b"], ["lemon", 64, 74, "b"], ["lemon", 84, 70, "b"]],
                    {"a": "apples", "b": "lemons"},
                    [
                        ph("Examples", "We start with fruit we have already labelled.", 2600, placed=False),
                        ph("Plot", "Place each one by two features: colour and shape. Apples gather in one corner, lemons in another.", 3200),
                        ph("New fruit", "A fruit nobody labelled arrives. Where does it land?", 2800, query=["?", 28, 32]),
                        ph("Predict", "Its nearest neighbours are all apples, so the model calls it an apple.", 3400, query=["?", 28, 32], near=[0, 1, 3]),
                    ],
                ),
                "Picture 1 · a new example lands near the ones it resembles",
                "Learning from examples",
                "The model never received a definition of an apple. It only got examples, each described by a few numbers (how red, how round) and a label. Learning means finding where the labels fall in that space.",
                "A new, unlabelled fruit gets described with the same numbers. It lands somewhere, and the model answers with the label of that region. Most machine learning, however fancy, is a version of this.",
            ),
            part(
                flow(
                    [("Examples", "with answers"), ("Training", "find the pattern"), ("Model", "the pattern"), ("New case", "no answer"), ("Prediction", "best guess")],
                    [
                        ph("Collect", "Gather examples where the answer is already known.", 2600, at=0, packet="1,000 houses + prices"),
                        ph("Train", "The computer adjusts itself until it matches those answers as well as it can.", 2800, at=1, packet="looking for patterns"),
                        ph("Model", "What remains is the model: the pattern, stored as numbers.", 2600, at=2, packet="size → price"),
                        ph("Use", "Now give it a house it has never seen.", 2600, at=3, packet="90 m², 2 bed"),
                        ph("Predict", "It answers from the pattern it learned.", 3000, at=4, packet="≈ £240k", say="A prediction, not a certainty."),
                    ],
                ),
                "Picture 2 · the whole journey",
                "Training, then using",
                "There are two separate moments. Training happens once (or occasionally) and is slow and expensive. Using the model, called inference, happens every time someone asks and is quick.",
                "This is why a model can be out of date. It knows the pattern from its training examples, not anything that happened after.",
            ),
            part(
                bars(
                    ["10 examples", "100 examples", "1,000 examples", "10,000 examples"],
                    [
                        ph("10", "With ten examples, the model is barely better than guessing.", 2400, values=[55, None, None, None], pick=0),
                        ph("100", "More examples, a clearer pattern.", 2400, values=[55, 72, None, None], pick=1),
                        ph("1k", "Keep going and it gets steadily better.", 2400, values=[55, 72, 86, None], pick=2),
                        ph("10k", "Gains slow down, but rarely stop.", 3200, values=[55, 72, 86, 92], pick=3, foot="More, cleaner examples is usually the cheapest upgrade."),
                    ],
                    title="correct answers out of 100 (illustrative)",
                ),
                "Picture 3 · more examples, better pattern",
                "Data is the ingredient",
                "A model is only as good as its examples. More examples help, but so does variety and correct labels. A thousand mislabelled examples teach the wrong pattern very confidently.",
            ),
        ],
        "Show examples with answers, let the computer find the pattern, then use it on new cases.",
        "ml training inference model prediction data examples supervised",
    ),
    topic(
        "neural-networks", "Neural networks", "Basics",
        "Layers of tiny calculators, each passing a number to the next. Training tunes millions of little dials until the right answer comes out at the end.",
        "A neural network is a stack of very simple maths, repeated millions of times. What it knows lives in its settings, not its code.",
        "Imagine a huge team of very simple workers arranged in rows. Each worker takes numbers from the row before, multiplies each one by how much it trusts that source (that trust is called a weight), adds them up and passes a single number on. The first row looks at raw input, like the pixels of a photo. The middle rows combine those into bigger ideas: first edges, then shapes, then \"this looks like an ear\". The last row gives the answer: \"cat, 92 percent\". No single worker knows what a cat is. The knowledge is spread across the weights, millions or billions of little dials, and learning simply means turning those dials until the answers come out right.",
        [
            part(
                flow(
                    [("Input", "pixels"), ("Layer 1", "edges"), ("Layer 2", "shapes"), ("Layer 3", "parts"), ("Output", "answer")],
                    [
                        ph("Pixels", "A photo goes in as thousands of numbers, one per pixel.", 2600, at=0, packet="photo"),
                        ph("Edges", "The first layer reacts to simple things like lines and edges.", 2600, at=1, packet="lines"),
                        ph("Shapes", "The next layer combines edges into curves and corners.", 2600, at=2, packet="curves"),
                        ph("Parts", "Deeper still, shapes become parts: an ear, an eye, whiskers.", 2600, at=3, packet="ears, whiskers"),
                        ph("Answer", "The last layer weighs it all up and gives an answer.", 3200, at=4, packet="cat · 92%", say="Each layer builds on the one before."),
                    ],
                ),
                "Picture 1 · layers build bigger ideas",
                "Layers, from simple to complex",
                "Nobody tells the layers what to look for. They work it out during training, and the progression from edges to parts appears on its own because it is a useful way to recognise things.",
                "\"Deep\" in deep learning just means many layers. More layers let the network build more abstract ideas.",
            ),
            part(
                chips([
                    ph("Inputs", "One single worker, called a neuron. It gets three signals: 1 means yes, 0 means no.", 3000, rows=[row("inputs", [c("whiskers", n=1), c("pointy ears", n=1), c("barks", n=0)])]),
                    ph("Weights", "Each signal is multiplied by a weight: how much this neuron trusts it.", 3000, rows=[row("inputs", [c("whiskers", n=1), c("pointy ears", n=1), c("barks", n=0)]), row("weights", [c("× 0.9", "dark"), c("× 0.7", "dark"), c("× −0.8", "dark")])]),
                    ph("Sum", "Add it all up. A high total means: this looks like a cat.", 3400, rows=[row("inputs", [c("whiskers", n=1), c("pointy ears", n=1), c("barks", n=0)]), row("weights", [c("× 0.9", "dark"), c("× 0.7", "dark"), c("× −0.8", "dark")]), row("signal passed on", [c("0.9 + 0.7 + 0 = 1.6", "hot")])], out="1.6 is high, so it fires: 'cat-like'", outCap="decision"),
                ]),
                "Picture 2 · one neuron, up close",
                "Each worker is just a sum",
                "A neuron multiplies, adds and passes a number on. That is all. The power comes from having millions of them and from getting the weights right.",
                "A negative weight means \"this is evidence against\". Barking counts against cat, which is exactly what you would want.",
            ),
            part(
                grid(
                    ["layer 1", "layer 2", "layer 3"], ["w1", "w2", "w3", "w4", "w5", "w6"],
                    [
                        ph("Random", "Before training, every weight is random. The answers are nonsense.", 2800, cap="before training: random dials", cells=[[0.5, 0.2, 0.8, 0.3, 0.6, 0.4], [0.3, 0.7, 0.2, 0.9, 0.1, 0.5], [0.6, 0.4, 0.5, 0.2, 0.8, 0.3]]),
                        ph("Nudge", "Each mistake nudges the weights a little.", 2600, cap="training: small nudges", cells=[[0.6, 0.15, 0.7, 0.25, 0.5, 0.45], [0.25, 0.75, 0.3, 0.8, 0.15, 0.4], [0.7, 0.3, 0.45, 0.2, 0.85, 0.25]]),
                        ph("Tuned", "After millions of nudges, the dials settle into a pattern that works.", 3200, cap="after training: tuned dials", cells=[[0.9, 0.05, 0.6, 0.1, 0.3, 0.7], [0.1, 0.95, 0.4, 0.6, 0.2, 0.15], [0.85, 0.1, 0.3, 0.15, 0.95, 0.05]]),
                    ],
                ),
                "Picture 3 · the knowledge is in the dials",
                "What \"a model\" actually is",
                "Strip away the software and a trained network is a long list of numbers. A model with seven billion parameters is seven billion of these dials.",
                "That is why you cannot simply read what a model knows. There is no sentence inside it, only settings that together happen to produce good answers.",
            ),
        ],
        "A neural network is many simple sums in layers. Everything it knows is stored in its weights.",
        "neuron weights layers deep learning parameters",
    ),
    topic(
        "training", "How a model learns", "Basics",
        "Guess, measure how wrong, nudge the dials a little, repeat. Millions of tiny corrections turn a random network into a useful one.",
        "Training is a loop of guessing and correcting. The model never gets told the rule. It just keeps getting less wrong.",
        "Picture throwing darts blindfolded while a friend calls out \"a bit left, a bit lower\". That is training. The model starts with random weights, so its first guesses are rubbish. For each example it makes a guess, and a score called the loss says how wrong it was. A method called gradient descent works out which way to turn every dial so the loss gets a little smaller, and turns each one a tiny amount. Then it moves on to the next example. Repeat that millions of times and the guesses get steadily better. Learning too well is its own problem: a model can memorise its practice examples and then fail on new ones, which is why we always test on examples it never trained on.",
        [
            part(
                cycle(
                    ["Guess", "Measure", "Nudge"],
                    [
                        ph("Guess", "The model guesses a house price. The real price is £100k.", 2400, at=0, center="£40k", sub="guess", lines=["try 1 · guessed £40k"]),
                        ph("Measure", "It was off by £60k. That gap is the loss.", 2400, at=1, center="−£60k", sub="very wrong", lines=["try 1 · guessed £40k", c("off by £60k")]),
                        ph("Nudge", "Turn the dials a little in the direction that shrinks the gap.", 2400, at=2, center="↑", sub="nudge up", lines=["try 1 · guessed £40k", "off by £60k"]),
                        ph("Again", "Next guess is closer.", 2400, at=0, center="£85k", sub="guess", lines=["try 1 · off by £60k", "try 2 · guessed £85k"]),
                        ph("Closer", "Smaller gap, smaller nudge.", 2400, at=1, center="−£15k", sub="closer", lines=["try 1 · off by £60k", "try 2 · off by £15k"]),
                        ph("Nearly", "After many rounds the guesses land close to the truth.", 3200, at=0, center="£99k", sub="nearly there", lines=["try 1 · off by £60k", "try 2 · off by £15k", c("try 3 · off by £1k", "good")]),
                    ],
                    log="training log",
                ),
                "Picture 1 · guess, measure, nudge",
                "The loop at the heart of it",
                "Every model you have heard of was trained with this loop. The scale changes (billions of examples, thousands of chips, weeks of time) but the moves do not: guess, measure the error, adjust, repeat.",
                "The nudges are small on purpose. Big jumps overshoot and bounce around. Small ones add up to a smooth path downhill towards fewer mistakes.",
            ),
            part(
                bars(
                    ["step 1", "step 100", "step 1,000", "step 10,000", "step 100,000"],
                    [
                        ph("Start", "At the start, the error is huge.", 2200, values=[95, None, None, None, None], pick=0),
                        ph("Early", "It drops fast at first: the easy patterns are learned quickly.", 2200, values=[95, 60, None, None, None], pick=1),
                        ph("Middle", "Then more slowly.", 2200, values=[95, 60, 35, None, None], pick=2),
                        ph("Late", "Each extra bit of improvement takes far longer.", 2200, values=[95, 60, 35, 22, None], pick=3),
                        ph("Settle", "Eventually it levels off.", 3000, values=[95, 60, 35, 22, 18], pick=4, foot="Lower is better. This curve is what people watch during training."),
                    ],
                    title="loss: how wrong the model is", unit="",
                ),
                "Picture 2 · the loss goes down",
                "Watching it learn",
                "Training is tracked with a loss curve like this. A falling curve means the model is learning. A flat one means it has stopped. One that goes back up means something is wrong.",
            ),
            part(
                compare(
                    "Learned the pattern", "Memorised the examples",
                    [
                        ph("Practice", "Two models score perfectly on their practice questions.", 2800, l=[c("practice questions", v="98%")], r=[c("practice questions", v="100%")]),
                        ph("New", "Now test them on questions neither has seen.", 2800, l=[c("practice questions", v="98%"), c("new questions", v="94%")], r=[c("practice questions", v="100%"), c("new questions", v="51%")]),
                        ph("Verdict", "The second one memorised the answers instead of learning the idea. This is called overfitting.", 3600, l=[c("practice questions", v="98%"), c("new questions", "good", v="94%")], r=[c("practice questions", v="100%"), c("new questions", "bad", v="51%")], win="l"),
                    ],
                ),
                "Picture 3 · learning versus memorising",
                "Always test on fresh examples",
                "A student who memorises last year's exam answers can ace the practice paper and fail the real one. Models do the same thing. That is why some examples are always held back and never used for training. They are the only honest test.",
            ),
        ],
        "Training is guess, measure, nudge, repeated millions of times, then tested on examples the model never saw.",
        "loss gradient descent overfitting backpropagation learning",
    ),
    topic(
        "large-language-models", "Large language models", "Models",
        "A neural network trained on a huge pile of text to do one thing: predict the next piece of text. Chat, code and summaries all grow out of that.",
        "An LLM is a next-word predictor that got so good at the game it picked up a great deal about the world along the way.",
        "A large language model, or LLM, is a very big neural network that has read an enormous amount of text: books, websites, code and conversations. During training it played one game billions of times. Hide the next word, guess it, check, adjust. To get really good at that game it had to pick up grammar, facts, writing styles and even some reasoning, because all of those help predict what comes next. \"Large\" refers to the number of weights, often billions. When you chat with one, it is still playing the same game. It reads your message and keeps predicting what a helpful reply would say next, one small piece at a time, until the reply is finished.",
        [
            part(
                chips([
                    ph("Game", "During training, the model sees a sentence with the next word hidden.", 2800, rows=[row("training text", [c("The"), c("cat"), c("sat"), c("on"), c("the"), c("?", "gap")])]),
                    ph("Guess", "It guesses. Then it checks the real word and adjusts.", 3000, rows=[row("training text", [c("The"), c("cat"), c("sat"), c("on"), c("the"), c("mat", "hot")])], out="Guessed 'mat'. Correct, so reinforce.", outCap="check"),
                    ph("Facts", "To win this game on billions of sentences, it has to soak up facts as well.", 3200, rows=[row("training text", [c("The"), c("capital"), c("of"), c("Japan"), c("is"), c("?", "gap")])]),
                    ph("Learned", "Predicting well means knowing that the answer is Tokyo.", 3200, rows=[row("training text", [c("The"), c("capital"), c("of"), c("Japan"), c("is"), c("Tokyo", "hot")])], out="Knowledge emerges from prediction.", outCap="why it matters"),
                ]),
                "Picture 1 · the next-word game",
                "One simple game",
                "It sounds too simple to produce anything clever, but think about what perfect prediction would need. To finish \"the capital of Japan is\", you need geography. To finish a line of code, you need to understand the program. Prediction at scale quietly forces a lot of learning.",
            ),
            part(
                flow(
                    [("Your message", "text"), ("Tokens", "small pieces"), ("Network", "billions of weights"), ("Next token", "one piece"), ("Reply", "grows")],
                    [
                        ph("Message", "You type a question.", 2400, at=0, packet="Why is the sky blue?"),
                        ph("Tokens", "It is chopped into tokens, small chunks of text.", 2400, at=1, packet="Why · is · the · sky · blue · ?"),
                        ph("Network", "The network reads them all and scores every possible next token.", 2600, at=2, packet="scoring…"),
                        ph("Pick", "One token is chosen.", 2400, at=3, packet="Sunlight"),
                        ph("Repeat", "It is added to the reply, and the whole thing runs again for the next token.", 3200, at=4, packet="Sunlight scatters…", say="One token at a time, until the reply is done."),
                    ],
                ),
                "Picture 2 · from your message to its reply",
                "Chatting is the same game",
                "When you chat, the model is still predicting. Your message plus its reply so far is the text; it predicts what a helpful assistant would write next. Extra training (see fine-tuning and RLHF) is what makes those predictions helpful rather than just plausible.",
            ),
            part(
                bars(
                    ["GPT-1 · 2018", "GPT-2 · 2019", "GPT-3 · 2020"],
                    [
                        ph("2018", "OpenAI's first GPT had about 0.1 billion weights.", 2400, values=[0.12, None, None], pick=0),
                        ph("2019", "GPT-2 had 1.5 billion.", 2400, values=[0.12, 1.5, None], pick=1),
                        ph("2020", "GPT-3 jumped to 175 billion, and suddenly could do tasks nobody trained it for.", 3400, values=[0.12, 1.5, 175], pick=2, foot="Bigger models, trained on more text, kept getting better at the same game."),
                    ],
                    title="weights, in billions", unit="B", max=175,
                ),
                "Picture 3 · why they are called large",
                "Size changed what they could do",
                "The surprise of the last few years was that simply scaling up, more weights and more text, kept unlocking new abilities. Translation, summarising and writing code were never separate features. They appeared as the models grew.",
            ),
        ],
        "An LLM predicts the next piece of text. Doing that well, at huge scale, is what makes it seem to understand.",
        "llm gpt claude gemini chatgpt language model parameters",
    ),
    topic(
        "tokens", "Tokens", "Models",
        "Models do not read letters or words. They read tokens: common chunks of text, each turned into a number. Prices, limits and odd mistakes all come from this.",
        "Before a model reads anything, the text is chopped into tokens. That one step explains a surprising amount of model behaviour.",
        "A model cannot read text the way you do. First the text is chopped into pieces called tokens. A token is often a whole common word like \"the\", a piece of a longer word like \"un\" + \"believ\" + \"able\", or a bit of punctuation. Each token has an ID number from a fixed list called the vocabulary, and the model only ever sees those numbers. In English, one token is roughly three quarters of a word. This matters more than it sounds. You pay per token. Context windows are measured in tokens. And because the model sees chunks rather than letters, simple-looking jobs like counting the r's in \"strawberry\" can trip it up.",
        [
            part(
                chips([
                    ph("Text", "You see a word.", 2400, rows=[row("what you type", [c("unbelievable!")])]),
                    ph("Split", "The tokenizer splits it into common chunks.", 2800, rows=[row("what you type", [c("unbelievable!")]), row("tokens", [c("un", "hot"), c("believ", "hot"), c("able", "hot"), c("!", "hot")])]),
                    ph("Numbers", "Each chunk is swapped for its ID number.", 3000, rows=[row("what you type", [c("unbelievable!")]), row("tokens", [c("un", n=403), c("believ", n=6593), c("able", n=481), c("!", n=0)])]),
                    ph("Model", "The model only ever sees the numbers, never the letters.", 3200, rows=[row("tokens (example IDs)", [c("un", n=403), c("believ", n=6593), c("able", n=481), c("!", n=0)])], out="403 · 6593 · 481 · 0", outCap="what the model reads"),
                ]),
                "Picture 1 · text becomes tokens, tokens become numbers",
                "Chunks, not letters",
                "Common words get their own token. Rare words are built from pieces. That keeps the vocabulary to a manageable size, tens of thousands of entries, while still covering any text, including typos and new words.",
            ),
            part(
                compare(
                    "What you see", "What the model sees",
                    [
                        ph("Word", "Same word, two views.", 2400, l=[c("strawberry")], r=[c("str"), c("aw"), c("berry")]),
                        ph("Ask", "Ask how many r's it has.", 2600, l=[c("strawberry"), c("how many r's?")], r=[c("str"), c("aw"), c("berry"), c("how many r's?")]),
                        ph("Answer", "You count letters. The model sees three chunks with the letters hidden inside, so it can miscount.", 3600, l=[c("strawberry"), c("how many r's?"), c("count them: 3", "good")], r=[c("str"), c("aw"), c("berry"), c("how many r's?"), c("letters hidden in chunks", "bad")], win="l"),
                    ],
                ),
                "Picture 2 · why spelling questions can trip a model up",
                "Odd mistakes, explained",
                "Tasks about individual letters (spelling, counting, reversing words) are harder for models than they look, because letters are not what they read. Newer models often get these right by reasoning step by step, but the root cause is tokens.",
                "Splits shown here are illustrative. Each model family has its own tokenizer and splits differently.",
            ),
            part(
                bars(
                    ["instructions", "chat so far", "attached document", "the answer"],
                    [
                        ph("Prompt", "Everything you send is counted in tokens.", 2400, values=[300, None, None, None], pick=0),
                        ph("History", "So is the conversation so far.", 2400, values=[300, 800, None, None], pick=1),
                        ph("Docs", "And any document you paste in.", 2400, values=[300, 800, 1500, None], pick=2),
                        ph("Answer", "And the reply. Add it up and that is what you pay for, and what has to fit in the window.", 3400, values=[300, 800, 1500, 400], pick=3, foot="3,000 tokens in total, roughly 2,250 words."),
                    ],
                    title="tokens used in one request", unit="", max=1500,
                ),
                "Picture 3 · tokens are the unit of cost and size",
                "Why it matters day to day",
                "Pricing is per million tokens. Context windows are a number of tokens. Speed is tokens per second. When people talk about a model being expensive or running out of room, tokens are the unit they mean.",
            ),
        ],
        "Models read tokens, not words, and limits, speed and cost are all counted in them.",
        "tokenizer vocabulary token count cost subword",
    ),
    topic(
        "how-an-llm-writes", "How an LLM writes", "Models",
        "The model never fetches a finished sentence. It scores every possible next token, picks one, appends it, and starts again.",
        "A language model does not look up an answer. It predicts the next token from the ones already there, one token at a time.",
        "Think of the predictive text on your phone, the three suggested words above the keyboard, but enormously smarter. When a language model writes, it looks at everything written so far and gives every possible next token a score: how likely is this to come next? \"hold\" might get 42 percent, \"be\" 21 percent, and thousands of others almost nothing. One token is picked, usually a likely one, and added to the end. Then the whole process runs again with that new token included. A paragraph is hundreds of these tiny choices in a row. Nothing is stored as a finished sentence. That is why the same question can get different answers, and why a sentence can sound confident without being checked.",
        [
            part(
                "llm",
                "Picture 1 · score, pick, append",
                "Score, pick, append",
                "Text is split into tokens: whole words, pieces of words, punctuation. \"The number has to\" is a handful of tokens, and that is all the model has to go on.",
                "For the next position the model scores every token it knows. \"hold\" gets 42 percent, \"be\" 21, \"stay\" 11, and a long tail gets almost nothing. One token is picked, it is appended, the scores are thrown away, and the prediction runs again.",
            ),
            part(
                cycle(
                    ["Read", "Score", "Pick", "Append"],
                    [
                        ph("Read", "The model reads everything so far.", 2200, at=0, center="read", sub="all tokens so far", lines=["The number has to"]),
                        ph("Score", "Every possible next token gets a probability.", 2200, at=1, center="42%", sub="'hold' is likeliest"),
                        ph("Pick", "One is chosen.", 2200, at=2, center="hold", sub="picked"),
                        ph("Append", "It is added on, and the loop starts again.", 2400, at=3, center="+1", sub="token added", lines=["The number has to", "The number has to hold"]),
                        ph("Again", "Read, score, pick, append, for every single token.", 3000, at=2, center="up", sub="next pick", lines=["The number has to", "The number has to hold", c("The number has to hold up", "good")]),
                    ],
                    log="the sentence so far",
                ),
                "Picture 2 · the loop behind every reply",
                "A loop, not a lookup",
                "Every reply you have ever had from a chatbot was produced by this loop. A 500-word answer is roughly 650 trips round it. Each trip reads everything, including the tokens the model itself just wrote.",
                "This is why long answers can drift. An early odd choice becomes part of the text that every later choice is based on.",
            ),
            part(
                bars(
                    ["hold", "be", "stay", "add", "everything else"],
                    [
                        ph("Scores", "For one position, these are the chances of each next token.", 3000, values=[42, 21, 11, 6, 20]),
                        ph("Usually", "Most of the time the top one wins.", 2600, values=[42, 21, 11, 6, 20], pick=0, foot="Picked: 'hold'"),
                        ph("Sometimes", "But a less likely one can be picked too. That is why the same prompt can give different replies.", 3600, values=[42, 21, 11, 6, 20], pick=1, foot="Picked: 'be'. Same question, a different sentence from here on."),
                    ],
                    title="next-token probabilities",
                ),
                "Picture 3 · why answers vary",
                "Why this matters",
                "There is no stored sentence called \"The number has to hold up.\" It was built one choice at a time. A confident sentence is just a run of likely tokens, not a checked fact. If you need a fact, give it to the model in the context or let it call a tool.",
            ),
        ],
        "An LLM writes by predicting one token at a time. Each choice is likely, not verified.",
        "next token prediction generation sampling autoregressive probability",
    ),
    topic(
        "attention", "Attention", "Models",
        "When a model reads a word, attention lets it look back at every other word and decide which ones matter for understanding this one.",
        "Attention is how a model works out which words relate to which. It is the core idea inside every modern LLM.",
        "Read this: \"The trophy didn't fit in the suitcase because it was too big.\" What does \"it\" mean? You know instantly that it is the trophy, because you glanced back at the other words and weighed them up. Attention is the model doing the same thing. For every token, it asks: which other tokens should I focus on right now? It gives each one a score, pays most attention to the high scorers, and blends their meaning into the current word. Change \"big\" to \"small\" and the focus shifts to \"suitcase\". This idea, introduced in 2017 in a design called the Transformer (the T in GPT), is the engine inside every modern language model.",
        [
            part(
                bars(
                    ["The", "trophy", "fit", "suitcase", "too big"],
                    [
                        ph("Look", "The model is reading the word 'it'. It looks back at every earlier word.", 2800, values=[2, 2, 2, 2, 2]),
                        ph("Big", "In '…because it was too big', most attention goes to 'trophy'.", 3400, values=[3, 62, 8, 17, 10], pick=1, foot="'it' = the trophy"),
                        ph("Small", "Change one word to 'too small' and the focus jumps to 'suitcase'.", 3600, items=["The", "trophy", "fit", "suitcase", "too small"], values=[3, 14, 9, 64, 10], pick=3, foot="'it' = the suitcase"),
                    ],
                    title="how much 'it' attends to each word",
                ),
                "Picture 1 · what does 'it' refer to?",
                "Looking back with a purpose",
                "Words get their meaning from other words. \"Bank\" means something different next to \"river\" than next to \"loan\". Attention lets every token pull in meaning from exactly the tokens that matter, wherever they are in the text.",
            ),
            part(
                grid(
                    ["The", "cat", "sat", "on", "mat"], ["The", "cat", "sat", "on", "mat"],
                    [
                        ph("Grid", "Every word looks at every word. That makes a grid of attention scores.", 2600, cap="rows: the word reading · columns: the word looked at", cells=[[0.1] * 5 for _ in range(5)]),
                        ph("cat", "'cat' mostly attends to itself and 'The'.", 2600, cap="row: cat", focus=1, colHot=[0, 1], cells=[[0.8, 0.1, 0, 0, 0], [0.5, 0.7, 0.1, 0, 0], [0.1, 0.7, 0.4, 0.1, 0], [0, 0.1, 0.6, 0.4, 0.2], [0.2, 0.3, 0.3, 0.4, 0.6]]),
                        ph("sat", "'sat' looks hard at 'cat': who did the sitting?", 2600, cap="row: sat", focus=2, colHot=[1], cells=[[0.8, 0.1, 0, 0, 0], [0.5, 0.7, 0.1, 0, 0], [0.1, 0.8, 0.4, 0.1, 0], [0, 0.1, 0.6, 0.4, 0.2], [0.2, 0.3, 0.3, 0.4, 0.6]]),
                        ph("mat", "'mat' spreads its attention across 'sat on': where was the sitting?", 3200, cap="row: mat", focus=4, colHot=[2, 3, 4], cells=[[0.8, 0.1, 0, 0, 0], [0.5, 0.7, 0.1, 0, 0], [0.1, 0.8, 0.4, 0.1, 0], [0, 0.1, 0.6, 0.4, 0.2], [0.1, 0.3, 0.5, 0.6, 0.7]]),
                    ],
                ),
                "Picture 2 · every word looks at every word",
                "A grid of relationships",
                "Inside the model, attention runs as a grid: each row is one word deciding where to look. Real models run dozens of these grids side by side (called heads) in every layer, each free to track a different kind of relationship: grammar, references, topic.",
                "The grid grows with the square of the text length. Double the text and there are four times as many scores to compute. That is one reason long context windows are expensive.",
            ),
            part(
                compare(
                    "Reading one word at a time", "Attention",
                    [
                        ph("Old", "Older models read in order and carried a running memory.", 3000, l=[c("word 1 → word 2 → … → word 50"), c("early words fade", "bad")]),
                        ph("New", "Attention lets every word see every other word directly.", 3000, l=[c("word 1 → word 2 → … → word 50"), c("early words fade", "bad")], r=[c("every word sees every word"), c("distance does not matter", "good")]),
                        ph("Fast", "And all of it can be computed at once, which suits modern chips.", 3400, l=[c("word 1 → word 2 → … → word 50"), c("early words fade", "bad"), c("one step after another")], r=[c("every word sees every word"), c("distance does not matter", "good"), c("all computed in parallel", "good")], win="r"),
                    ],
                ),
                "Picture 3 · why attention changed everything",
                "The idea that unlocked LLMs",
                "Before attention, models struggled to connect words far apart, and training was slow because each step waited for the last. Attention fixed both. That is why one 2017 paper, \"Attention Is All You Need\", sits underneath almost everything in this notebook.",
            ),
        ],
        "Attention lets each word look at all the others and borrow meaning from the ones that matter.",
        "transformer self-attention heads query key value context",
    ),
]
