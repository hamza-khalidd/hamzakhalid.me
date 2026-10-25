const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
let pending = [];

function later(fn, ms) {
  const list = pending;
  list.push(
    window.setTimeout(() => {
      pending = list;
      fn();
    }, reduce ? 0 : ms)
  );
}

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function place(node, x, y) {
  node.style.left = x + "%";
  node.style.top = y + "%";
  return node;
}

const scenes = {
  loop: {
    rounds: 3,
    roundLabel: "Pass",
    phases: [
      { label: "Goal", note: "The agent holds the outcome: a weekly loss report. The route there is not fixed." },
      { label: "Plan", note: "It picks only the next step on the list, based on what it knows so far." },
      { label: "Act", note: "It does that one step: runs a query, calls a tool, or writes a draft." },
      { label: "Observe", note: "It checks the result against the goal. Gap left, loop again. Goal met, stop." },
    ],
    build(root) {
      const tasks = ["Pull last 7 days", "Find the gaps", "Draft the report"];
      const ring = el("div", "lp-ring");
      ring.innerHTML =
        '<svg viewBox="0 0 100 100" aria-hidden="true"><circle class="lp-track" cx="50" cy="50" r="34"></circle><circle class="lp-flow" cx="50" cy="50" r="34"></circle></svg>';
      const arm = el("div", "lp-arm");
      arm.appendChild(el("span", "lp-dot"));
      ring.appendChild(arm);
      const middle = el("div", "lp-mid");
      const passName = el("span", "", "pass");
      const passNum = el("strong", "", "1");
      middle.append(passName, passNum);
      ring.appendChild(middle);
      const spots = [
        [50, 16],
        [84, 50],
        [50, 84],
        [16, 50],
      ];
      const nodes = this.phases.map((phase, index) =>
        ring.appendChild(place(el("span", "lp-node", phase.label), spots[index][0], spots[index][1]))
      );

      const card = el("div", "lp-card");
      card.append(el("span", "lp-kicker", "Goal"), el("strong", "", "Weekly loss report"));
      const list = el("ul", "lp-list");
      const items = tasks.map((task) => {
        const item = el("li");
        item.append(el("i", "lp-box"), el("span", "", task));
        list.appendChild(item);
        return item;
      });
      const bar = el("div", "lp-bar");
      const fill = el("i");
      bar.appendChild(fill);
      const status = el("span", "lp-status");
      card.append(list, bar, status);
      root.append(ring, card);

      let spin = 0;
      let last = 0;
      return (phase, round) => {
        spin += (phase - last + 4) % 4;
        last = phase;
        arm.style.transform = "rotate(" + spin * 90 + "deg)";
        nodes.forEach((node, index) => node.classList.toggle("is-hot", index === phase));
        passNum.textContent = String(round + 1);
        card.classList.toggle("is-goal", phase === 0);

        let done = 0;
        items.forEach((item, index) => {
          const isDone = index < round || (index === round && phase === 3);
          if (isDone) done += 1;
          item.classList.toggle("is-done", isDone);
          item.classList.toggle("is-next", index === round && (phase === 1 || phase === 2));
          item.classList.toggle("is-run", index === round && phase === 2);
        });
        fill.style.width = (done / tasks.length) * 100 + "%";
        const finished = done === tasks.length;
        card.classList.toggle("is-met", finished);
        if (finished) status.textContent = "Goal met. Stop.";
        else if (phase === 3) status.textContent = "Gap left. Loop again.";
        else status.textContent = done + " of " + tasks.length + " done";
      };
    },
  },

  orch: {
    rounds: 1,
    phases: [
      { label: "Brief", note: "One brief arrives. Only the orchestrator sees the whole question." },
      { label: "Split", note: "It cuts the brief into tasks and sends each one to a specialist." },
      { label: "Work", note: "The specialists work in parallel, each on their own piece only.", ms: 3000 },
      { label: "Merge", note: "Results go back to the orchestrator, not to each other." },
      { label: "Answer", note: "The orchestrator stitches the pieces into one answer." },
    ],
    build(root) {
      const hub = [50, 26];
      const workers = [
        { name: "Search", task: "policy docs", result: "3 docs", x: 17, y: 76, ms: 700 },
        { name: "SQL", task: "loss by site", result: "2 rows", x: 50, y: 76, ms: 1500 },
        { name: "Chart", task: "weekly trend", result: "1 chart", x: 83, y: 76, ms: 2200 },
      ];
      const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("viewBox", "0 0 100 100");
      svg.setAttribute("preserveAspectRatio", "none");
      svg.setAttribute("class", "or-lines");
      const lines = workers.map((worker) => {
        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", hub[0]);
        line.setAttribute("y1", hub[1]);
        line.setAttribute("x2", worker.x);
        line.setAttribute("y2", worker.y);
        line.setAttribute("vector-effect", "non-scaling-stroke");
        svg.appendChild(line);
        return line;
      });
      root.appendChild(svg);

      const brief = place(el("span", "or-chip or-brief", "Why did losses rise?"), 14, hub[1]);
      const answer = place(el("span", "or-chip or-answer", "2 sites, meter drift"), 86, hub[1]);
      const center = place(el("div", "or-hub"), hub[0], hub[1]);
      const hubName = el("strong", "", "Orchestrator");
      const hubState = el("span", "", "waiting");
      center.append(hubName, hubState);
      root.append(brief, answer, center);

      const cards = workers.map((worker) => {
        const card = place(el("div", "or-worker"), worker.x, worker.y);
        const state = el("span", "or-state");
        const sub = el("span", "or-sub", worker.task);
        card.append(state, el("strong", "", worker.name), sub);
        root.appendChild(card);
        const packet = place(el("span", "or-packet"), hub[0], hub[1]);
        root.appendChild(packet);
        return { card, sub, packet, worker };
      });

      return (phase) => {
        brief.classList.toggle("is-in", phase === 0);
        answer.classList.toggle("is-in", phase === 4);
        center.classList.toggle("is-busy", phase === 0 || phase === 3);
        hubState.textContent = ["reading brief", "splitting", "waiting on 3", "merging", "done"][phase];
        lines.forEach((line) => {
          line.classList.toggle("is-down", phase === 1);
          line.classList.toggle("is-up", phase === 3);
          line.classList.toggle("is-on", phase >= 1 && phase <= 3);
        });
        cards.forEach(({ card, sub, packet, worker }) => {
          const atWorker = phase === 1 || phase === 2;
          place(packet, atWorker ? worker.x : hub[0], atWorker ? worker.y : hub[1]);
          packet.classList.toggle("is-shown", phase >= 1 && phase <= 3);
          packet.classList.toggle("is-result", phase === 3);
          card.classList.toggle("is-tasked", phase >= 1);
          card.classList.remove("is-run", "is-done");
          sub.textContent = phase >= 3 ? worker.result : worker.task;
          if (phase === 2) {
            card.classList.add("is-run");
            later(() => {
              card.classList.remove("is-run");
              card.classList.add("is-done");
              sub.textContent = worker.result;
            }, worker.ms);
          }
          if (phase >= 3) card.classList.add("is-done");
        });
      };
    },
  },

  sql: {
    rounds: 1,
    phases: [
      { label: "Ask", note: "A person asks in plain English. Nothing has touched the database yet." },
      { label: "Write", note: "The model translates the question into SQL against a real table.", ms: 2800 },
      { label: "Run", note: "The database runs it. WHERE keeps week 42; everything else is skipped.", ms: 2800 },
      { label: "Rows", note: "GROUP BY adds up each site. These rows are facts from the table, not a guess." },
    ],
    build(root) {
      const code = [
        "SELECT site, SUM(litres) AS lost",
        "FROM fuel_losses",
        "WHERE week = 42",
        "GROUP BY site",
        "ORDER BY lost DESC;",
      ];
      const data = [
        ["E14-02", "42", "260"],
        ["N1-18", "42", "180"],
        ["SW3-07", "41", "300"],
        ["E14-02", "42", "160"],
        ["N1-18", "42", "80"],
      ];
      const left = el("div", "sq-left");
      const ask = el("div", "sq-ask", "Which sites lost the most fuel this week?");
      const box = el("pre", "sq-code");
      const codeLines = code.map((line) => box.appendChild(el("span", "", "")));
      left.append(ask, box);

      const right = el("div", "sq-right");
      const table = el("div", "sq-table");
      table.appendChild(el("span", "sq-cap", "fuel_losses"));
      const head = el("div", "sq-row sq-head");
      ["site", "week", "litres"].forEach((name) => head.appendChild(el("span", "", name)));
      table.appendChild(head);
      const rows = data.map((cells) => {
        const row = el("div", "sq-row");
        cells.forEach((cell) => row.appendChild(el("span", "", cell)));
        table.appendChild(row);
        return row;
      });
      const scan = el("i", "sq-scan");
      table.appendChild(scan);

      const result = el("div", "sq-table sq-result");
      result.appendChild(el("span", "sq-cap", "result · 2 rows"));
      const resultHead = el("div", "sq-row sq-head");
      ["site", "sum", "lost"].forEach((name) => resultHead.appendChild(el("span", "", name)));
      result.appendChild(resultHead);
      const sums = [
        ["E14-02", "260 + 160", "420"],
        ["N1-18", "180 + 80", "260"],
      ].map((cells) => {
        const row = el("div", "sq-row");
        cells.forEach((cell) => row.appendChild(el("span", "", cell)));
        result.appendChild(row);
        return row;
      });
      right.append(table, result);
      root.append(left, right);

      return (phase) => {
        ask.classList.toggle("is-hot", phase === 0);
        box.classList.toggle("is-on", phase >= 1);
        codeLines.forEach((line, index) => {
          line.textContent = phase >= 2 ? code[index] : "";
          line.classList.toggle("is-hot", phase === 2 && index === 2);
        });
        if (phase === 1) {
          let at = 0;
          code.forEach((line, index) => {
            for (let char = 1; char <= line.length; char += 1) {
              at += 22;
              later(() => {
                codeLines[index].textContent = line.slice(0, char);
              }, at);
            }
            at += 120;
          });
        }

        table.classList.toggle("is-gone", phase === 3);
        result.classList.toggle("is-in", phase === 3);
        table.classList.toggle("is-scan", phase === 2);
        rows.forEach((row, index) => {
          row.classList.remove("is-match", "is-skip");
          if (phase === 2) {
            later(() => row.classList.add(data[index][1] === "42" ? "is-match" : "is-skip"), 300 + index * 330);
          }
        });
        sums.forEach((row, index) => {
          row.classList.remove("is-in");
          if (phase === 3) later(() => row.classList.add("is-in"), 250 + index * 300);
        });
      };
    },
  },

  llm: {
    rounds: 3,
    roundLabel: "Token",
    phases: [
      { label: "Predict", note: "The model reads every token so far and scores what could come next." },
      { label: "Pick", note: "It picks one token, usually a likely one. There is no finished sentence to fetch." },
      { label: "Append", note: "That token joins the context, and the whole prediction runs again." },
    ],
    build(root) {
      const base = ["The", "number", "has", "to"];
      const steps = [
        [["hold", 42], ["be", 21], ["stay", 11], ["go", 6]],
        [["up", 58], ["steady", 17], ["true", 9], [",", 5]],
        [[".", 47], ["under", 22], ["today", 12], ["again", 6]],
      ];
      const top = el("div", "lm-context");
      top.appendChild(el("span", "lm-cap", "Context"));
      const sentence = el("div", "lm-sentence");
      top.appendChild(sentence);

      const scores = el("div", "lm-scores");
      scores.appendChild(el("span", "lm-cap", "Next-token scores"));
      const bars = [0, 1, 2, 3].map(() => {
        const row = el("div", "lm-row");
        const name = el("span", "lm-tok");
        const track = el("span", "lm-track");
        const fill = el("i");
        track.appendChild(fill);
        const pct = el("span", "lm-pct");
        row.append(name, track, pct);
        scores.appendChild(row);
        return { row, name, fill, pct };
      });
      root.append(top, scores);

      return (phase, round) => {
        const written = base.concat(steps.slice(0, round + (phase === 2 ? 1 : 0)).map((step) => step[0][0]));
        sentence.replaceChildren();
        written.forEach((word, index) => {
          const chip = el("span", "lm-word", word);
          if (phase === 2 && index === written.length - 1) chip.classList.add("is-new");
          sentence.appendChild(chip);
        });
        sentence.appendChild(el("span", "lm-caret"));

        steps[round].forEach(([word, value], index) => {
          const bar = bars[index];
          bar.name.textContent = word;
          bar.pct.textContent = value + "%";
          bar.row.classList.toggle("is-pick", phase >= 1 && index === 0);
          bar.row.classList.toggle("is-dim", phase >= 1 && index > 0);
          scores.classList.toggle("is-spent", phase === 2);
          if (phase === 0) {
            bar.fill.style.transition = "none";
            bar.fill.style.width = "0%";
            void bar.fill.offsetWidth;
            bar.fill.style.transition = "";
            later(() => {
              bar.fill.style.width = value + "%";
            }, 120 + index * 140);
          } else {
            bar.fill.style.width = value + "%";
          }
        });
      };
    },
  },

  embed: {
    rounds: 1,
    phases: [
      { label: "Words", note: "Words start as text. A model cannot measure the distance between two strings." },
      { label: "Embed", note: "Each word becomes a point. Words used in similar ways land close together.", ms: 2800 },
      { label: "Query", note: "A new word is embedded the same way. It has never been seen in this list." },
      { label: "Nearest", note: "The closest points are its meaning neighbours. Distance stands in for similarity.", ms: 3000 },
    ],
    build(root) {
      const plane = el("div", "em-plane");
      root.appendChild(plane);
      const words = [
        ["diesel", 12, 26, "a"], ["petrol", 30, 12, "a"], ["fuel", 16, 56, "a"],
        ["cost", 70, 16, "b"], ["price", 88, 30, "b"], ["spend", 72, 44, "b"],
        ["site", 34, 82, "c"], ["station", 54, 72, "c"], ["depot", 66, 88, "c"],
      ];
      const query = { word: "gasoline", x: 38, y: 38 };
      const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("viewBox", "0 0 100 100");
      svg.setAttribute("preserveAspectRatio", "none");
      svg.setAttribute("class", "em-lines");
      plane.appendChild(svg);
      const points = words.map(([word, x, y, group], index) => {
        const point = el("span", "em-point em-" + group, word);
        point.dataset.x = x;
        point.dataset.y = y;
        point.dataset.startX = 8 + index * 10.5;
        plane.appendChild(point);
        return point;
      });
      const near = [0, 1, 2];
      const lines = near.map((index) => {
        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", query.x);
        line.setAttribute("y1", query.y);
        line.setAttribute("x2", words[index][1]);
        line.setAttribute("y2", words[index][2]);
        line.setAttribute("vector-effect", "non-scaling-stroke");
        svg.appendChild(line);
        return line;
      });
      const dists = ["0.08", "0.11", "0.14"].map((text, i) => {
        const tag = el("span", "em-dist", text);
        place(tag, (query.x + words[near[i]][1]) / 2, (query.y + words[near[i]][2]) / 2);
        plane.appendChild(tag);
        return tag;
      });
      const q = place(el("span", "em-point em-query", query.word), query.x, query.y);
      plane.appendChild(q);
      const legend = el("div", "em-legend");
      [["a", "fuel"], ["b", "money"], ["c", "places"]].forEach(([group, name]) => {
        const item = el("span", "em-key em-" + group);
        item.append(el("i"), document.createTextNode(name));
        legend.appendChild(item);
      });
      root.appendChild(legend);

      return (phase) => {
        points.forEach((point, index) => {
          const placed = phase >= 1;
          place(point, placed ? point.dataset.x : point.dataset.startX, placed ? point.dataset.y : 92);
          point.classList.toggle("is-placed", placed);
          point.classList.toggle("is-dim", phase === 3 && !near.includes(index));
          point.classList.toggle("is-near", phase === 3 && near.includes(index));
        });
        legend.classList.toggle("is-in", phase >= 1);
        q.classList.toggle("is-in", phase >= 2);
        lines.forEach((line, index) => {
          line.classList.remove("is-on");
          if (phase === 3) later(() => line.classList.add("is-on"), 200 + index * 250);
        });
        dists.forEach((tag, index) => {
          tag.classList.remove("is-in");
          if (phase === 3) later(() => tag.classList.add("is-in"), 450 + index * 250);
        });
      };
    },
  },

  rag: {
    rounds: 1,
    phases: [
      { label: "Ask", note: "The question arrives. The model alone would answer from memory." },
      { label: "Search", note: "The question is matched against stored chunks. Each gets a relevance score.", ms: 2800 },
      { label: "Pick", note: "Only the top chunks are kept. The rest never reach the model." },
      { label: "Answer", note: "The model answers from the chunks it was given, and can point back to them.", ms: 3000 },
    ],
    build(root) {
      const ask = el("div", "rg-ask", "What is the refund window?");
      const store = el("div", "rg-store");
      store.appendChild(el("span", "rg-cap", "document store"));
      const chunks = [
        ["Delivery takes 3 days", "0.21"],
        ["Refunds within 30 days", "0.92"],
        ["Opening hours 9 to 5", "0.08"],
        ["Refund needs a receipt", "0.81"],
        ["Fuel card terms", "0.33"],
      ].map(([text, score]) => {
        const chunk = el("div", "rg-chunk");
        const s = el("b", "", score);
        chunk.append(el("span", "", text), s);
        store.appendChild(chunk);
        return { chunk, score: Number(score) };
      });
      const prompt = el("div", "rg-prompt");
      prompt.appendChild(el("span", "rg-cap", "prompt"));
      const ctx1 = el("span", "rg-ctx", "[1] Refunds within 30 days");
      const ctx2 = el("span", "rg-ctx", "[2] Refund needs a receipt");
      const answer = el("p", "rg-answer", "30 days, with a receipt. [1][2]");
      prompt.append(ctx1, ctx2, answer);
      root.append(ask, store, prompt);

      return (phase) => {
        ask.classList.toggle("is-hot", phase === 0);
        store.classList.toggle("is-scan", phase === 1);
        chunks.forEach(({ chunk, score }, index) => {
          chunk.classList.remove("is-scored", "is-top", "is-out");
          if (phase === 1) later(() => chunk.classList.add("is-scored"), 250 + index * 300);
          if (phase >= 2) {
            chunk.classList.add("is-scored");
            chunk.classList.add(score > 0.5 ? "is-top" : "is-out");
          }
        });
        [ctx1, ctx2].forEach((ctx, index) => {
          ctx.classList.remove("is-in");
          if (phase === 2) later(() => ctx.classList.add("is-in"), 300 + index * 300);
          if (phase === 3) ctx.classList.add("is-in");
        });
        answer.classList.remove("is-in");
        if (phase === 3) later(() => answer.classList.add("is-in"), 400);
      };
    },
  },

  chunk: {
    rounds: 1,
    phases: [
      { label: "Document", note: "A long document is too big to search or send in one piece." },
      { label: "Split", note: "It is cut into chunks of a fixed size, measured in tokens." },
      { label: "Overlap", note: "Neighbouring chunks share a few lines, so a sentence on the cut is not lost." },
      { label: "Store", note: "Each chunk is stored on its own, ready to be embedded and searched.", ms: 2800 },
    ],
    build(root) {
      const doc = el("div", "ck-doc");
      doc.appendChild(el("span", "ck-cap", "policy.pdf"));
      const widths = [92, 80, 88, 70, 95, 84, 60, 90, 78, 86, 72, 66];
      const body = el("div", "ck-body");
      widths.forEach((width) => {
        const line = el("i", "ck-line");
        line.style.width = width + "%";
        body.appendChild(line);
      });
      doc.appendChild(body);
      const bands = [
        [0, 5],
        [4, 9],
        [8, 12],
      ].map(([from, to], index) => {
        const band = el("span", "ck-band ck-band-" + index);
        band.style.top = (from / 12) * 100 + "%";
        band.style.height = ((to - from) / 12) * 100 + "%";
        body.appendChild(band);
        return band;
      });
      const overlaps = [4, 8].map((row) => {
        const strip = el("span", "ck-overlap");
        strip.style.top = (row / 12) * 100 + "%";
        strip.style.height = (1 / 12) * 100 + "%";
        body.appendChild(strip);
        return strip;
      });
      const shelf = el("div", "ck-shelf");
      const cards = ["chunk 1 · 180 tokens", "chunk 2 · 180 tokens", "chunk 3 · 150 tokens"].map((text, index) => {
        const card = el("div", "ck-card ck-card-" + index);
        card.append(el("strong", "", text.split(" · ")[0]), el("span", "", text.split(" · ")[1]));
        shelf.appendChild(card);
        return card;
      });
      root.append(doc, shelf);

      return (phase) => {
        bands.forEach((band, index) => {
          band.classList.remove("is-in");
          if (phase >= 1) later(() => band.classList.add("is-in"), phase === 1 ? 200 + index * 350 : 0);
        });
        overlaps.forEach((strip) => strip.classList.toggle("is-in", phase >= 2));
        doc.classList.toggle("is-faded", phase === 3);
        cards.forEach((card, index) => {
          card.classList.remove("is-in");
          if (phase === 3) later(() => card.classList.add("is-in"), 200 + index * 300);
        });
      };
    },
  },

  tool: {
    rounds: 1,
    phases: [
      { label: "Ask", note: "The person asks something the model cannot know from training." },
      { label: "Call", note: "The model does not guess. It writes a structured call: tool name and arguments." },
      { label: "Run", note: "Your code runs the tool. The model never touches the system directly.", ms: 2600 },
      { label: "Answer", note: "The result goes back to the model, which turns it into a plain answer." },
    ],
    build(root) {
      const lanes = ["Person", "Model", "Tool"].map((name, index) => {
        const lane = el("div", "tl-lane");
        lane.style.left = 16 + index * 34 + "%";
        lane.appendChild(el("span", "tl-head", name));
        root.appendChild(lane);
        return lane;
      });
      const steps = [
        { cls: "tl-msg", text: "How much diesel is at E14-02?", from: 0, to: 1, y: 30 },
        { cls: "tl-msg tl-code", text: '{ "tool": "get_stock", "site": "E14-02" }', from: 1, to: 2, y: 50 },
        { cls: "tl-msg tl-code", text: '{ "diesel_l": 12400 }', from: 2, to: 1, y: 68 },
        { cls: "tl-msg", text: "12,400 litres of diesel.", from: 1, to: 0, y: 86 },
      ].map((step) => {
        const node = el("div", step.cls);
        const x = 16 + ((step.from + step.to) / 2) * 34;
        place(node, x, step.y);
        node.appendChild(el("span", "", step.text));
        const arrow = el("i", "tl-arrow" + (step.to < step.from ? " is-back" : ""));
        arrow.style.left = 16 + Math.min(step.from, step.to) * 34 + "%";
        arrow.style.width = Math.abs(step.to - step.from) * 34 + "%";
        arrow.style.top = step.y + 6.5 + "%";
        root.append(arrow, node);
        return { node, arrow };
      });
      const spin = el("span", "tl-spin");
      place(spin, 84, 59);
      root.appendChild(spin);

      return (phase) => {
        steps.forEach(({ node, arrow }, index) => {
          let shown = index <= phase;
          if (index === 2) shown = phase === 3;
          node.classList.toggle("is-in", shown);
          arrow.classList.toggle("is-in", shown);
          node.classList.toggle("is-hot", shown && (index === phase || (index === 2 && phase === 2)));
        });
        spin.classList.toggle("is-in", phase === 2);
        if (phase === 2) {
          later(() => {
            spin.classList.remove("is-in");
            steps[2].node.classList.add("is-in", "is-hot");
            steps[2].arrow.classList.add("is-in");
          }, 1300);
        }
      };
    },
  },

  window: {
    rounds: 1,
    phases: [
      { label: "Fill", note: "Every token the model reads goes into one fixed-size window.", ms: 2800 },
      { label: "Full", note: "The window has a hard limit. Here it holds six tokens." },
      { label: "Slide", note: "New tokens push the oldest ones out. They are not summarised. They are gone.", ms: 3000 },
      { label: "Lost", note: "Ask about something that fell out, and the model has nothing to read it from.", ms: 3000 },
    ],
    build(root) {
      const words = ["Site", "E14-02", "lost", "420", "litres", "this", "week", "after", "a", "fault"];
      const size = 6;
      const frame = el("div", "cw-frame");
      const count = el("span", "cw-count");
      const row = el("div", "cw-row");
      frame.append(row);
      const tray = el("div", "cw-tray");
      tray.appendChild(el("span", "cw-cap", "fell out"));
      const trayRow = el("div", "cw-tray-row");
      tray.appendChild(trayRow);
      const qa = el("div", "cw-qa");
      const q = el("span", "cw-q", "Which site lost fuel?");
      const a = el("span", "cw-a", "Not in the window.");
      qa.append(q, a);
      const top = el("div", "cw-top");
      top.append(el("span", "cw-cap", "context window"), count);
      root.append(top, frame, tray, qa);

      const draw = (visible, dropped, hotDropped) => {
        row.replaceChildren();
        visible.forEach((word, index) => {
          const chip = el("span", "cw-tok", word);
          if (index === visible.length - 1 && visible.length) chip.classList.add("is-new");
          row.appendChild(chip);
        });
        for (let i = visible.length; i < size; i += 1) row.appendChild(el("span", "cw-tok is-empty"));
        trayRow.replaceChildren();
        dropped.forEach((word) => {
          const chip = el("span", "cw-tok is-gone", word);
          if (hotDropped && word === "E14-02") chip.classList.add("is-hot");
          trayRow.appendChild(chip);
        });
        count.textContent = Math.min(visible.length, size) + " / " + size + " tokens";
        frame.classList.toggle("is-full", visible.length === size);
      };

      return (phase) => {
        qa.classList.toggle("is-in", phase === 3);
        if (phase === 0) {
          draw([], [], false);
          for (let i = 1; i <= size; i += 1) later(() => draw(words.slice(0, i), [], false), i * 330);
        } else if (phase === 1) {
          draw(words.slice(0, size), [], false);
        } else if (phase === 2) {
          draw(words.slice(0, size), [], false);
          for (let i = 1; i <= words.length - size; i += 1) {
            later(() => draw(words.slice(i, i + size), words.slice(0, i), false), i * 600);
          }
        } else {
          draw(words.slice(words.length - size), words.slice(0, words.length - size), true);
        }
      };
    },
  },

  temp: {
    rounds: 3,
    roundLabel: "Setting",
    phases: [
      { label: "Set", note: "Temperature reshapes the scores before a token is picked. Low sharpens, high flattens." },
      { label: "Sample", note: "Five draws from the same scores. Watch how much the picks spread.", ms: 3000 },
    ],
    build(root) {
      const tokens = ["hold", "be", "stay", "go", "remain"];
      const settings = [
        { t: "0.2", bars: [94, 4, 1, 1, 0], picks: [0, 0, 0, 0, 0] },
        { t: "1.0", bars: [48, 24, 14, 9, 5], picks: [0, 1, 0, 0, 2] },
        { t: "1.8", bars: [28, 22, 19, 16, 15], picks: [1, 3, 0, 4, 2] },
      ];
      const dial = el("div", "tp-dial");
      dial.appendChild(el("span", "tp-cap", "temperature"));
      const track = el("div", "tp-track");
      const knob = el("i", "tp-knob");
      track.appendChild(knob);
      const value = el("strong", "tp-value");
      dial.append(track, value);
      const chart = el("div", "tp-chart");
      const bars = tokens.map((word) => {
        const col = el("div", "tp-col");
        const bar = el("i", "tp-bar");
        const pct = el("span", "tp-pct");
        col.append(pct, bar, el("span", "tp-tok", word));
        chart.appendChild(col);
        return { bar, pct, col };
      });
      const draws = el("div", "tp-draws");
      draws.appendChild(el("span", "tp-cap", "5 draws"));
      const drawRow = el("div", "tp-draw-row");
      draws.appendChild(drawRow);
      root.append(dial, chart, draws);

      return (phase, round) => {
        const set = settings[round];
        knob.style.left = (Number(set.t) / 2) * 100 + "%";
        value.textContent = set.t;
        bars.forEach(({ bar, pct }, index) => {
          bar.style.height = Math.max(set.bars[index], 1) + "%";
          pct.textContent = set.bars[index] + "%";
        });
        drawRow.replaceChildren();
        if (phase === 1) {
          set.picks.forEach((pick, index) => {
            later(() => {
              drawRow.appendChild(el("span", "tp-pick" + (pick === 0 ? " is-top" : ""), tokens[pick]));
              bars[pick].col.classList.add("is-hit");
              later(() => bars[pick].col.classList.remove("is-hit"), 300);
            }, 250 + index * 420);
          });
        }
      };
    },
  },

  evals: {
    rounds: 1,
    phases: [
      { label: "Cases", note: "An eval is a fixed set of questions with known good answers." },
      { label: "Run v1", note: "The current prompt runs every case. Each answer is graded pass or fail.", ms: 2800 },
      { label: "Change", note: "One change to the prompt. Without the eval, this would be judged by feel." },
      { label: "Run v2", note: "Same cases, new prompt. The score moves, and one case that passed now fails.", ms: 3200 },
    ],
    build(root) {
      const cases = [
        ["Loss at E14-02 this week", 1, 1],
        ["Top site by spend", 0, 1],
        ["Refund window", 1, 1],
        ["Diesel stock, N1-18", 0, 1],
        ["Week-on-week change", 1, 0],
        ["Sites with no data", 0, 1],
      ];
      const table = el("div", "ev-table");
      const head = el("div", "ev-row ev-head");
      head.append(el("span", "", "case"), el("span", "", "v1"), el("span", "", "v2"));
      table.appendChild(head);
      const rows = cases.map(([text]) => {
        const row = el("div", "ev-row");
        const a = el("span", "ev-mark");
        const b = el("span", "ev-mark");
        row.append(el("span", "", text), a, b);
        table.appendChild(row);
        return { row, a, b };
      });
      const side = el("div", "ev-side");
      const change = el("div", "ev-change");
      change.append(el("span", "ev-cap", "prompt v2"), el("span", "", "+ always filter by week"));
      const score1 = el("div", "ev-score");
      const score2 = el("div", "ev-score");
      const mk = (box, name) => {
        const fill = el("i");
        const num = el("strong", "", "–");
        const track = el("span", "ev-track");
        track.appendChild(fill);
        box.append(el("span", "ev-cap", name), track, num);
        return { fill, num };
      };
      const s1 = mk(score1, "v1 score");
      const s2 = mk(score2, "v2 score");
      side.append(change, score1, score2);
      root.append(table, side);

      const mark = (node, ok) => {
        node.textContent = ok ? "✓" : "✗";
        node.className = "ev-mark is-in " + (ok ? "is-pass" : "is-fail");
      };
      return (phase) => {
        rows.forEach(({ row, a, b }, index) => {
          row.classList.toggle("is-in", true);
          a.className = "ev-mark";
          a.textContent = "";
          b.className = "ev-mark";
          b.textContent = "";
          row.classList.remove("is-regress");
          if (phase === 1) later(() => mark(a, cases[index][1]), 200 + index * 300);
          if (phase >= 2) mark(a, cases[index][1]);
          if (phase === 3) {
            later(() => {
              mark(b, cases[index][2]);
              if (cases[index][1] && !cases[index][2]) row.classList.add("is-regress");
            }, 200 + index * 300);
          }
        });
        change.classList.toggle("is-in", phase >= 2);
        s1.fill.style.width = phase >= 1 ? "50%" : "0%";
        s1.num.textContent = phase >= 1 ? "3 / 6" : "–";
        s2.fill.style.width = "0%";
        s2.num.textContent = "–";
        if (phase === 3) {
          later(() => {
            s2.fill.style.width = "83%";
            s2.num.textContent = "5 / 6";
          }, 2000);
        }
      };
    },
  },

  guard: {
    rounds: 3,
    roundLabel: "Request",
    phases: [
      { label: "Send", note: "A request heads for the model. Two checks sit on the path." },
      { label: "Input check", note: "Before the model: is this something it should see at all?" },
      { label: "Model", note: "The model only runs on what the input check let through." },
      { label: "Output check", note: "After the model: is the answer safe and supported before anyone reads it?" },
    ],
    build(root) {
      const stops = [
        { name: "Person", x: 8 },
        { name: "Input check", x: 33, gate: true },
        { name: "Model", x: 58 },
        { name: "Output check", x: 83, gate: true },
      ];
      const rail = el("i", "gd-rail");
      root.appendChild(rail);
      const nodes = stops.map((stop) => {
        const node = place(el("div", "gd-stop" + (stop.gate ? " is-gate" : "")), stop.x, 42);
        node.append(el("strong", "", stop.name), el("span", "gd-verdict"));
        root.appendChild(node);
        return node;
      });
      const packet = place(el("div", "gd-packet"), 8, 18);
      root.appendChild(packet);
      const result = el("div", "gd-result");
      root.appendChild(result);
      const runs = [
        { text: "Weekly loss for E14-02?", block: -1, out: "420 litres this week.", reply: "Delivered." },
        { text: "My card is 4929 1234…", block: 1, reason: "card number", reply: "Blocked at input. Card details removed." },
        { text: "Will losses double?", block: 3, reason: "not in source", draft: "Losses will double.", reply: "Replaced: no forecast in the data." },
      ];

      return (phase, round) => {
        const run = runs[round];
        const stopAt = run.block === -1 ? 3 : run.block;
        const at = Math.min(phase, stopAt);
        place(packet, stops[at].x, 18);
        packet.textContent = phase >= 2 && run.block !== 1 ? (run.draft || run.out) : run.text;
        packet.classList.toggle("is-blocked", run.block !== -1 && phase >= run.block);
        nodes.forEach((node, index) => {
          const verdict = node.querySelector(".gd-verdict");
          node.classList.remove("is-pass", "is-stop", "is-hot");
          verdict.textContent = "";
          if (index === at) node.classList.add("is-hot");
          if (!stops[index].gate || index > phase) return;
          if (index === run.block) {
            node.classList.add("is-stop");
            verdict.textContent = run.reason;
          } else if (index < stopAt || run.block === -1) {
            node.classList.add("is-pass");
            verdict.textContent = "pass";
          }
        });
        result.classList.remove("is-in", "is-bad");
        const ended = phase === 3 || (run.block === 1 && phase >= 1);
        if (ended) {
          result.textContent = run.reply;
          if (run.block !== -1) result.classList.add("is-bad");
          later(() => result.classList.add("is-in"), 450);
        }
      };
    },
  },
};

const svgNS = "http://www.w3.org/2000/svg";

function chipOf(item) {
  return typeof item === "string" ? { t: item } : item;
}

function classes(prefix, c) {
  return c ? " " + c.split(" ").map((name) => prefix + name).join(" ") : "";
}

const kinds = {
  flow(cfg) {
    return (root) => {
      const n = cfg.nodes.length;
      const xs = cfg.nodes.map((_, i) => (n === 1 ? 50 : 10 + (80 * i) / (n - 1)));
      root.appendChild(el("i", "fl-rail"));
      const nodes = cfg.nodes.map((node, i) => {
        const box = place(el("div", "fl-node"), xs[i], 48);
        box.appendChild(el("strong", "", node.t));
        if (node.s) box.appendChild(el("span", "", node.s));
        root.appendChild(box);
        return box;
      });
      const packet = place(el("span", "fl-packet"), xs[0], 18);
      const say = place(el("div", "fl-say"), xs[0], 80);
      root.append(packet, say);
      return (p) => {
        const ph = cfg.phases[p];
        const at = ph.at === undefined ? Math.min(p, n - 1) : ph.at;
        nodes.forEach((box, i) => {
          box.classList.toggle("is-hot", i === at);
          box.classList.toggle("is-past", i < at);
          box.classList.toggle("is-stop", ph.stop === i);
        });
        place(packet, xs[at], 18);
        packet.textContent = ph.packet || "";
        packet.classList.toggle("is-in", Boolean(ph.packet));
        packet.classList.toggle("is-bad", Boolean(ph.bad));
        say.classList.remove("is-in", "is-bad");
        if (ph.say) {
          say.textContent = ph.say;
          place(say, Math.min(Math.max(xs[at], 22), 78), 80);
          if (ph.bad) say.classList.add("is-bad");
          later(() => say.classList.add("is-in"), 380);
        }
      };
    };
  },

  seq(cfg) {
    return (root) => {
      const L = cfg.lanes.length;
      const xs = cfg.lanes.map((_, i) => (L === 1 ? 50 : 12 + (76 * i) / (L - 1)));
      cfg.lanes.forEach((name, i) => {
        const lane = el("div", "tl-lane");
        lane.style.left = xs[i] + "%";
        lane.appendChild(el("span", "tl-head", name));
        root.appendChild(lane);
      });
      const M = cfg.msgs.length;
      const ys = cfg.msgs.map((_, i) => 24 + (64 * i) / Math.max(M - 1, 1));
      const items = cfg.msgs.map((m, i) => {
        const a = Math.min(xs[m.f], xs[m.t]);
        const b = Math.max(xs[m.f], xs[m.t]);
        const arrow = el("i", "tl-arrow" + (m.t < m.f ? " is-back" : ""));
        arrow.style.left = a + "%";
        arrow.style.width = b - a + "%";
        arrow.style.top = ys[i] + 5.5 + "%";
        if (m.f === m.t) arrow.style.display = "none";
        const bubble = place(el("div", "tl-msg" + (m.code ? " tl-code" : "") + (m.bad ? " is-bad" : "")), (xs[m.f] + xs[m.t]) / 2, ys[i]);
        bubble.appendChild(el("span", "", m.text));
        root.append(arrow, bubble);
        return { arrow, bubble };
      });
      return (p) => {
        const ph = cfg.phases[p];
        const upto = ph.upto === undefined ? p : ph.upto;
        items.forEach(({ arrow, bubble }, i) => {
          arrow.classList.toggle("is-in", i <= upto);
          bubble.classList.toggle("is-in", i <= upto);
          bubble.classList.toggle("is-hot", i === upto);
        });
      };
    };
  },

  bars(cfg) {
    return (root) => {
      const wrap = el("div", "br-wrap");
      if (cfg.title) wrap.appendChild(el("span", "br-cap", cfg.title));
      const max = cfg.max || 100;
      const unit = cfg.unit === undefined ? "%" : cfg.unit;
      const rows = cfg.items.map(() => {
        const row = el("div", "br-row");
        const name = el("span", "br-name");
        const track = el("span", "br-track");
        const fill = el("i");
        track.appendChild(fill);
        const val = el("span", "br-val");
        row.append(name, track, val);
        wrap.appendChild(row);
        return { row, name, fill, val };
      });
      const foot = el("p", "br-foot");
      wrap.appendChild(foot);
      root.appendChild(wrap);
      return (p) => {
        const ph = cfg.phases[p];
        const names = ph.items || cfg.items;
        const picks = [].concat(ph.pick === undefined ? [] : ph.pick);
        rows.forEach((r, i) => {
          const v = ph.values[i];
          r.name.textContent = names[i];
          r.val.textContent = v === null || v === undefined ? "–" : (cfg.div ? (v / cfg.div).toFixed(2) : v) + unit;
          r.fill.style.width = Math.max(0, ((v || 0) / max) * 100) + "%";
          r.row.classList.toggle("is-pick", picks.includes(i));
          r.row.classList.toggle("is-cut", ph.cut !== undefined && i >= ph.cut);
        });
        foot.classList.remove("is-in");
        foot.textContent = ph.foot || "";
        if (ph.foot) later(() => foot.classList.add("is-in"), 500);
      };
    };
  },

  scatter(cfg) {
    return (root) => {
      const plane = el("div", "em-plane");
      root.appendChild(plane);
      const svg = document.createElementNS(svgNS, "svg");
      svg.setAttribute("viewBox", "0 0 100 100");
      svg.setAttribute("preserveAspectRatio", "none");
      svg.setAttribute("class", "em-lines");
      plane.appendChild(svg);
      const count = cfg.points.length;
      const points = cfg.points.map(([t, x, y, g], i) => {
        const node = el("span", "em-point em-" + (g || "a"), t);
        plane.appendChild(node);
        return { node, x, y, sx: 8 + (84 * i) / Math.max(count - 1, 1) };
      });
      const query = el("span", "em-point em-query");
      plane.appendChild(query);
      const legend = el("div", "em-legend");
      Object.entries(cfg.groups || {}).forEach(([g, name]) => {
        const key = el("span", "em-key em-" + g);
        key.append(el("i"), document.createTextNode(name));
        legend.appendChild(key);
      });
      root.appendChild(legend);
      return (p) => {
        const ph = cfg.phases[p];
        const placed = ph.placed !== false;
        const near = ph.near || [];
        points.forEach((o, i) => {
          place(o.node, placed ? o.x : o.sx, placed ? o.y : 92);
          o.node.classList.toggle("is-placed", placed);
          o.node.classList.toggle("is-dim", near.length > 0 && !near.includes(i));
          o.node.classList.toggle("is-near", near.includes(i));
        });
        legend.classList.toggle("is-in", placed);
        svg.replaceChildren();
        if (ph.query) {
          query.textContent = ph.query[0];
          place(query, ph.query[1], ph.query[2]);
          query.classList.add("is-in");
          near.forEach((i, k) => {
            const line = document.createElementNS(svgNS, "line");
            line.setAttribute("x1", ph.query[1]);
            line.setAttribute("y1", ph.query[2]);
            line.setAttribute("x2", points[i].x);
            line.setAttribute("y2", points[i].y);
            line.setAttribute("vector-effect", "non-scaling-stroke");
            svg.appendChild(line);
            later(() => line.classList.add("is-on"), 250 + k * 220);
          });
        } else {
          query.classList.remove("is-in");
        }
      };
    };
  },

  chips(cfg) {
    return (root) => {
      const wrap = el("div", "ch-wrap");
      root.appendChild(wrap);
      return (p) => {
        const ph = cfg.phases[p];
        wrap.replaceChildren();
        (ph.rows || []).forEach((row) => {
          const block = el("div", "ch-block");
          if (row.cap) block.appendChild(el("span", "ch-cap", row.cap));
          const line = el("div", "ch-row" + (row.box ? " is-box" : ""));
          row.chips.forEach((item, i) => {
            const o = chipOf(item);
            const chip = el("span", "ch-chip" + classes("is-", o.c));
            chip.appendChild(el("span", "", o.t));
            if (o.n !== undefined) chip.appendChild(el("small", "", String(o.n)));
            chip.style.animationDelay = i * 0.06 + "s";
            line.appendChild(chip);
          });
          block.appendChild(line);
          wrap.appendChild(block);
        });
        if (ph.out) {
          const out = el("div", "ch-out" + classes("is-", ph.outC));
          if (ph.outCap) out.appendChild(el("span", "ch-cap", ph.outCap));
          out.appendChild(el("p", "", ph.out));
          wrap.appendChild(out);
          later(() => out.classList.add("is-in"), 350);
        }
      };
    };
  },

  cycle(cfg) {
    return (root) => {
      const n = cfg.steps.length;
      const ring = el("div", "lp-ring cy-ring" + (cfg.log ? "" : " is-solo"));
      ring.innerHTML =
        '<svg viewBox="0 0 100 100" aria-hidden="true"><circle class="lp-track" cx="50" cy="50" r="34"></circle><circle class="lp-flow" cx="50" cy="50" r="34"></circle></svg>';
      const arm = el("div", "lp-arm");
      arm.appendChild(el("span", "lp-dot"));
      ring.appendChild(arm);
      const mid = el("div", "cy-mid");
      const big = el("strong");
      const small = el("span");
      mid.append(big, small);
      ring.appendChild(mid);
      const nodes = cfg.steps.map((name, i) => {
        const a = ((-90 + (360 * i) / n) * Math.PI) / 180;
        const node = place(el("span", "lp-node", name), 50 + 34 * Math.cos(a), 50 + 34 * Math.sin(a));
        ring.appendChild(node);
        return node;
      });
      root.appendChild(ring);
      let log = null;
      if (cfg.log) {
        log = el("div", "cy-log");
        log.appendChild(el("span", "ch-cap", cfg.log));
        root.appendChild(log);
      }
      let spin = 0;
      let last = 0;
      return (p) => {
        const ph = cfg.phases[p];
        const at = ph.at === undefined ? p % n : ph.at;
        spin += (at - last + n) % n;
        last = at;
        arm.style.transform = "rotate(" + (spin * 360) / n + "deg)";
        nodes.forEach((node, i) => node.classList.toggle("is-hot", i === at));
        big.textContent = ph.center || "";
        small.textContent = ph.sub || "";
        if (log) {
          [...log.querySelectorAll(".cy-line")].forEach((line) => line.remove());
          (ph.lines || []).forEach((text, i, all) => {
            const o = chipOf(text);
            const line = el("span", "cy-line" + classes("is-", o.c) + (i === all.length - 1 ? " is-new" : ""), o.t);
            log.appendChild(line);
          });
        }
      };
    };
  },

  stack(cfg) {
    return (root) => {
      const col = el("div", "st-col");
      const layers = cfg.layers.map((layer) => {
        const box = el("div", "st-layer");
        box.appendChild(el("strong", "", layer.t));
        if (layer.s) box.appendChild(el("span", "", layer.s));
        col.appendChild(box);
        return box;
      });
      const side = el("div", "st-side");
      root.append(col, side);
      return (p) => {
        const ph = cfg.phases[p];
        const at = [].concat(ph.at === undefined ? p : ph.at);
        layers.forEach((box, i) => {
          box.classList.toggle("is-hot", at.includes(i));
          box.classList.toggle("is-dim", (ph.dim || []).includes(i));
        });
        side.classList.remove("is-in");
        side.replaceChildren();
        if (ph.title) side.appendChild(el("strong", "", ph.title));
        if (ph.side) side.appendChild(el("p", "", ph.side));
        if (ph.title || ph.side) later(() => side.classList.add("is-in"), 250);
      };
    };
  },

  compare(cfg) {
    return (root) => {
      const cols = [cfg.left, cfg.right].map((title, ci) => {
        const card = el("div", "cp-card " + (ci ? "cp-r" : "cp-l"));
        card.appendChild(el("span", "cp-title", title));
        const list = el("div", "cp-list");
        card.appendChild(list);
        root.appendChild(card);
        return { card, list, seen: 0 };
      });
      root.appendChild(el("span", "cp-vs", "vs"));
      return (p) => {
        const ph = cfg.phases[p];
        [ph.l || [], ph.r || []].forEach((items, ci) => {
          const col = cols[ci];
          col.list.replaceChildren();
          items.forEach((item, i) => {
            const o = chipOf(item);
            const row = el("div", "cp-item" + classes("is-", o.c));
            row.appendChild(el("span", "", o.t));
            if (o.v) row.appendChild(el("b", "", o.v));
            if (i >= col.seen) {
              row.classList.add("is-new");
              row.style.animationDelay = (i - col.seen) * 0.15 + "s";
            }
            col.list.appendChild(row);
          });
          col.seen = items.length;
          col.card.classList.toggle("is-win", ph.win === (ci ? "r" : "l"));
          col.card.classList.toggle("is-lose", Boolean(ph.win) && ph.win !== (ci ? "r" : "l"));
        });
      };
    };
  },

  grid(cfg) {
    return (root) => {
      const wrap = el("div", "gr-wrap");
      const cap = el("span", "br-cap");
      const table = el("div", "gr-table");
      table.style.gridTemplateColumns = "4.6rem repeat(" + cfg.cols.length + ", 1fr)";
      table.appendChild(el("span"));
      const colHeads = cfg.cols.map((name) => table.appendChild(el("span", "gr-col", name)));
      const rowHeads = [];
      const cells = cfg.rows.map((name) => {
        rowHeads.push(table.appendChild(el("span", "gr-rowname", name)));
        return cfg.cols.map(() => table.appendChild(el("span", "gr-cell")));
      });
      wrap.append(cap, table);
      root.appendChild(wrap);
      return (p) => {
        const ph = cfg.phases[p];
        cap.textContent = ph.cap || cfg.title || "";
        rowHeads.forEach((head, i) => head.classList.toggle("is-hot", ph.focus === i));
        colHeads.forEach((head, i) => head.classList.toggle("is-hot", (ph.colHot || []).includes(i)));
        cells.forEach((row, ri) =>
          row.forEach((cell, ci) => {
            const v = ph.cells ? ph.cells[ri][ci] : 0;
            cell.style.setProperty("--v", v);
            cell.textContent = ph.nums && v ? v.toFixed(1) : "";
            cell.classList.toggle("is-dim", ph.focus !== undefined && ph.focus !== ri);
          })
        );
      };
    };
  },
};

function fromConfig(cfg) {
  return {
    rounds: 1,
    phases: cfg.phases,
    build: kinds[cfg.kind](cfg),
  };
}

const vizData = (() => {
  const node = document.getElementById("viz-data");
  return node ? JSON.parse(node.textContent) : {};
})();

function createPlayer(parts) {
  const { viz, phaseBox, roundBox, caption } = parts;
  const own = [];
  let scene = null;
  let show = null;
  let phase = 0;
  let round = 0;
  let timer = 0;
  let captionTimer = 0;
  let visible = true;

  function render() {
    own.forEach((id) => window.clearTimeout(id));
    own.length = 0;
    pending = own;
    window.clearTimeout(timer);
    show(phase, round);

    [...phaseBox.children].forEach((pill, index) => {
      pill.classList.toggle("is-hot", index === phase);
      pill.classList.toggle("is-past", index < phase);
    });
    if (roundBox) {
      roundBox.textContent = scene.rounds > 1 ? scene.roundLabel + " " + (round + 1) + " of " + scene.rounds : "";
    }

    if (caption) {
      const note = scene.phases[phase].note;
      caption.style.opacity = "0";
      window.clearTimeout(captionTimer);
      captionTimer = window.setTimeout(() => {
        caption.textContent = note;
        caption.style.opacity = "1";
      }, 160);
    }

    if (!reduce && visible) timer = window.setTimeout(advance, scene.phases[phase].ms || 2600);
  }

  function advance() {
    phase += 1;
    if (phase === scene.phases.length) {
      phase = 0;
      round = (round + 1) % scene.rounds;
    }
    render();
  }

  function open(name) {
    scene = scenes[name] || fromConfig(vizData[name]);
    phase = 0;
    round = 0;
    viz.replaceChildren();
    viz.className = "viz viz-" + (scenes[name] ? name : vizData[name].kind);
    void viz.offsetWidth;
    viz.classList.add("is-in");
    pending = own;
    show = scene.build(viz);

    phaseBox.replaceChildren();
    scene.phases.forEach((item, index) => {
      const pill = el("button", "viz-pill", item.label);
      pill.type = "button";
      pill.addEventListener("click", () => {
        phase = index;
        render();
      });
      phaseBox.appendChild(pill);
    });
    render();
  }

  function setVisible(next) {
    if (next === visible || !scene) {
      visible = next;
      return;
    }
    visible = next;
    if (visible) render();
    else window.clearTimeout(timer);
  }

  return { open, setVisible };
}

const watcher =
  "IntersectionObserver" in window
    ? new IntersectionObserver((entries) => {
        entries.forEach((entry) => entry.target.player && entry.target.player.setVisible(entry.isIntersecting));
      }, { threshold: 0.25 })
    : null;

function mountPlayer(stage) {
  const player = createPlayer({
    viz: stage.querySelector(".viz"),
    phaseBox: stage.querySelector(".viz-phases"),
    roundBox: stage.querySelector(".viz-round"),
    caption: stage.querySelector(".motion-caption"),
  });
  stage.player = player;
  if (watcher) watcher.observe(stage);
  return player;
}

document.querySelectorAll("[data-scene]").forEach((stage) => {
  mountPlayer(stage).open(stage.dataset.scene);
});
