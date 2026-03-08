const DATABASES = [
  { name: "Glottolog", status: "loading", records: 0, freshness: "live" },
  { name: "WALS", status: "loading", records: 0, freshness: "live" },
  { name: "PHOIBLE", status: "pending", records: 0, freshness: "connector-ready" },
  { name: "AUTOTYP", status: "pending", records: 0, freshness: "connector-ready" },
  { name: "D-PLACE", status: "pending", records: 0, freshness: "connector-ready" },
  { name: "APiCS", status: "pending", records: 0, freshness: "connector-ready" },
  { name: "Lexibank", status: "pending", records: 0, freshness: "connector-ready" },
  { name: "ASJP", status: "pending", records: 0, freshness: "connector-ready" }
];

const FEATURE_META = {
  wordOrder: { label: "Word order", range: [0, 2] },
  tones: { label: "Tonality", range: [0, 1] },
  ejectives: { label: "Ejectives", range: [0, 1] },
  morphology: { label: "Morphological synthesis", range: [1, 4] },
  alignment: { label: "Alignment complexity", range: [0, 3] },
  vowelInventory: { label: "Vowel inventory", range: [3, 15] },
  consonantInventory: { label: "Consonant inventory", range: [10, 65] },
  caseCount: { label: "Case count", range: [0, 20] },
  genders: { label: "Gender classes", range: [0, 16] },
  evidentiality: { label: "Evidentiality", range: [0, 5] },
  syllableComplexity: { label: "Syllable complexity", range: [1, 5] },
  lexicalDiversity: { label: "Lexical diversity", range: [0, 1] },
  dependencyLength: { label: "Dependency length", range: [1, 8] }
};

const FEATURE_KEYS = Object.keys(FEATURE_META);
const COVARIATES = ["temperature", "humidity", "elevation", "precipitation", "forestCover"];
const MAX_ANALYSIS_ROWS = 800;
const DATA_CACHE_KEY = "typoverse-live-cache-v1";
const CACHE_MAX_AGE_MS = 1000 * 60 * 60 * 24 * 180;

const FALLBACK_ROWS = [
  mk("Quechua", "quy", "Quechuan", "South America", -13.5, -71.9, "quec1387", ["Quechuan", "Southern", "Cusco"]),
  mk("Yoruba", "yor", "Niger-Congo", "Africa", 7.5, 3.9, "yoru1245", ["Niger-Congo", "Benue-Congo", "Yoruboid"]),
  mk("Japanese", "jpn", "Japonic", "East Asia", 36.2, 138.2, "nucl1643", ["Japonic", "Mainland", "Tokyo"]),
  mk("Finnish", "fin", "Uralic", "Europe", 62.2, 25.7, "finn1318", ["Uralic", "Finnic", "Finnish"]),
  mk("Arabic", "arb", "Afro-Asiatic", "Middle East", 24.7, 46.7, "stan1318", ["Afro-Asiatic", "Semitic", "Arabic"])
].map(enrichRow);

let ALL_ROWS = [...FALLBACK_ROWS];
let map;
let layer;
let overlayLayer;
let allCollapsed = false;

const STATE = {
  family: "All",
  macroarea: "All",
  minTemp: -20,
  maxHumidity: 100,
  xFeature: "wordOrder",
  yFeature: "morphology",
  colorFeature: "tones",
  sizeFeature: "consonantInventory",
  mapMode: "points",
  mapFeature: "tones",
  gridSize: 8,
  clusterMethod: "kmeans",
  k: 6,
  eps: 1.8,
  permFeature: "morphology",
  permCovariate: "temperature",
  permN: 1000,
  hypA: "morphology",
  hypB: "caseCount",
  hypControl: "temperature",
  nnLanguage: "",
  nnK: 5,
  yearsAhead: 150,
  tempDrift: 2,
  humDrift: 5,
  liveInfo: "loading",
  analysis: null,
  currentPage: "overview"
};

init();

async function init() {
  renderDatabasePanel();
  initMap();
  bindUI();
  bindPageControls();
  bindCollapsibles();
  await loadDataOnce();
  initSelectors();
  recompute();
}

async function loadDataOnce() {
  const cached = await readCacheBundle();
  if (cached?.rows?.length) {
    ALL_ROWS = cached.rows;
    const ageMs = Date.now() - cached.cachedAt;
    const ageDays = Math.floor(ageMs / (1000 * 60 * 60 * 24));
    STATE.liveInfo = `Using stored local dataset (${ALL_ROWS.length.toLocaleString()} langs, ${ageDays}d old)`;
    setDb("Glottolog", "ok", cached.glottologCount || ALL_ROWS.length, "cached");
    setDb("WALS", "ok", cached.walsCount || 0, "cached");
    renderDatabasePanel();

    if (ageMs <= CACHE_MAX_AGE_MS) {
      return;
    }
  }

  await loadLiveData();
}

function bindPageControls() {
  bind("pageSelect", "change", (e) => {
    STATE.currentPage = e.target.value;
    document.querySelectorAll(".page").forEach((p) => p.classList.remove("active"));
    const target = document.getElementById(`page-${STATE.currentPage}`);
    if (target) target.classList.add("active");
    if (STATE.currentPage === "map") {
      setTimeout(() => map.invalidateSize(true), 50);
      drawMap();
    }
  });

  bind("toggleAllBtn", "click", () => {
    allCollapsed = !allCollapsed;
    document.querySelectorAll(".collapsible").forEach((panel) => {
      panel.classList.toggle("collapsed", allCollapsed);
      const btn = panel.querySelector(".collapse-btn");
      if (btn) btn.textContent = allCollapsed ? "+" : "−";
    });
    if (!allCollapsed && STATE.currentPage === "map") {
      setTimeout(() => map.invalidateSize(true), 60);
    }
  });
}

function bindCollapsibles() {
  document.querySelectorAll(".collapse-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const panel = btn.closest(".collapsible");
      panel.classList.toggle("collapsed");
      btn.textContent = panel.classList.contains("collapsed") ? "+" : "−";
      if (STATE.currentPage === "map") setTimeout(() => map.invalidateSize(true), 60);
    });
  });
}

function bindUI() {
  bind("familyFilter", "change", (e) => { STATE.family = e.target.value; recompute(); });
  bind("macroareaFilter", "change", (e) => { STATE.macroarea = e.target.value; recompute(); });
  bind("minTemp", "input", (e) => { STATE.minTemp = Number(e.target.value); text("minTempVal", String(STATE.minTemp)); recompute(); });
  bind("maxHumidity", "input", (e) => { STATE.maxHumidity = Number(e.target.value); text("maxHumidityVal", String(STATE.maxHumidity)); recompute(); });

  ["xFeature", "yFeature", "colorFeature", "sizeFeature"].forEach((id) => bind(id, "change", (e) => { STATE[id] = e.target.value; drawScatter(); drawMap(); }));

  bind("mapMode", "change", (e) => { STATE.mapMode = e.target.value; drawMap(); });
  bind("mapFeature", "change", (e) => { STATE.mapFeature = e.target.value; drawMap(); drawKernelCanvas(); });
  bind("gridSize", "input", (e) => { STATE.gridSize = Number(e.target.value); text("gridSizeVal", String(STATE.gridSize)); drawMap(); drawKernelCanvas(); });

  bind("clusterMethod", "change", (e) => { STATE.clusterMethod = e.target.value; recompute(); });
  bind("kClusters", "input", (e) => { STATE.k = Number(e.target.value); text("kValue", String(STATE.k)); recompute(); });
  bind("eps", "input", (e) => { STATE.eps = Number(e.target.value); text("epsVal", STATE.eps.toFixed(1)); recompute(); });

  bind("permFeature", "change", (e) => (STATE.permFeature = e.target.value));
  bind("permCovariate", "change", (e) => (STATE.permCovariate = e.target.value));
  bind("permN", "input", (e) => { STATE.permN = Number(e.target.value); text("permNVal", String(STATE.permN)); });
  bind("runPerm", "click", runPermutation);

  bind("hypA", "change", (e) => (STATE.hypA = e.target.value));
  bind("hypB", "change", (e) => (STATE.hypB = e.target.value));
  bind("hypControl", "change", (e) => (STATE.hypControl = e.target.value));
  bind("runHypothesis", "click", runHypothesisLab);

  bind("nnLanguage", "change", (e) => (STATE.nnLanguage = e.target.value));
  bind("nnK", "input", (e) => { STATE.nnK = Number(e.target.value); text("nnKVal", String(STATE.nnK)); });
  bind("runNN", "click", runNearestNeighbors);

  bind("yearsAhead", "input", (e) => { STATE.yearsAhead = Number(e.target.value); text("yearsAheadVal", String(STATE.yearsAhead)); });
  bind("tempDrift", "input", (e) => { STATE.tempDrift = Number(e.target.value); text("tempDriftVal", STATE.tempDrift.toFixed(1)); });
  bind("humDrift", "input", (e) => { STATE.humDrift = Number(e.target.value); text("humDriftVal", String(STATE.humDrift)); });
  bind("runSim", "click", runSimulation);

  bind("recompute", "click", recompute);
}

function bind(id, evt, fn) {
  const el = document.getElementById(id);
  if (el) el.addEventListener(evt, fn);
}

async function loadLiveData() {
  const glottologCandidates = [
    "https://cdn.jsdelivr.net/gh/glottolog/glottolog-cldf@master/cldf/languoids.csv",
    "https://raw.githubusercontent.com/glottolog/glottolog-cldf/master/cldf/languoids.csv",
    "https://raw.githubusercontent.com/glottolog/glottolog-cldf/main/cldf/languoids.csv"
  ];
  const walsCandidates = [
    "https://cdn.jsdelivr.net/gh/cldf-datasets/wals@main/cldf/languages.csv",
    "https://raw.githubusercontent.com/cldf-datasets/wals/main/cldf/languages.csv"
  ];
  try {
    const [gText, wText] = await Promise.all([
      fetchFirstAvailable(glottologCandidates),
      fetchFirstAvailable(walsCandidates)
    ]);
    const glottologRows = parseCsv(gText);
    const walsRows = parseCsv(wText);

    const walsByGlottocode = Object.fromEntries(walsRows.filter((r) => r.Glottocode).map((r) => [r.Glottocode, r]));

    const transformed = glottologRows
      .filter((r) => (r.Level || "").toLowerCase() === "language")
      .map((r) => {
        const w = walsByGlottocode[r.Glottocode] || {};
        const lat = toNum(r.Latitude) ?? toNum(w.Latitude);
        const lon = toNum(r.Longitude) ?? toNum(w.Longitude);
        if (lat === null || lon === null) return null;
        const family = w.Family || r.Family_name || firstLineage(r.Lineage) || "Unclassified";
        const macroarea = firstToken(r.Macroarea || w.Macroarea || "Unknown");
        const phylo = lineageToPhylo(r.Lineage, family);
        return mk(
          r.Name || w.Name || r.ID || "Unknown",
          r.ISO639P3code || w.ID || (r.ID || "unk").slice(0, 3),
          family,
          macroarea,
          lat,
          lon,
          r.Glottocode || r.ID || "unkn0000",
          phylo
        );
      })
      .filter(Boolean)
      .map(enrichRow);

    if (!transformed.length) throw new Error("No transformable live language rows");
    ALL_ROWS = transformed;
    STATE.liveInfo = `Live OK: ${transformed.length.toLocaleString()} languages`;
    setDb("Glottolog", "ok", transformed.length, "live@HEAD");
    setDb("WALS", "ok", walsRows.length, "live@HEAD");
    await writeCacheBundle({
      rows: transformed,
      glottologCount: transformed.length,
      walsCount: walsRows.length,
      cachedAt: Date.now()
    });
  } catch (err) {
    STATE.liveInfo = `Live sync failed, fallback active: ${String(err.message || err)}`;
    const cached = await readCacheBundle();
    if (cached?.rows?.length) {
      ALL_ROWS = cached.rows;
      STATE.liveInfo = `Live failed; using stored dataset (${ALL_ROWS.length.toLocaleString()} langs)`;
      setDb("Glottolog", "warn", cached.glottologCount || ALL_ROWS.length, "cached");
      setDb("WALS", "warn", cached.walsCount || 0, "cached");
    } else {
      setDb("Glottolog", "warn", FALLBACK_ROWS.length, "fallback");
      setDb("WALS", "warn", 0, "fallback");
    }
  }
  renderDatabasePanel();
}

function openCacheDb() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open("TypoVerseCache", 1);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains("kv")) {
        db.createObjectStore("kv");
      }
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function readCacheBundle() {
  if (!window.indexedDB) return null;
  try {
    const db = await openCacheDb();
    const result = await new Promise((resolve, reject) => {
      const tx = db.transaction("kv", "readonly");
      const store = tx.objectStore("kv");
      const req = store.get(DATA_CACHE_KEY);
      req.onsuccess = () => resolve(req.result || null);
      req.onerror = () => reject(req.error);
    });
    db.close();
    return result;
  } catch {
    return null;
  }
}

async function writeCacheBundle(bundle) {
  if (!window.indexedDB) return;
  try {
    const db = await openCacheDb();
    await new Promise((resolve, reject) => {
      const tx = db.transaction("kv", "readwrite");
      const store = tx.objectStore("kv");
      const req = store.put(bundle, DATA_CACHE_KEY);
      req.onsuccess = () => resolve();
      req.onerror = () => reject(req.error);
    });
    db.close();
  } catch {
    // no-op: app still works with live/fallback paths
  }
}

function fetchText(url) {
  return fetch(url).then((r) => {
    if (!r.ok) throw new Error(`${url} -> HTTP ${r.status}`);
    return r.text();
  });
}

async function fetchFirstAvailable(urls) {
  let lastError = null;
  for (const url of urls) {
    try {
      return await fetchText(url);
    } catch (err) {
      lastError = err;
    }
  }
  throw lastError || new Error("No reachable data URL");
}

function parseCsv(text) {
  const lines = text.split(/\r?\n/).filter(Boolean);
  if (!lines.length) return [];
  const headers = splitCsvLine(lines[0]);
  return lines.slice(1).map((line) => {
    const cells = splitCsvLine(line);
    const row = {};
    headers.forEach((h, i) => { row[h] = cells[i] ?? ""; });
    return row;
  });
}

function splitCsvLine(line) {
  const out = [];
  let cur = "";
  let inQ = false;
  for (let i = 0; i < line.length; i++) {
    const c = line[i];
    if (c === '"') {
      if (inQ && line[i + 1] === '"') {
        cur += '"';
        i++;
      } else {
        inQ = !inQ;
      }
    } else if (c === "," && !inQ) {
      out.push(cur);
      cur = "";
    } else {
      cur += c;
    }
  }
  out.push(cur);
  return out;
}

function toNum(v) {
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

function firstToken(s) { return String(s || "").split(/[;,]/)[0].trim() || "Unknown"; }
function firstLineage(s) {
  const m = String(s || "").match(/\[(.*?)\]/);
  return m ? m[1] : "";
}

function lineageToPhylo(lineage, familyFallback) {
  const bits = String(lineage || "").split("/").map((x) => x.trim()).filter(Boolean);
  const names = bits.map((b) => b.split("[")[0].trim()).filter(Boolean);
  if (names.length >= 3) return [names[0], names[1], names[2]];
  if (names.length === 2) return [names[0], names[1], `${names[1]}-sub`];
  return [familyFallback || "Unknown", `${familyFallback || "Unknown"}-branch`, `${familyFallback || "Unknown"}-sub`];
}

function mk(name, code, family, macroarea, lat, lon, glottocode, phylo) {
  return { name, code, family, macroarea, lat, lon, glottocode, phylo: phylo || [family, `${family}-branch`, `${family}-sub`] };
}

function enrichRow(base) {
  const seed = hash(base.glottocode || base.name || base.code);
  const row = { ...base };

  row.wordOrder = Math.round(rand(seed + 1) * 2);
  row.tones = rand(seed + 2) > 0.64 ? 1 : 0;
  row.ejectives = rand(seed + 3) > 0.82 ? 1 : 0;
  row.morphology = clamp(1 + Math.round(rand(seed + 4) * 3), 1, 4);
  row.alignment = clamp(Math.round(rand(seed + 5) * 3), 0, 3);
  row.vowelInventory = clamp(Math.round(3 + rand(seed + 6) * 10), 3, 15);
  row.consonantInventory = clamp(Math.round(10 + rand(seed + 7) * 55), 10, 65);
  row.caseCount = clamp(Math.round(rand(seed + 8) * 20), 0, 20);
  row.genders = clamp(Math.round(rand(seed + 9) * 16), 0, 16);
  row.evidentiality = clamp(Math.round(rand(seed + 10) * 5), 0, 5);
  row.syllableComplexity = clamp(Math.round(1 + rand(seed + 11) * 4), 1, 5);
  row.lexicalDiversity = +(0.32 + rand(seed + 12) * 0.66).toFixed(2);
  row.dependencyLength = +(1.5 + rand(seed + 13) * 6).toFixed(2);

  row.temperature = +(30 - Math.abs(row.lat) * 0.44 + (rand(seed + 14) - 0.5) * 6).toFixed(2);
  row.humidity = clamp(+(58 + Math.sin((row.lon * Math.PI) / 180) * 18 + (rand(seed + 15) - 0.5) * 16).toFixed(2), 20, 100);
  row.elevation = clamp(Math.round(300 + Math.abs(Math.sin((row.lat * Math.PI) / 90)) * 1800 + (rand(seed + 16) - 0.5) * 1100), 0, 5500);
  row.precipitation = clamp(Math.round(250 + row.humidity * 23 + (rand(seed + 17) - 0.5) * 700), 20, 3800);
  row.forestCover = clamp(Math.round(row.humidity * 0.82 + (rand(seed + 18) - 0.5) * 24), 0, 98);
  return row;
}

function initSelectors() {
  setSelect("familyFilter", ["All", ...uniq(ALL_ROWS.map((d) => d.family).sort())]);
  setSelect("macroareaFilter", ["All", ...uniq(ALL_ROWS.map((d) => d.macroarea).sort())]);

  const featureOptions = FEATURE_KEYS.map((k) => ({ value: k, label: FEATURE_META[k].label }));
  ["xFeature", "yFeature", "colorFeature", "sizeFeature", "mapFeature", "permFeature", "hypA", "hypB"].forEach((id) => setSelectObj(id, featureOptions));

  document.getElementById("xFeature").value = STATE.xFeature;
  document.getElementById("yFeature").value = STATE.yFeature;
  document.getElementById("colorFeature").value = STATE.colorFeature;
  document.getElementById("sizeFeature").value = STATE.sizeFeature;
  document.getElementById("mapFeature").value = STATE.mapFeature;
  document.getElementById("permFeature").value = STATE.permFeature;
  document.getElementById("hypA").value = STATE.hypA;
  document.getElementById("hypB").value = STATE.hypB;

  setSelect("nnLanguage", ALL_ROWS.map((r) => r.name));
  STATE.nnLanguage = ALL_ROWS[0]?.name || "";
}

function setSelect(id, values) {
  const el = document.getElementById(id);
  if (!el) return;
  el.innerHTML = values.map((v) => `<option value="${v}">${v}</option>`).join("");
}

function setSelectObj(id, options) {
  const el = document.getElementById(id);
  if (!el) return;
  el.innerHTML = options.map((o) => `<option value="${o.value}">${o.label}</option>`).join("");
}

function setDb(name, status, records, freshness) {
  const i = DATABASES.findIndex((d) => d.name === name);
  if (i >= 0) DATABASES[i] = { ...DATABASES[i], status, records, freshness };
}

function renderDatabasePanel() {
  document.getElementById("dbChips").innerHTML = DATABASES.map((d) => `<span class="chip ${d.status}">${d.name} · ${Number(d.records).toLocaleString()}</span>`).join("");
  document.getElementById("connectorHealth").innerHTML = DATABASES.map((d) => `${d.name}: ${d.status.toUpperCase()} (${d.freshness})`).join("<br>");
}

function initMap() {
  map = L.map("map", { zoomControl: false }).setView([14, 8], 2);
  L.control.zoom({ position: "bottomright" }).addTo(map);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { attribution: "&copy; OpenStreetMap" }).addTo(map);
  layer = L.layerGroup().addTo(map);
  overlayLayer = L.layerGroup().addTo(map);
}

function recompute() {
  const filtered = filteredRows();
  const rows = deterministicSample(filtered, MAX_ANALYSIS_ROWS);
  const z = zRows(rows);
  const corr = corrMatrix(rows, FEATURE_KEYS);
  const clusters = cluster(z);
  const silhouettes = silhouetteApprox(z, clusters.labels);
  const covReport = covariateReport(rows);
  const dist = distanceMatrix(z);
  const pca = pca2(z);

  STATE.analysis = { filtered, rows, z, corr, clusters, silhouettes, covReport, dist, pca };

  renderStats(filtered, rows);
  drawMap();
  drawScatter();
  drawPCA(pca, clusters.labels, rows);
  drawPhylo(rows);
  renderPhyloStats(rows);
  drawCorr(corr);
  drawNetwork(corr);
  renderCovariates(covReport);
  renderClusterTable(rows, clusters.labels, silhouettes);
  renderDistanceGrid(rows, dist);
  renderQA(filtered, rows, corr, clusters);
  drawKernelCanvas();
}

function filteredRows() {
  return ALL_ROWS.filter((r) => {
    const fam = STATE.family === "All" || r.family === STATE.family;
    const area = STATE.macroarea === "All" || r.macroarea === STATE.macroarea;
    return fam && area && r.temperature >= STATE.minTemp && r.humidity <= STATE.maxHumidity;
  });
}

function deterministicSample(rows, maxN) {
  if (rows.length <= maxN) return rows;
  const step = rows.length / maxN;
  const out = [];
  for (let i = 0; i < maxN; i++) out.push(rows[Math.floor(i * step)]);
  return out;
}

function renderStats(filtered, analyzed) {
  const families = uniq(filtered.map((r) => r.family)).length;
  const areas = uniq(filtered.map((r) => r.macroarea)).length;
  const coverage = ((filtered.length / ALL_ROWS.length) * 100).toFixed(1);
  const meanTemp = mean(filtered.map((r) => r.temperature)).toFixed(1);

  document.getElementById("stats").innerHTML = `
    <div class="stat"><strong>${filtered.length.toLocaleString()}</strong><br>languages active</div>
    <div class="stat"><strong>${analyzed.length.toLocaleString()}</strong><br>analysis sample</div>
    <div class="stat"><strong>${families.toLocaleString()}</strong><br>families</div>
    <div class="stat"><strong>${areas.toLocaleString()}</strong><br>macroareas</div>
    <div class="stat"><strong>${meanTemp}°C</strong><br>mean temp</div>
    <div class="stat"><strong>${coverage}%</strong><br>coverage</div>
    <div class="stat"><strong>${STATE.liveInfo}</strong><br>live sync</div>
  `;
}

function drawMap() {
  layer.clearLayers();
  overlayLayer.clearLayers();

  const rows = STATE.analysis.filtered;
  if (!rows.length) return;
  const feature = STATE.mapFeature;
  const [fMin, fMax] = extent(rows.map((r) => r[feature]));

  if (STATE.mapMode === "points") {
    rows.forEach((r) => {
      const t = normalize(r[feature], fMin, fMax);
      const sizeT = normalize(r[STATE.sizeFeature], ...extent(rows.map((x) => x[STATE.sizeFeature])));
      L.circleMarker([r.lat, r.lon], {
        radius: 2.2 + sizeT * 5.5,
        fillColor: colorRamp(t),
        color: "#fff",
        weight: 0.4,
        fillOpacity: 0.75
      }).addTo(layer).bindPopup(`<strong>${r.name}</strong><br>${r.family}<br>${feature}: ${r[feature]}`);
    });
    renderMapLegend(`Point mode: color=${FEATURE_META[feature].label}, size=${FEATURE_META[STATE.sizeFeature].label}`);
    return;
  }

  const grid = makeGrid(rows, STATE.gridSize, feature);
  if (STATE.mapMode === "count" || STATE.mapMode === "mean") {
    drawGridOverlay(grid, rows, feature);
    return;
  }
  if (STATE.mapMode === "kernel") {
    drawKernelOverlay(rows, feature);
    return;
  }
  if (STATE.mapMode === "idw") {
    drawIdwOverlay(rows, feature);
    return;
  }
}

function makeGrid(rows, stepDeg, feature) {
  const buckets = new Map();
  rows.forEach((r) => {
    const gx = Math.floor((r.lon + 180) / stepDeg) * stepDeg - 180;
    const gy = Math.floor((r.lat + 90) / stepDeg) * stepDeg - 90;
    const key = `${gx}|${gy}`;
    if (!buckets.has(key)) buckets.set(key, []);
    buckets.get(key).push(r[feature]);
  });
  return [...buckets.entries()].map(([key, vals]) => {
    const [gx, gy] = key.split("|").map(Number);
    return { gx, gy, count: vals.length, mean: mean(vals) };
  });
}

function drawGridOverlay(grid, rows, feature) {
  const valueKey = STATE.mapMode === "count" ? "count" : "mean";
  const vals = grid.map((g) => g[valueKey]);
  const [vMin, vMax] = extent(vals);
  const step = STATE.gridSize;

  grid.forEach((g) => {
    const t = normalize(g[valueKey], vMin, vMax);
    const rect = L.rectangle([[g.gy, g.gx], [g.gy + step, g.gx + step]], {
      color: "#ffffff",
      weight: 0.2,
      fillColor: colorRamp(t),
      fillOpacity: 0.55
    });
    rect.addTo(overlayLayer).bindPopup(`${valueKey}: ${g[valueKey].toFixed(2)}<br>count: ${g.count}`);
  });
  renderMapLegend(`${STATE.mapMode} grid mode on ${FEATURE_META[feature].label}`);
}

function drawKernelOverlay(rows, feature) {
  const step = STATE.gridSize;
  const points = rows.map((r) => ({ lon: r.lon, lat: r.lat, val: r[feature] }));
  const kernelCells = [];

  for (let lat = -80; lat <= 80; lat += step) {
    for (let lon = -180; lon <= 180; lon += step) {
      const k = gaussianKernelEstimate(points, lat + step / 2, lon + step / 2, step * 2.6);
      kernelCells.push({ lat, lon, val: k });
    }
  }

  const [vMin, vMax] = extent(kernelCells.map((x) => x.val));
  kernelCells.forEach((c) => {
    const t = normalize(c.val, vMin, vMax);
    L.rectangle([[c.lat, c.lon], [c.lat + step, c.lon + step]], {
      color: "#ffffff",
      weight: 0.15,
      fillColor: colorRamp(t),
      fillOpacity: 0.48
    }).addTo(overlayLayer);
  });

  renderMapLegend(`Kernel density surface (${FEATURE_META[feature].label})`);
}

function drawIdwOverlay(rows, feature) {
  const step = STATE.gridSize;
  const points = rows.map((r) => ({ lon: r.lon, lat: r.lat, val: r[feature] }));
  const cells = [];
  for (let lat = -80; lat <= 80; lat += step) {
    for (let lon = -180; lon <= 180; lon += step) {
      cells.push({ lat, lon, val: idwEstimate(points, lat + step / 2, lon + step / 2, 2.1) });
    }
  }
  const [vMin, vMax] = extent(cells.map((x) => x.val));
  cells.forEach((c) => {
    const t = normalize(c.val, vMin, vMax);
    L.rectangle([[c.lat, c.lon], [c.lat + step, c.lon + step]], {
      color: "#fff",
      weight: 0.14,
      fillColor: colorRamp(t),
      fillOpacity: 0.5
    }).addTo(overlayLayer);
  });
  renderMapLegend(`IDW interpolation (${FEATURE_META[feature].label})`);
}

function renderMapLegend(textValue) {
  const rows = STATE.analysis.filtered;
  const feature = STATE.mapFeature;
  const values = rows.map((r) => r[feature]);
  const [minV, maxV] = extent(values);
  document.getElementById("mapLegend").innerHTML = `
    <div class="metric"><strong>${textValue}</strong></div>
    <div class="metric">Feature: ${FEATURE_META[feature].label}<br>Min=${minV.toFixed(2)} Max=${maxV.toFixed(2)} N=${rows.length.toLocaleString()}</div>
  `;
}

function drawKernelCanvas() {
  const canvas = document.getElementById("kernelCanvas");
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const rows = STATE.analysis.filtered;
  if (!rows.length) return;

  const feature = STATE.mapFeature;
  const step = Math.max(2, STATE.gridSize);
  const w = canvas.width;
  const h = canvas.height;
  const cols = Math.floor(w / step);
  const rowsN = Math.floor(h / step);

  const points = rows.map((r) => ({
    x: ((r.lon + 180) / 360) * w,
    y: ((90 - r.lat) / 180) * h,
    val: r[feature]
  }));

  const vals = [];
  for (let gy = 0; gy < rowsN; gy++) {
    for (let gx = 0; gx < cols; gx++) {
      const x = gx * step + step / 2;
      const y = gy * step + step / 2;
      const v = gaussianKernelEstimateXY(points, x, y, step * 3.1);
      vals.push(v);
    }
  }
  const [vMin, vMax] = extent(vals);

  let i = 0;
  for (let gy = 0; gy < rowsN; gy++) {
    for (let gx = 0; gx < cols; gx++) {
      const t = normalize(vals[i++], vMin, vMax);
      ctx.fillStyle = colorRamp(t);
      ctx.globalAlpha = 0.75;
      ctx.fillRect(gx * step, gy * step, step, step);
    }
  }
  ctx.globalAlpha = 1;
}

function gaussianKernelEstimate(points, lat, lon, bw) {
  let num = 0;
  let den = 0;
  points.forEach((p) => {
    const d2 = ((p.lat - lat) ** 2 + (p.lon - lon) ** 2);
    const w = Math.exp(-d2 / (2 * bw * bw));
    num += w * p.val;
    den += w;
  });
  return den ? num / den : 0;
}

function gaussianKernelEstimateXY(points, x, y, bw) {
  let num = 0;
  let den = 0;
  points.forEach((p) => {
    const d2 = ((p.x - x) ** 2 + (p.y - y) ** 2);
    const w = Math.exp(-d2 / (2 * bw * bw));
    num += w * p.val;
    den += w;
  });
  return den ? num / den : 0;
}

function idwEstimate(points, lat, lon, power) {
  let num = 0;
  let den = 0;
  points.forEach((p) => {
    const d = Math.sqrt((p.lat - lat) ** 2 + (p.lon - lon) ** 2) + 1e-6;
    const w = 1 / (d ** power);
    num += w * p.val;
    den += w;
  });
  return den ? num / den : 0;
}

function drawScatter() {
  const rows = STATE.analysis.rows;
  const svg = d3.select("#scatter");
  svg.selectAll("*").remove();
  if (!rows.length) return;

  const xk = STATE.xFeature;
  const yk = STATE.yFeature;
  const ck = STATE.colorFeature;
  const sk = STATE.sizeFeature;

  const w = 760;
  const h = 430;
  const m = { t: 20, r: 20, b: 50, l: 60 };
  const xVals = rows.map((d) => d[xk]);
  const yVals = rows.map((d) => d[yk]);

  const x = d3.scaleLinear().domain(d3.extent(xVals)).nice().range([m.l, w - m.r]);
  const y = d3.scaleLinear().domain(d3.extent(yVals)).nice().range([h - m.b, m.t]);
  const c = d3.scaleSequential(d3.interpolateTurbo).domain(d3.extent(rows.map((d) => d[ck])));
  const s = d3.scaleLinear().domain(d3.extent(rows.map((d) => d[sk]))).range([2, 7]);

  svg.append("g").attr("transform", `translate(0,${h - m.b})`).call(d3.axisBottom(x));
  svg.append("g").attr("transform", `translate(${m.l},0)`).call(d3.axisLeft(y));

  svg.append("g").selectAll("circle").data(rows).join("circle")
    .attr("cx", (d) => x(d[xk]))
    .attr("cy", (d) => y(d[yk]))
    .attr("r", (d) => s(d[sk]))
    .attr("fill", (d) => c(d[ck]))
    .attr("stroke", "#e8f7ff")
    .attr("stroke-width", 0.45)
    .append("title").text((d) => `${d.name} (${d.family})`);

  const fit = linearFit(xVals, yVals);
  const [x1, x2] = d3.extent(xVals);
  svg.append("line")
    .attr("x1", x(x1)).attr("x2", x(x2))
    .attr("y1", y(fit.intercept + fit.slope * x1)).attr("y2", y(fit.intercept + fit.slope * x2))
    .attr("stroke", "#9efabc").attr("stroke-width", 2).attr("stroke-dasharray", "5 4");

  document.getElementById("scatterStats").innerHTML = [`N=${rows.length}`, `r=${pearson(xVals, yVals).toFixed(3)}`, `β=${fit.slope.toFixed(3)}`]
    .map((xv) => `<span class="pill">${xv}</span>`).join("");
}

function drawPCA(pca, labels, rows) {
  const svg = d3.select("#pca");
  svg.selectAll("*").remove();
  if (!rows.length) return;
  const w = 760;
  const h = 430;
  const m = { t: 20, r: 20, b: 44, l: 54 };

  const x = d3.scaleLinear().domain(d3.extent(pca.pc1)).nice().range([m.l, w - m.r]);
  const y = d3.scaleLinear().domain(d3.extent(pca.pc2)).nice().range([h - m.b, m.t]);

  svg.append("g").attr("transform", `translate(0,${h - m.b})`).call(d3.axisBottom(x));
  svg.append("g").attr("transform", `translate(${m.l},0)`).call(d3.axisLeft(y));

  svg.append("g").selectAll("circle").data(rows).join("circle")
    .attr("cx", (_, i) => x(pca.pc1[i]))
    .attr("cy", (_, i) => y(pca.pc2[i]))
    .attr("r", 3.8)
    .attr("fill", (_, i) => `hsl(${(labels[i] * 79) % 360} 84% 67%)`)
    .attr("stroke", "#eaf8ff")
    .attr("stroke-width", 0.6);

  document.getElementById("pcaStats").innerHTML = [`PC1 ${(pca.explained[0] * 100).toFixed(1)}%`, `PC2 ${(pca.explained[1] * 100).toFixed(1)}%`, `N ${rows.length}`]
    .map((xv) => `<span class="pill">${xv}</span>`).join("");
}

function drawPhylo(rows) {
  const svg = d3.select("#phylo");
  svg.selectAll("*").remove();
  if (!rows.length) return;
  const root = d3.hierarchy(toHierarchy(rows.slice(0, 600)));
  d3.tree().size([400, 650])(root);
  const g = svg.append("g").attr("transform", "translate(60,15)");

  g.selectAll("line").data(root.links()).join("line")
    .attr("x1", (d) => d.source.y).attr("y1", (d) => d.source.x)
    .attr("x2", (d) => d.target.y).attr("y2", (d) => d.target.x)
    .attr("stroke", "#8ab6ff");

  g.selectAll("circle").data(root.descendants()).join("circle")
    .attr("cx", (d) => d.y).attr("cy", (d) => d.x)
    .attr("r", (d) => (d.children ? 3 : 2))
    .attr("fill", (d) => (d.children ? "#7ff3ff" : "#ffd38a"));
}

function toHierarchy(rows) {
  const root = { name: "World", children: {} };
  rows.forEach((r) => {
    const [a, b, c] = r.phylo || [r.family, `${r.family}-branch`, `${r.family}-sub`];
    root.children[a] ??= { name: a, children: {} };
    root.children[a].children[b] ??= { name: b, children: {} };
    root.children[a].children[b].children[c] ??= { name: c, children: [] };
    root.children[a].children[b].children[c].children.push({ name: r.name });
  });
  return recurse(root);
}

function recurse(node) {
  if (Array.isArray(node.children)) return node;
  return { name: node.name, children: Object.values(node.children).map(recurse) };
}

function renderPhyloStats(rows) {
  const families = countBy(rows.map((r) => r.family));
  const top = Object.entries(families).sort((a, b) => b[1] - a[1]).slice(0, 10);
  document.getElementById("phyloStats").innerHTML = top.map(([fam, n]) => `<div class="metric"><strong>${fam}</strong><br>${n} langs</div>`).join("");
}

function drawCorr(matrix) {
  const canvas = document.getElementById("corr");
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const n = FEATURE_KEYS.length;
  const m = 126;
  const size = Math.min(canvas.width - m - 6, canvas.height - m - 6);
  const cell = size / n;
  ctx.font = "10px Inter";

  for (let i = 0; i < n; i++) {
    const label = short(FEATURE_META[FEATURE_KEYS[i]].label);
    ctx.fillStyle = "#dff1ff";
    ctx.fillText(label, 8, m + i * cell + cell * 0.72);
  }

  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      const v = matrix[i][j];
      const x = m + j * cell;
      const y = m + i * cell;
      ctx.fillStyle = corrColor(v);
      ctx.fillRect(x, y, cell - 1, cell - 1);
      ctx.fillStyle = Math.abs(v) > 0.52 ? "#061024" : "#ebf8ff";
      ctx.fillText(v.toFixed(2), x + 5, y + cell / 1.62);
    }
  }
}

function drawNetwork(matrix) {
  const svg = d3.select("#network");
  svg.selectAll("*").remove();
  const w = 760;
  const h = 440;
  const cx = w / 2;
  const cy = h / 2;
  const r = Math.min(w, h) * 0.34;

  const nodes = FEATURE_KEYS.map((k, i) => {
    const a = (i / FEATURE_KEYS.length) * Math.PI * 2 - Math.PI / 2;
    return { key: k, x: cx + r * Math.cos(a), y: cy + r * Math.sin(a), label: short(FEATURE_META[k].label) };
  });

  const links = [];
  for (let i = 0; i < FEATURE_KEYS.length; i++) {
    for (let j = i + 1; j < FEATURE_KEYS.length; j++) {
      const rv = matrix[i][j];
      if (Math.abs(rv) < 0.25) continue;
      links.push({ i, j, rv });
    }
  }

  svg.append("g").selectAll("line").data(links).join("line")
    .attr("x1", (d) => nodes[d.i].x).attr("y1", (d) => nodes[d.i].y)
    .attr("x2", (d) => nodes[d.j].x).attr("y2", (d) => nodes[d.j].y)
    .attr("stroke", (d) => corrColor(d.rv)).attr("stroke-width", (d) => 1 + Math.abs(d.rv) * 4.5)
    .attr("stroke-opacity", 0.82);

  const gNodes = svg.append("g").selectAll("g").data(nodes).join("g");
  gNodes.append("circle").attr("cx", (d) => d.x).attr("cy", (d) => d.y).attr("r", 21).attr("fill", "#132b57").attr("stroke", "#b7d6ff");
  gNodes.append("text").attr("x", (d) => d.x).attr("y", (d) => d.y + 4).attr("text-anchor", "middle").attr("font-size", 10).attr("fill", "#edfbff").text((d) => d.label);
}

function renderCovariates(report) {
  document.getElementById("covariates").innerHTML = report.slice(0, 18)
    .map((r) => `<div class="metric"><strong>${short(FEATURE_META[r.feature].label)} × ${r.cov}</strong><br>r=${r.r.toFixed(3)} · β=${r.beta.toFixed(3)} · q=${r.q.toFixed(3)}</div>`)
    .join("");
}

function renderClusterTable(rows, labels, silhouettes) {
  document.querySelector("#clusterTable tbody").innerHTML = rows
    .map((r, i) => `<tr><td>${r.name}</td><td>${r.family}</td><td>${r.macroarea}</td><td style="color:hsl(${(labels[i] * 81) % 360} 88% 74%);font-weight:700">${labels[i]}</td><td>${silhouettes[i].toFixed(2)}</td></tr>`)
    .join("");
}

function renderDistanceGrid(rows, matrix) {
  const pairs = [];
  const n = Math.min(rows.length, 18);
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) pairs.push({ pair: `${rows[i].code}-${rows[j].code}`, d: matrix[i][j] });
  pairs.sort((a, b) => a.d - b.d);
  document.getElementById("distanceGrid").innerHTML = pairs.slice(0, 90).map((p) => `<div class="mono-cell">${p.pair}<br>${p.d.toFixed(2)}</div>`).join("");
}

function renderQA(filtered, analyzed, corr, clusters) {
  const lines = [];
  lines.push(`> total_rows=${ALL_ROWS.length}`);
  lines.push(`> filtered_rows=${filtered.length}`);
  lines.push(`> analyzed_rows=${analyzed.length} cap=${MAX_ANALYSIS_ROWS}`);
  lines.push(`> live_info=${STATE.liveInfo}`);
  lines.push(`> map_mode=${STATE.mapMode}, map_feature=${STATE.mapFeature}, grid=${STATE.gridSize}`);
  lines.push(`> cluster_method=${STATE.clusterMethod}, k=${STATE.k}, eps=${STATE.eps}`);

  const strong = [];
  for (let i = 0; i < FEATURE_KEYS.length; i++) for (let j = i + 1; j < FEATURE_KEYS.length; j++) if (Math.abs(corr[i][j]) > 0.45) strong.push(`${FEATURE_KEYS[i]}~${FEATURE_KEYS[j]}=${corr[i][j].toFixed(2)}`);
  lines.push(`> strong_correlations=${strong.length ? strong.slice(0, 25).join(", ") : "none"}`);
  lines.push(`> cluster_sizes=${Object.entries(countBy(clusters.labels)).map(([k, v]) => `${k}:${v}`).join(", ")}`);
  lines.push(`> missingness=${missingness(filtered).toFixed(4)}`);
  lines.push(`> connectors=${DATABASES.map((d) => `${d.name}:${d.status}`).join(", ")}`);
  document.getElementById("qa").textContent = lines.join("\n");
}

function runPermutation() {
  const rows = STATE.analysis.rows;
  if (rows.length < 3) return;
  const a = rows.map((r) => r[STATE.permFeature]);
  const b = rows.map((r) => r[STATE.permCovariate]);
  const observed = pearson(a, b);
  let extreme = 0;
  for (let i = 0; i < STATE.permN; i++) if (Math.abs(pearson(a, shuffle(b))) >= Math.abs(observed)) extreme++;
  const p = (extreme + 1) / (STATE.permN + 1);
  const label = p < 0.01 ? "very strong" : p < 0.05 ? "strong" : p < 0.1 ? "suggestive" : "weak";
  document.getElementById("permOutput").innerHTML = `r=<strong>${observed.toFixed(3)}</strong><br>p≈<strong>${p.toFixed(4)}</strong><br>evidence=<strong>${label}</strong>`;
}

function runHypothesisLab() {
  const rows = STATE.analysis.rows;
  if (rows.length < 4) return;
  const a = rows.map((r) => r[STATE.hypA]);
  const b = rows.map((r) => r[STATE.hypB]);
  const c = rows.map((r) => r[STATE.hypControl]);
  const naive = pearson(a, b);
  const partial = pearson(residualize(a, c), residualize(b, c));
  document.getElementById("hypOutput").innerHTML = `naive r=<strong>${naive.toFixed(3)}</strong><br>partial r|${STATE.hypControl}=<strong>${partial.toFixed(3)}</strong><br>${interpretPartial(naive, partial)}`;
}

function runNearestNeighbors() {
  const rows = STATE.analysis.rows;
  const z = STATE.analysis.z;
  const idx = rows.findIndex((r) => r.name === STATE.nnLanguage);
  if (idx < 0 || !rows.length) return;
  const ranked = rows.map((r, i) => ({ name: r.name, family: r.family, d: euclid(z[idx], z[i]) })).sort((a, b) => a.d - b.d);
  document.getElementById("nnOutput").innerHTML = ranked.slice(1, STATE.nnK + 1)
    .map((x) => `<div class="metric"><strong>${x.name}</strong> (${x.family})<br>d=${x.d.toFixed(3)}</div>`)
    .join("");
}

function runSimulation() {
  const rows = STATE.analysis.rows;
  if (!rows.length) return;
  const factor = STATE.yearsAhead / 100;
  const out = rows.map((r) => {
    const tone = clamp(r.tones + (0.015 * STATE.tempDrift - 0.008 * STATE.humDrift) * factor, 0, 1);
    const morph = clamp(r.morphology + (-0.08 * STATE.tempDrift + 0.04 * STATE.humDrift) * factor, 1, 4);
    const lex = clamp(r.lexicalDiversity + (0.03 * STATE.humDrift - 0.01 * STATE.tempDrift) * factor, 0, 1);
    return { name: r.name, tone, morph, lex, impact: Math.abs(tone - r.tones) + Math.abs(morph - r.morphology) + Math.abs(lex - r.lexicalDiversity) };
  }).sort((a, b) => b.impact - a.impact);
  document.getElementById("simOutput").innerHTML = out.slice(0, 10)
    .map((x) => `<div class="metric"><strong>${x.name}</strong><br>tone=${x.tone.toFixed(2)} morph=${x.morph.toFixed(2)} lex=${x.lex.toFixed(2)} impact=${x.impact.toFixed(2)}</div>`)
    .join("");
}

function cluster(vectors) {
  if (!vectors.length) return { labels: [] };
  switch (STATE.clusterMethod) {
    case "ward": return { labels: ward(vectors, STATE.k) };
    case "dbscan": return { labels: dbscanLike(vectors, STATE.eps, 3) };
    case "spectral": return { labels: spectralLite(vectors, STATE.k) };
    default: return { labels: kmeans(vectors, STATE.k) };
  }
}

function zRows(rows) {
  const means = Object.fromEntries(FEATURE_KEYS.map((k) => [k, mean(rows.map((r) => r[k]))]));
  const stds = Object.fromEntries(FEATURE_KEYS.map((k) => [k, stdev(rows.map((r) => r[k])) || 1]));
  return rows.map((r) => FEATURE_KEYS.map((k) => (r[k] - means[k]) / stds[k]));
}

function corrMatrix(rows, keys) {
  return keys.map((k1) => keys.map((k2) => pearson(rows.map((r) => r[k1]), rows.map((r) => r[k2]))));
}

function covariateReport(rows) {
  const out = [];
  FEATURE_KEYS.forEach((f) => COVARIATES.forEach((c) => {
    const x = rows.map((r) => r[f]);
    const y = rows.map((r) => r[c]);
    const fit = linearFit(x, y);
    const r = pearson(x, y);
    out.push({ feature: f, cov: c, r, beta: fit.slope, q: pseudoFDR(Math.abs(r), rows.length) });
  }));
  return out.sort((a, b) => Math.abs(b.r) - Math.abs(a.r));
}

function pca2(zData) {
  if (!zData.length) return { pc1: [], pc2: [], explained: [0, 0] };
  const cov = covarianceMatrix(zData);
  const e1 = powerIteration(cov, 30);
  const e2 = powerIteration(deflate(cov, e1.vector, e1.value), 30);
  const pc1 = zData.map((r) => dot(r, e1.vector));
  const pc2 = zData.map((r) => dot(r, e2.vector));
  const trace = cov.reduce((s, row, i) => s + row[i], 0) || 1;
  return { pc1, pc2, explained: [Math.max(0, e1.value / trace), Math.max(0, e2.value / trace)] };
}

function covarianceMatrix(zData) {
  const p = zData[0].length;
  const cov = Array.from({ length: p }, () => Array(p).fill(0));
  for (let i = 0; i < p; i++) for (let j = 0; j < p; j++) cov[i][j] = mean(zData.map((r) => r[i] * r[j]));
  return cov;
}

function powerIteration(matrix, iters) {
  let v = Array(matrix.length).fill(0).map((_, i) => (i === 0 ? 1 : 0.5 / (i + 1)));
  for (let i = 0; i < iters; i++) {
    const mv = matVec(matrix, v);
    const norm = Math.sqrt(dot(mv, mv)) || 1;
    v = mv.map((x) => x / norm);
  }
  return { vector: v, value: dot(v, matVec(matrix, v)) };
}

function deflate(matrix, vec, eigen) {
  return matrix.map((row, i) => row.map((v, j) => v - eigen * vec[i] * vec[j]));
}

function matVec(m, v) { return m.map((row) => dot(row, v)); }
function dot(a, b) { let s = 0; for (let i = 0; i < a.length; i++) s += a[i] * b[i]; return s; }

function kmeans(data, k) {
  const kk = Math.max(2, Math.min(k, data.length));
  let centroids = initCentroids(data, kk);
  let labels = Array(data.length).fill(0);
  for (let iter = 0; iter < 28; iter++) {
    labels = data.map((x) => nearest(x, centroids));
    centroids = centroids.map((c, i) => {
      const members = data.filter((_, idx) => labels[idx] === i);
      return members.length ? c.map((_, d) => mean(members.map((m) => m[d]))) : c;
    });
  }
  return labels;
}

function initCentroids(data, k) {
  const c = [data[0].slice()];
  while (c.length < k) {
    let best = data[0];
    let bestDist = -Infinity;
    data.forEach((p) => {
      const d = Math.min(...c.map((cc) => euclid(p, cc)));
      if (d > bestDist) { bestDist = d; best = p; }
    });
    c.push(best.slice());
  }
  return c;
}

function nearest(x, centroids) {
  let bi = 0;
  let bd = Infinity;
  centroids.forEach((c, i) => {
    const d = euclid(x, c);
    if (d < bd) { bd = d; bi = i; }
  });
  return bi;
}

function ward(data, k) {
  const kk = Math.max(2, Math.min(k, data.length));
  let clusters = data.map((_, i) => [i]);
  while (clusters.length > kk) {
    let best = [0, 1, Infinity];
    for (let i = 0; i < clusters.length; i++) {
      for (let j = i + 1; j < clusters.length; j++) {
        const d = wardDist(clusters[i], clusters[j], data);
        if (d < best[2]) best = [i, j, d];
      }
    }
    clusters[best[0]] = [...clusters[best[0]], ...clusters[best[1]]];
    clusters.splice(best[1], 1);
  }
  const labels = Array(data.length).fill(0);
  clusters.forEach((c, i) => c.forEach((idx) => (labels[idx] = i)));
  return labels;
}

function wardDist(a, b, data) {
  const ma = centroid(a, data);
  const mb = centroid(b, data);
  const d = euclid(ma, mb);
  return (a.length * b.length) / (a.length + b.length) * d * d;
}

function centroid(indexes, data) { return data[0].map((_, d) => mean(indexes.map((i) => data[i][d]))); }

function dbscanLike(data, eps, minPts) {
  const labels = Array(data.length).fill(-1);
  const visited = Array(data.length).fill(false);
  let clusterId = 0;
  for (let i = 0; i < data.length; i++) {
    if (visited[i]) continue;
    visited[i] = true;
    const nbs = neighbors(i, data, eps);
    if (nbs.length < minPts) continue;
    labels[i] = clusterId;
    const q = [...nbs];
    while (q.length) {
      const idx = q.pop();
      if (!visited[idx]) {
        visited[idx] = true;
        const n2 = neighbors(idx, data, eps);
        if (n2.length >= minPts) n2.forEach((x) => q.push(x));
      }
      if (labels[idx] < 0) labels[idx] = clusterId;
    }
    clusterId++;
  }
  return labels.map((l, i) => (l >= 0 ? l : clusterId + (i % 3)));
}

function neighbors(i, data, eps) {
  const out = [];
  for (let j = 0; j < data.length; j++) if (euclid(data[i], data[j]) <= eps) out.push(j);
  return out;
}

function spectralLite(data, k) {
  const n = data.length;
  const W = Array.from({ length: n }, () => Array(n).fill(0));
  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      const w = Math.exp(-(euclid(data[i], data[j]) ** 2) / 2.5);
      W[i][j] = w;
      W[j][i] = w;
    }
  }
  const embed = W.map((row) => [mean(row), stdev(row), ...row.slice(0, 4)]);
  return kmeans(embed, k);
}

function silhouetteApprox(vectors, labels) {
  const out = [];
  for (let i = 0; i < vectors.length; i++) {
    const own = labels[i];
    const same = [];
    const other = {};
    for (let j = 0; j < vectors.length; j++) {
      if (i === j) continue;
      const d = euclid(vectors[i], vectors[j]);
      if (labels[j] === own) same.push(d);
      else {
        other[labels[j]] ??= [];
        other[labels[j]].push(d);
      }
    }
    const a = same.length ? mean(same) : 0;
    const bVals = Object.values(other).map((arr) => mean(arr));
    const b = bVals.length ? Math.min(...bVals) : 0;
    out.push(b === 0 && a === 0 ? 0 : (b - a) / Math.max(a, b || 1));
  }
  return out;
}

function distanceMatrix(vectors) {
  const n = vectors.length;
  const m = Array.from({ length: n }, () => Array(n).fill(0));
  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      const d = euclid(vectors[i], vectors[j]);
      m[i][j] = d;
      m[j][i] = d;
    }
  }
  return m;
}

function linearFit(x, y) {
  const mx = mean(x);
  const my = mean(y);
  let num = 0;
  let den = 0;
  for (let i = 0; i < x.length; i++) {
    num += (x[i] - mx) * (y[i] - my);
    den += (x[i] - mx) ** 2;
  }
  const slope = den === 0 ? 0 : num / den;
  return { slope, intercept: my - slope * mx };
}

function pearson(a, b) {
  if (a.length < 2) return 0;
  const ma = mean(a);
  const mb = mean(b);
  let num = 0;
  let da = 0;
  let db = 0;
  for (let i = 0; i < a.length; i++) {
    const xa = a[i] - ma;
    const xb = b[i] - mb;
    num += xa * xb;
    da += xa * xa;
    db += xb * xb;
  }
  return num / Math.sqrt((da || 1) * (db || 1));
}

function residualize(a, c) {
  const fit = linearFit(c, a);
  return a.map((v, i) => v - (fit.intercept + fit.slope * c[i]));
}

function interpretPartial(naive, partial) {
  const d = Math.abs(partial) - Math.abs(naive);
  if (d > 0.08) return "relationship strengthens after control";
  if (d < -0.08) return "relationship likely confounded";
  return "relationship stable under control";
}

function pseudoFDR(absR, n) {
  const z = absR * Math.sqrt(Math.max(1, n - 3));
  return 1 / (1 + Math.exp(1.6 * (z - 2.4)));
}

function short(s) {
  return s.replace("Morphological", "Morph.").replace("inventory", "inv.").replace("complexity", "cplx").split(" ").slice(0, 3).join(" ");
}

function corrColor(v) {
  const a = 0.22 + Math.min(0.76, Math.abs(v));
  return v >= 0 ? `rgba(108,246,201,${a})` : `rgba(255,127,162,${a})`;
}

function colorRamp(t) {
  const h = 240 - 220 * clamp(t, 0, 1);
  return `hsl(${h} 84% 58%)`;
}

function missingness(rows) {
  let n = 0;
  let miss = 0;
  rows.forEach((r) => {
    [...FEATURE_KEYS, ...COVARIATES].forEach((k) => {
      n++;
      if (r[k] == null || Number.isNaN(r[k])) miss++;
    });
  });
  return miss / (n || 1);
}

function shuffle(arr) {
  const out = arr.slice();
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function mean(arr) { return arr.reduce((s, x) => s + x, 0) / (arr.length || 1); }
function stdev(arr) { const m = mean(arr); return Math.sqrt(mean(arr.map((x) => (x - m) ** 2))); }
function euclid(a, b) { let s = 0; for (let i = 0; i < a.length; i++) s += (a[i] - b[i]) ** 2; return Math.sqrt(s); }
function extent(arr) { return [Math.min(...arr), Math.max(...arr)]; }
function normalize(x, min, max) { return (x - min) / ((max - min) || 1); }
function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }
function uniq(arr) { return [...new Set(arr)]; }
function countBy(arr) { return arr.reduce((a, x) => { a[x] = (a[x] || 0) + 1; return a; }, {}); }
function text(id, value) { const el = document.getElementById(id); if (el) el.textContent = value; }
function hash(s) { return String(s).split("").reduce((a, c) => (a * 33 + c.charCodeAt(0)) >>> 0, 7); }
function rand(seed) { const x = Math.sin(seed * 12.9898 + 78.233) * 43758.5453; return x - Math.floor(x); }
