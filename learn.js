const scenes = {
  loop: {
    nodes: ["Goal", "Plan", "Act", "Observe"],
    captions: ["goal", "plan", "act", "observe"],
    meters: ["Progress", "Evidence"],
    notes: [
      "Start with the outcome you actually need, not the first tool that comes to mind.",
      "Break that outcome into the next concrete step. One step, not the whole project.",
      "Do the step: query, call a tool, or write a draft.",
      "Look at what came back. If the goal is not met, plan again from this evidence.",
    ],
    bars: [
      [22, 8],
      [46, 24],
      [70, 38],
      [92, 74],
    ],
  },
  orch: {
    nodes: ["Brief", "Search", "SQL", "Write"],
    captions: ["brief", "search", "sql", "write"],
    meters: ["Tasks out", "Results in"],
    notes: [
      "The orchestrator keeps the brief. Specialists only see their piece.",
      "Search is asked for the source documents.",
      "SQL is asked for the numbers in the warehouse.",
      "Write turns those pieces into the answer the person asked for.",
    ],
    bars: [
      [18, 6],
      [40, 20],
      [66, 48],
      [88, 80],
    ],
  },
  sql: {
    nodes: ["Question", "SQL", "Run", "Rows"],
    captions: ["ask", "write", "run", "rows"],
    meters: ["Query", "Rows"],
    notes: [
      "The question is still just language. Nothing has touched the database.",
      "The model has written SQL. It has not run yet.",
      "The database executes the query.",
      "These rows are the answer, not the model's guess.",
    ],
    bars: [
      [15, 4],
      [48, 12],
      [72, 40],
      [96, 90],
    ],
  },
  llm: {
    nodes: ["Context", "Predict", "Pick", "Append"],
    captions: ["context", "predict", "pick", "append"],
    meters: ["Context", "Next token"],
    notes: [
      "The sentence so far is the only context the model can see.",
      "It scores possible next tokens. It does not retrieve a finished line.",
      "One token is chosen.",
      "That token is appended, and prediction starts again.",
    ],
    bars: [
      [30, 12],
      [55, 62],
      [70, 44],
      [86, 28],
    ],
  },
};

const topics = document.querySelectorAll(".worth-item");
const labels = document.querySelectorAll(".orbit-label");
const dot = document.getElementById("orbit-dot");
const dialValue = document.getElementById("dial-value");
const dialCaption = document.getElementById("dial-caption");
const barA = document.getElementById("bar-a");
const barB = document.getElementById("bar-b");
const meterAName = document.getElementById("meter-a-name");
const meterBName = document.getElementById("meter-b-name");
const caption = document.getElementById("motion-caption");

const angles = [-90, 0, 90, 180];
let topic = "loop";
let step = 0;
let timer = 0;
let captionTimer = 0;

function paint() {
  const scene = scenes[topic];
  labels.forEach((label, index) => {
    label.textContent = scene.nodes[index];
    label.classList.toggle("is-hot", index === step);
  });
  if (dot) {
    dot.style.transform = "translate(-50%, -50%) rotate(" + angles[step] + "deg) translateX(104px)";
  }
  if (dialValue) dialValue.textContent = String(step + 1).padStart(2, "0");
  if (dialCaption) dialCaption.textContent = scene.captions[step];
  if (meterAName) meterAName.textContent = scene.meters[0];
  if (meterBName) meterBName.textContent = scene.meters[1];
  if (barA) barA.style.width = scene.bars[step][0] + "%";
  if (barB) barB.style.width = scene.bars[step][1] + "%";
  if (caption) {
    const note = scene.notes[step];
    caption.style.opacity = "0";
    window.clearTimeout(captionTimer);
    captionTimer = window.setTimeout(() => {
      caption.textContent = note;
      caption.style.opacity = "1";
    }, 160);
  }
}

function play() {
  window.clearInterval(timer);
  paint();
  timer = window.setInterval(() => {
    step = (step + 1) % 4;
    paint();
  }, 1700);
}

if (topics.length && dot) {
  topics.forEach((button) => {
    button.addEventListener("click", () => {
      topic = button.dataset.topic;
      step = 0;
      topics.forEach((item) => {
        item.setAttribute("aria-selected", item === button ? "true" : "false");
      });
      play();
    });
  });
  labels.forEach((label) => {
    label.addEventListener("click", () => {
      step = Number(label.dataset.step);
      play();
    });
  });
  play();
}
