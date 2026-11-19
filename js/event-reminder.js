const reminderToggle = document.querySelector("#event-reminder-toggle");
const reminderPanel = document.querySelector("#event-reminder-details");
const reminder = document.querySelector(".event-reminder");
const reminderSummary = document.querySelector("#event-reminder-summary");
const reminderCountdown = document.querySelector("#event-reminder-countdown");
const registrationDeadline = new Date("2026-12-09T23:59:59+05:30").getTime();
const eventStart = new Date("2026-12-11T00:00:00+05:30").getTime();

function updateReminderCountdown() {
  const remaining = Math.max(0, registrationDeadline - Date.now());
  const totalSeconds = Math.floor(remaining / 1000);
  const days = Math.floor(totalSeconds / 86400);
  const hours = Math.floor((totalSeconds % 86400) / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;

  document.querySelector("#reminder-days").textContent = String(days).padStart(2, "0");
  document.querySelector("#reminder-hours").textContent = String(hours).padStart(2, "0");
  document.querySelector("#reminder-minutes").textContent = String(minutes).padStart(2, "0");
  document.querySelector("#reminder-seconds").textContent = String(seconds).padStart(2, "0");

  if (Date.now() > eventStart) {
    reminderSummary.textContent = "FOUNDER'S DIARY · 11 DEC";
    reminderCountdown.textContent = "Event day has passed";
  } else if (remaining === 0) {
    reminderCountdown.textContent = "Reminder date has passed";
  } else {
    reminderCountdown.textContent = `${days} days to register`;
  }
}

reminderToggle.addEventListener("click", () => {
  const isExpanded = reminderToggle.getAttribute("aria-expanded") === "true";
  reminderToggle.setAttribute("aria-expanded", String(!isExpanded));
  reminderPanel.hidden = isExpanded;
  reminder.classList.toggle("is-open", !isExpanded);
});

updateReminderCountdown();
window.setInterval(updateReminderCountdown, 1000);
