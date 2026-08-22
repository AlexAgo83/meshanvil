// @ts-check

/**
 * @param {boolean} served
 * @param {() => Promise<number>} refreshLive
 */
export function startLiveRefresh(served, refreshLive) {
  if (!served) return;
  if ("EventSource" in window) {
    const stream = new EventSource(`${location.origin}/api/events`);
    stream.addEventListener("changed", () => { refreshLive(); });
    /** @type {any} */ (window).__meshanvilStopLive = () => stream.close();
    window.addEventListener("beforeunload", () => stream.close(), { once: true });
    return;
  }
  let liveTimer = 0;
  const tick = async () => {
    const cost = await refreshLive();
    liveTimer = setTimeout(tick, Math.max(1000, cost * 20));
  };
  liveTimer = setTimeout(tick, 1000);
  /** @type {any} */ (globalThis).__meshanvilStopLive = () => clearTimeout(liveTimer);
  addEventListener("beforeunload", () => clearTimeout(liveTimer), { once: true });
}
