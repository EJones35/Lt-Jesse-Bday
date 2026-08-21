const mainSubtitle = document.querySelector(".main-subtitle");
const mission1Subtitle = document.querySelector(".mission1-subtitle");
const mission2Subtitle = document.querySelector(".mission2-subtitle");


function reloadTime() {
	const missionDate = new Date("2026-10-04T00:00:00").getTime();
	const today = Date.now();

	let timeLeft = missionDate - today;

	const missionDateDays = Math.floor(timeLeft / 86400000);
	timeLeft -= missionDateDays * 86400000;

	const missionDateHours = Math.floor(timeLeft / 3600000);
	timeLeft -= missionDateHours * 3600000;

	const missionDateMinutes = Math.floor(timeLeft / 60000);
	timeLeft -= missionDateMinutes * 60000;

	const missionDateSeconds = Math.floor(timeLeft / 1000);

	const timeLeftString = `${missionDateDays.toString().padStart(2, "0")}:${missionDateHours.toString().padStart(2, "0")}:${missionDateMinutes.toString().padStart(2, "0")}:${missionDateSeconds.toString().padStart(2, "0")} left`;

	mainSubtitle.textContent = `4 October 2026 - ${timeLeftString}`;
}

function reloadMission1Time() {
	const missionDate = new Date("2026-10-04T13:45:00").getTime();
	const today = Date.now();

	let timeLeft = missionDate - today;

	const missionDateDays = Math.floor(timeLeft / 86400000);
	timeLeft -= missionDateDays * 86400000;

	const missionDateHours = Math.floor(timeLeft / 3600000);
	timeLeft -= missionDateHours * 3600000;

	const missionDateMinutes = Math.floor(timeLeft / 60000);
	timeLeft -= missionDateMinutes * 60000;

	const missionDateSeconds = Math.floor(timeLeft / 1000);

	const timeLeftString = `${missionDateDays.toString().padStart(2, "0")}:${missionDateHours.toString().padStart(2, "0")}:${missionDateMinutes.toString().padStart(2, "0")}:${missionDateSeconds.toString().padStart(2, "0")}`;

	mission1Subtitle.textContent = `Only ${timeLeftString} until the deployment!`;
}

function reloadMission2Time() {
	const missionDate = new Date("2026-10-04T15:45:00").getTime();
	const today = Date.now();

	let timeLeft = missionDate - today;

	const missionDateDays = Math.floor(timeLeft / 86400000);
	timeLeft -= missionDateDays * 86400000;

	const missionDateHours = Math.floor(timeLeft / 3600000);
	timeLeft -= missionDateHours * 3600000;

	const missionDateMinutes = Math.floor(timeLeft / 60000);
	timeLeft -= missionDateMinutes * 60000;

	const missionDateSeconds = Math.floor(timeLeft / 1000);

	const timeLeftString = `${missionDateDays.toString().padStart(2, "0")}:${missionDateHours.toString().padStart(2, "0")}:${missionDateMinutes.toString().padStart(2, "0")}:${missionDateSeconds.toString().padStart(2, "0")}`;

	mission2Subtitle.textContent = `Only ${timeLeftString} until the deployment!`;
}

reloadTime();
reloadMission1Time();
reloadMission2Time();
setInterval(reloadTime, 1000);
setInterval(reloadMission1Time, 1000);
setInterval(reloadMission2Time, 1000);