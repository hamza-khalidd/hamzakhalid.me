const topics = document.querySelectorAll(".worth-item");
const worthStage = document.querySelector(".worth-stage");

if (topics.length && worthStage) {
  const player = mountPlayer(worthStage);
  topics.forEach((button) => {
    button.addEventListener("click", () => {
      topics.forEach((item) => {
        item.setAttribute("aria-selected", item === button ? "true" : "false");
      });
      player.open(button.dataset.topic);
    });
  });
  player.open("loop");
}
