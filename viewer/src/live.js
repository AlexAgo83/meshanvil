// @ts-check

/**
 * @param {boolean} served
 * @param {() => Promise<number>} refreshLive
 */
export function startLiveRefresh(served, refreshLive) {
  if (!served) return;
  if ("EventSource" in window) {
    const stream = new EventSource(`${location.origin}/api/events`);
    stream.addEventListener("changed", (event) => {
      // The page cannot swap its own code: a changed bundle is the one update it answers by
      // reloading. Everything else is data, and data is what refreshLive is for.
      let components = [];
      try { components = JSON.parse(/** @type {any} */ (event).data || "{}").components || []; }
      catch { components = []; }
      if (components.includes("viewer")) { location.reload(); return; }
      refreshLive();
    });
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
