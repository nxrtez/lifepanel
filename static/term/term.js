function handleTickInit(tick) {
  // Target: 19 December 2025 00:00 local time
  const target = new Date(2025, 11, 19, 0, 0, 0);

  const counter = Tick.count.down(target, { format: ["d","h","m","s"] });

  counter.onupdate = function (value) { tick.value = value; };
  counter.onended = function () {
    const el = document.getElementById("celebration");
    if (el) el.classList.remove("hidden");
  };
}
