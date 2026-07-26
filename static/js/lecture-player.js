(() => {
  const player = document.querySelector("[data-seminar-player]");
  if (!player) return;
  const synth = window.speechSynthesis;
  const Utterance = window.SpeechSynthesisUtterance;
  const available = Boolean(synth && Utterance);
  const segments = [...player.querySelectorAll("[data-audio-segment]")];
  const play = player.querySelector("[data-audio-play]");
  const pause = player.querySelector("[data-audio-pause]");
  const stop = player.querySelector("[data-audio-stop]");
  const voiceSelect = player.querySelector("[data-audio-voice]");
  const rateSelect = player.querySelector("[data-audio-rate]");
  const status = player.querySelector("[data-audio-status]");
  const progress = player.querySelector("[data-audio-progress]");
  let voices = [];
  let current = 0;
  let session = 0;
  let playing = false;
  let paused = false;

  function setStatus(text) {
    status.textContent = text;
  }

  function clearSpeaking() {
    segments.forEach((segment) => segment.classList.remove("is-speaking"));
  }

  function updateControls() {
    play.disabled = !available || (playing && !paused);
    pause.disabled = !available || !playing;
    stop.disabled = !available || !playing;
    pause.textContent = paused ? "Resume" : "Pause";
  }

  function setProgress(value) {
    progress.style.width = `${Math.max(0, Math.min(1, value)) * 100}%`;
  }

  function populateVoices() {
    if (!available) return;
    voices = synth.getVoices().filter((voice) => voice.lang.toLowerCase().startsWith("en"));
    if (!voices.length) voices = synth.getVoices();
    voiceSelect.replaceChildren();
    voices.forEach((voice, index) => {
      const option = document.createElement("option");
      option.value = String(index);
      option.textContent = `${voice.name} (${voice.lang})${voice.default ? " - default" : ""}`;
      voiceSelect.append(option);
    });
  }

  function stopPlayback(announce = true) {
    session += 1;
    if (available) {
      synth.cancel();
      synth.resume();
    }
    playing = false;
    paused = false;
    current = 0;
    clearSpeaking();
    setProgress(0);
    if (announce) setStatus("Stopped. Select Play / Replay or Play from here.");
    updateControls();
  }

  function speakSegment(index, playbackSession) {
    if (playbackSession !== session) return;
    if (index >= segments.length) {
      playing = false;
      paused = false;
      current = 0;
      clearSpeaking();
      setProgress(1);
      setStatus("Seminar complete. Prepare the expert-defense response.");
      updateControls();
      return;
    }
    current = index;
    clearSpeaking();
    const segment = segments[index];
    segment.classList.add("is-speaking");
    const heading = segment.querySelector("h2")?.textContent.trim() || `Layer ${index + 1}`;
    const body = segment.querySelector(":scope > p")?.textContent.trim() || "";
    const utterance = new Utterance(`${heading}. ${body}`);
    utterance.rate = Number.parseFloat(rateSelect.value);
    utterance.pitch = 0.94;
    utterance.voice = voices[Number.parseInt(voiceSelect.value, 10)] || voices[0] || null;
    utterance.onstart = () => {
      setStatus(`Speaking layer ${index + 1} of ${segments.length}: ${heading}`);
      setProgress(index / segments.length);
      updateControls();
    };
    utterance.onend = () => {
      if (playbackSession !== session || paused) return;
      segment.classList.remove("is-speaking");
      setProgress((index + 1) / segments.length);
      speakSegment(index + 1, playbackSession);
    };
    utterance.onerror = (event) => {
      if (event.error === "canceled" || playbackSession !== session) return;
      stopPlayback(false);
      setStatus(`Audio stopped: ${event.error}. The written seminar remains available.`);
    };
    synth.speak(utterance);
  }

  function begin(index) {
    if (!available) {
      setStatus("Text-to-speech is unavailable in this browser.");
      return;
    }
    stopPlayback(false);
    session += 1;
    playing = true;
    paused = false;
    speakSegment(index, session);
    updateControls();
  }

  function togglePause() {
    if (!playing) return;
    const resumeNow = paused;
    paused = !paused;
    setStatus(`${resumeNow ? "Resumed" : "Paused"} at layer ${current + 1}.`);
    updateControls();
    if (resumeNow) synth.resume();
    else synth.pause();
  }

  play.addEventListener("click", () => begin(0));
  pause.addEventListener("click", togglePause);
  stop.addEventListener("click", () => stopPlayback());
  player.querySelectorAll("[data-play-from]").forEach((button) => {
    button.addEventListener("click", () => begin(Number.parseInt(button.dataset.playFrom, 10)));
  });
  synth?.addEventListener?.("voiceschanged", populateVoices);
  populateVoices();
  if (!available) setStatus("Text-to-speech is unavailable. Use the complete written transcript.");
  updateControls();
  window.addEventListener("pagehide", () => stopPlayback(false));
})();
