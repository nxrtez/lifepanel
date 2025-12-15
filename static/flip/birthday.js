function handleTickInit(tick) {
  const now = new Date();

  let target = new Date(now.getFullYear(), 11, 24, 0, 0, 0); // Dec 24 00:00 local
  if (now > target) target = new Date(now.getFullYear() + 1, 11, 24, 0, 0, 0);

  const counter = Tick.count.down(target, { format: ["d","h","m","s"] });

  counter.onupdate = function (value) { tick.value = value; };
  counter.onended = function () {
    const el = document.getElementById("celebration");
    if (el) el.classList.remove("hidden");
  };
}
