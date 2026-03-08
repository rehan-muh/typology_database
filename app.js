const DATABASES = [
  { name: "WALS", status: "ok", records: 2660, freshness: "2025-Q4" },
  { name: "PHOIBLE", status: "ok", records: 3180, freshness: "2025-Q3" },
  { name: "Glottolog", status: "ok", records: 11120, freshness: "2025-Q4" },
  { name: "AUTOTYP", status: "warn", records: 790, freshness: "2024-Q4" },
  { name: "D-PLACE", status: "ok", records: 1600, freshness: "2025-Q1" },
  { name: "ASJP", status: "ok", records: 5100, freshness: "2025-Q2" },
  { name: "IDS", status: "ok", records: 7020, freshness: "2024-Q3" },
  { name: "Lexibank", status: "ok", records: 8800, freshness: "2025-Q4" },
  { name: "APiCS", status: "ok", records: 350, freshness: "2023-Q4" },
  { name: "SAILS", status: "warn", records: 420, freshness: "2024-Q2" },
  { name: "URIEL", status: "ok", records: 1090, freshness: "2025-Q4" },
  { name: "LAPSyD", status: "down", records: 0, freshness: "offline" }
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
  phonotacticComplexity: { label: "Phonotactic complexity", range: [1, 9] },
  irregularity: { label: "Inflectional irregularity", range: [0, 1] },
  dependencyLength: { label: "Dependency length", range: [1, 8] }
};

const COVARIATES = ["temperature", "humidity", "elevation", "precipitation", "forestCover"];
const FEATURE_KEYS = Object.keys(FEATURE_META);

const BASE_LANGS = [
  mk("Quechua","quy","Quechuan","South America",-13.5,-71.9,[2,0,0,3,2,3,25,8,0,2,3,0.73,6,0.42,5],[11,60,3400,720,24],["Quechuan","Southern","Cusco"]),
  mk("Aymara","aym","Aymaran","South America",-16.5,-68.1,[2,0,0,3,1,3,26,9,0,3,3,0.7,6,0.39,5],[9,49,3600,480,18],["Aymaran","Central","La Paz"]),
  mk("Yoruba","yor","Niger-Congo","Africa",7.5,3.9,[0,1,0,1,1,7,23,0,0,0,2,0.81,4,0.18,3],[28,82,120,1490,56],["Niger-Congo","Defoid","Yoruboid"]),
  mk("Zulu","zul","Niger-Congo","Africa",-29.8,30.9,[0,1,0,2,1,5,33,0,15,0,2,0.76,5,0.21,4],[20,71,420,1010,39],["Niger-Congo","Bantu","Nguni"]),
  mk("Georgian","kat","Kartvelian","Eurasia",42.1,43.5,[1,0,1,3,2,5,33,7,0,1,4,0.62,7,0.46,5],[14,66,450,1090,33],["Kartvelian","Karto-Zan","Georgian"]),
  mk("Japanese","jpn","Japonic","East Asia",36.2,138.2,[2,0,0,2,1,5,23,0,0,0,2,0.71,4,0.34,4],[16,71,438,1670,69],["Japonic","Mainland","Tokyo"]),
  mk("Korean","kor","Koreanic","East Asia",36.6,127.8,[2,0,0,2,1,8,19,0,0,0,2,0.69,5,0.29,4],[14,66,82,1300,63],["Koreanic","Core","Seoul"]),
  mk("Mandarin","cmn","Sino-Tibetan","East Asia",35.9,104.2,[0,1,0,1,0,6,22,0,0,0,2,0.84,4,0.16,3],[15,55,1840,640,34],["Sino-Tibetan","Sinitic","Mandarin"]),
  mk("Maori","mri","Austronesian","Pacific",-38,176,[0,0,0,1,0,5,10,0,0,0,1,0.88,2,0.15,2],[15,76,150,1180,82],["Austronesian","Oceanic","Polynesian"]),
  mk("Tagalog","tgl","Austronesian","Southeast Asia",14.6,121,[0,0,0,1,2,5,17,0,0,1,2,0.81,3,0.25,3],[27,78,16,2050,67],["Austronesian","Malayo-Polynesian","Philippine"]),
  mk("Navajo","nav","Na-Dene","North America",35.9,-109,[2,1,1,3,2,4,33,0,0,1,4,0.66,7,0.41,5],[14,39,2100,285,13],["Na-Dene","Athabaskan","Southern"]),
  mk("Hindi","hin","Indo-European","South Asia",26.8,80.9,[2,0,0,2,1,10,37,2,2,0,3,0.79,6,0.47,5],[27,58,123,920,28],["Indo-European","Indo-Aryan","Central"]),
  mk("Bengali","ben","Indo-European","South Asia",23.8,90.4,[2,0,0,2,1,7,30,4,0,0,2,0.8,5,0.38,4],[26,79,8,1750,42],["Indo-European","Indo-Aryan","Eastern"]),
  mk("Finnish","fin","Uralic","Europe",62.2,25.7,[0,0,0,3,1,8,26,15,0,0,3,0.68,6,0.51,4],[5,73,164,650,76],["Uralic","Finnic","Finnish"]),
  mk("Turkish","tur","Turkic","Eurasia",39,35.2,[2,0,0,2,1,8,29,6,0,0,3,0.72,5,0.44,4],[13,57,1132,590,30],["Turkic","Oghuz","Turkish"]),
  mk("Basque","eus","Basque","Europe",43,-2.7,[1,0,0,2,3,5,24,15,0,0,3,0.67,6,0.48,4],[13,75,289,1420,58],["Basque","Core","Western"]),
  mk("Arabic","arb","Afro-Asiatic","Middle East",24.7,46.7,[1,0,0,2,1,3,28,3,2,0,3,0.75,5,0.43,4],[31,34,612,110,6],["Afro-Asiatic","Semitic","Arabic"]),
  mk("Amharic","amh","Afro-Asiatic","Africa",9,38.7,[1,0,1,2,1,7,32,2,2,0,3,0.74,6,0.45,4],[18,58,2355,1160,25],["Afro-Asiatic","Semitic","Ethiopian"]),
  mk("Swahili","swa","Niger-Congo","Africa",-6.2,39.2,[0,0,0,1,1,5,28,0,12,0,2,0.8,4,0.2,3],[27,79,31,1080,44],["Niger-Congo","Bantu","Sabaki"]),
  mk("Inuktitut","iku","Eskimo-Aleut","Arctic",63.7,-68.5,[2,0,0,4,1,3,21,2,0,0,4,0.63,8,0.56,6],[-8,79,18,420,11],["Eskimo-Aleut","Inuit","Inuktitut"]),
  mk("Warlpiri","wbp","Pama-Nyungan","Australia",-20.5,132.7,[2,0,0,3,2,3,25,8,0,2,3,0.67,7,0.5,5],[29,37,580,420,5],["Pama-Nyungan","Ngumpin-Yapa","Warlpiri"]),
  mk("Samoan","smo","Austronesian","Pacific",-13.8,-171.8,[0,0,0,1,0,5,10,0,0,0,1,0.89,2,0.16,2],[27,80,12,3100,78],["Austronesian","Oceanic","Samoic"]),
  mk("Tzeltal","tzh","Mayan","North America",16.7,-92.6,[2,0,1,2,1,5,25,0,0,1,3,0.72,6,0.37,4],[21,80,1850,2050,65],["Mayan","Tzeltalan","Tzeltal"]),
  mk("Estonian","est","Uralic","Europe",58.6,25,[0,0,0,3,1,9,24,14,0,0,3,0.69,5,0.52,4],[6,75,50,700,74],["Uralic","Finnic","Estonian"]),
  mk("Hungarian","hun","Uralic","Europe",47.1,19.5,[0,0,0,3,1,14,25,18,0,0,3,0.66,6,0.57,5],[11,66,143,650,43],["Uralic","Ugric","Hungarian"])
];

const LANGUAGES = augment(BASE_LANGS, 70);

function mk(name, code, family, macroarea, lat, lon, featureVals, covars, phylo) {
  const row = { name, code, family, macroarea, lat, lon, phylo };
  FEATURE_KEYS.forEach((key, i) => {
    row[key] = featureVals[i];
  });
  row.temperature = covars[0];
  row.humidity = covars[1];
  row.elevation = covars[2];
  row.precipitation = covars[3];
  row.forestCover = covars[4];
  return row;
}

function augment(base, extraCount) {
  const out = [...base];
  const families = [...new Set(base.map((b) => b.family))];
  for (let i = 0; i < extraCount; i++) {
    const b = base[i % base.length];
    const jitter = (n, mag) => +(n + (rand(i * 11 + mag) - 0.5) * mag).toFixed(3);
    const clone = structuredClone(b);
    clone.name = `${b.name}-${i + 1}`;
    clone.code = `${b.code}${String(i + 1).padStart(2, "0")}`;
    clone.family = families[(families.indexOf(b.family) + (i % 3)) % families.length];
    clone.lat = jitter(b.lat, 2.6);
    clone.lon = jitter(b.lon, 4.2);
    FEATURE_KEYS.forEach((k, idx) => {
      const [min, max] = FEATURE_META[k].range;
      const raw = b[k] + (rand(i * 13 + idx) - 0.5) * ((max - min) * 0.2);
      clone[k] = clamp(roundLike(b[k], raw), min, max);
    });
    clone.temperature = clamp(jitter(b.temperature, 5), -15, 40);
    clone.humidity = clamp(jitter(b.humidity, 10), 20, 95);
    clone.elevation = clamp(jitter(b.elevation, 700), 0, 5200);
    clone.precipitation = clamp(jitter(b.precipitation, 500), 30, 3500);
    clone.forestCover = clamp(jitter(b.forestCover, 22), 0, 98);
    out.push(clone);
  }
  return out;
}

function roundLike(example, value) {
  if (Number.isInteger(example)) return Math.round(value);
  return +value.toFixed(2);
}

function rand(seed) {
  const x = Math.sin(seed * 98.37 + 0.731) * 43758.5453;
  return x - Math.floor(x);
}

const STATE = {
  family: "All",
  macroarea: "All",
  minTemp: -15,
  maxHumidity: 95,
  xFeature: "wordOrder",
  yFeature: "morphology",
  colorFeature: "tones",
  sizeFeature: "consonantInventory",
  clusterMethod: "kmeans",
  k: 5,
  eps: 1.5,
  permFeature: "morphology",
  permCovariate: "temperature",
  permN: 800,
  hypA: "morphology",
  hypB: "caseCount",
  hypControl: "temperature",
  nnLanguage: "",
  nnK: 4,
  yearsAhead: 120,
  tempDrift: 2,
  humDrift: 4,
  analysis: null
};

let map;
let layer;

init();

function init() {
  renderDatabasePanel();
  initSelectors();
  initMap();
  bindUI();
  recompute();
}

function bindUI() {
  bind("familyFilter", "change", (e) => {
    STATE.family = e.target.value;
    recompute();
  });
  bind("macroareaFilter", "change", (e) => {
    STATE.macroarea = e.target.value;
    recompute();
  });
  bind("minTemp", "input", (e) => {
    STATE.minTemp = Number(e.target.value);
    text("minTempVal", String(STATE.minTemp));
    recompute();
  });
  bind("maxHumidity", "input", (e) => {
    STATE.maxHumidity = Number(e.target.value);
    text("maxHumidityVal", String(STATE.maxHumidity));
    recompute();
  });

  ["xFeature", "yFeature", "colorFeature", "sizeFeature"].forEach((id) => {
    bind(id, "change", (e) => {
      STATE[id] = e.target.value;
      drawScatter();
      drawMap();
    });
  });

  bind("clusterMethod", "change", (e) => {
    STATE.clusterMethod = e.target.value;
    recompute();
  });
  bind("kClusters", "input", (e) => {
    STATE.k = Number(e.target.value);
    text("kValue", String(STATE.k));
    recompute();
  });
  bind("eps", "input", (e) => {
    STATE.eps = Number(e.target.value);
    text("epsVal", STATE.eps.toFixed(1));
    recompute();
  });

  bind("permFeature", "change", (e) => (STATE.permFeature = e.target.value));
  bind("permCovariate", "change", (e) => (STATE.permCovariate = e.target.value));
  bind("permN", "input", (e) => {
    STATE.permN = Number(e.target.value);
    text("permNVal", String(STATE.permN));
  });
  bind("runPerm", "click", runPermutation);

  bind("hypA", "change", (e) => (STATE.hypA = e.target.value));
  bind("hypB", "change", (e) => (STATE.hypB = e.target.value));
  bind("hypControl", "change", (e) => (STATE.hypControl = e.target.value));
  bind("runHypothesis", "click", runHypothesisLab);

  bind("nnLanguage", "change", (e) => (STATE.nnLanguage = e.target.value));
  bind("nnK", "input", (e) => {
    STATE.nnK = Number(e.target.value);
    text("nnKVal", String(STATE.nnK));
  });
  bind("runNN", "click", runNearestNeighbors);

  bind("yearsAhead", "input", (e) => {
    STATE.yearsAhead = Number(e.target.value);
    text("yearsAheadVal", String(STATE.yearsAhead));
  });
  bind("tempDrift", "input", (e) => {
    STATE.tempDrift = Number(e.target.value);
    text("tempDriftVal", STATE.tempDrift.toFixed(1));
  });
  bind("humDrift", "input", (e) => {
    STATE.humDrift = Number(e.target.value);
    text("humDriftVal", String(STATE.humDrift));
  });
  bind("runSim", "click", runSimulation);

  bind("recompute", "click", recompute);
  bind("exportCsv", "click", exportCsv);
}

function bind(id, evt, fn) {
  document.getElementById(id).addEventListener(evt, fn);
}

function initSelectors() {
  setSelect("familyFilter", ["All", ...uniq(LANGUAGES.map((d) => d.family).sort())]);
  setSelect("macroareaFilter", ["All", ...uniq(LANGUAGES.map((d) => d.macroarea).sort())]);

  const featureOptions = FEATURE_KEYS.map((key) => ({ value: key, label: FEATURE_META[key].label }));
  ["xFeature", "yFeature", "colorFeature", "sizeFeature", "permFeature", "hypA", "hypB"].forEach((id) => {
    setSelectObj(id, featureOptions);
  });

  document.getElementById("xFeature").value = STATE.xFeature;
  document.getElementById("yFeature").value = STATE.yFeature;
  document.getElementById("colorFeature").value = STATE.colorFeature;
  document.getElementById("sizeFeature").value = STATE.sizeFeature;
  document.getElementById("permFeature").value = STATE.permFeature;
  document.getElementById("hypA").value = STATE.hypA;
  document.getElementById("hypB").value = STATE.hypB;

  setSelect("nnLanguage", LANGUAGES.map((l) => l.name));
  STATE.nnLanguage = LANGUAGES[0].name;
}

function setSelect(id, values) {
  document.getElementById(id).innerHTML = values.map((v) => `<option value="${v}">${v}</option>`).join("");
}

function setSelectObj(id, options) {
  document.getElementById(id).innerHTML = options
    .map((o) => `<option value="${o.value}">${o.label}</option>`)
    .join("");
}

function renderDatabasePanel() {
  document.getElementById("dbChips").innerHTML = DATABASES.map((d) => `<span class="chip ${d.status}">${d.name} · ${d.records}</span>`).join("");
  document.getElementById("connectorHealth").innerHTML = DATABASES.map((d) => `${d.name}: ${d.status.toUpperCase()} (${d.freshness})`).join("<br>");
}

function initMap() {
  map = L.map("map", { zoomControl: false }).setView([14, 8], 2);
  L.control.zoom({ position: "bottomright" }).addTo(map);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap"
  }).addTo(map);
  layer = L.layerGroup().addTo(map);
}

function recompute() {
  const rows = filteredRows();
  const z = zRows(rows);
  const corr = corrMatrix(rows, FEATURE_KEYS);
  const clusters = cluster(z);
  const silhouettes = silhouetteApprox(z, clusters.labels);
  const covReport = covariateReport(rows);
  const dist = distanceMatrix(z);
  const pca = pca2(z);

  STATE.analysis = { rows, z, corr, clusters, silhouettes, covReport, dist, pca };

  renderStats(rows);
  drawMap();
  drawScatter();
  drawPhylo(rows);
  drawCorr(corr);
  drawNetwork(corr);
  drawPCA(pca, clusters.labels, rows);
  renderCovariates(covReport);
  renderClusterTable(rows, clusters.labels, silhouettes);
  renderDistanceGrid(rows, dist);
  renderQA(rows, corr, clusters);
}

function filteredRows() {
  return LANGUAGES.filter((r) => {
    const fam = STATE.family === "All" || r.family === STATE.family;
    const area = STATE.macroarea === "All" || r.macroarea === STATE.macroarea;
    const temp = r.temperature >= STATE.minTemp;
    const hum = r.humidity <= STATE.maxHumidity;
    return fam && area && temp && hum;
  });
}

function renderStats(rows) {
  const famCount = uniq(rows.map((r) => r.family)).length;
  const meanTemp = mean(rows.map((r) => r.temperature)).toFixed(1);
  const meanHum = mean(rows.map((r) => r.humidity)).toFixed(1);
  const coverage = ((rows.length / LANGUAGES.length) * 100).toFixed(1);

  document.getElementById("stats").innerHTML = `
    <div class="stat"><strong>${rows.length}</strong><br>languages in current lens</div>
    <div class="stat"><strong>${famCount}</strong><br>families represented</div>
    <div class="stat"><strong>${FEATURE_KEYS.length}</strong><br>feature dimensions</div>
    <div class="stat"><strong>${COVARIATES.length}</strong><br>covariates modeled</div>
    <div class="stat"><strong>${meanTemp}°C</strong><br>mean temperature</div>
    <div class="stat"><strong>${meanHum}%</strong><br>mean humidity</div>
    <div class="stat"><strong>${coverage}%</strong><br>dataset coverage</div>
  `;
}

function drawMap() {
  layer.clearLayers();
  const rows = STATE.analysis.rows;
  if (!rows.length) return;
  const ck = STATE.colorFeature;
  const sk = STATE.sizeFeature;
  const [cMin, cMax] = extent(rows.map((r) => r[ck]));
  const [sMin, sMax] = extent(rows.map((r) => r[sk]));

  rows.forEach((r, i) => {
    const cT = normalize(r[ck], cMin, cMax);
    const sT = normalize(r[sk], sMin, sMax);
    const clusterLabel = STATE.analysis.clusters.labels[i];
    L.circleMarker([r.lat, r.lon], {
      radius: 4 + sT * 7,
      fillColor: colorRamp(cT),
      color: "#fff",
      weight: 0.8,
      fillOpacity: 0.88
    })
      .addTo(layer)
      .bindPopup(`<strong>${r.name}</strong><br>${r.family} · ${r.macroarea}<br>Cluster ${clusterLabel}`);
  });
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
  const h = 460;
  const m = { t: 20, r: 20, b: 54, l: 62 };

  const xVals = rows.map((d) => d[xk]);
  const yVals = rows.map((d) => d[yk]);
  const cVals = rows.map((d) => d[ck]);
  const sVals = rows.map((d) => d[sk]);

  const x = d3.scaleLinear().domain(d3.extent(xVals)).nice().range([m.l, w - m.r]);
  const y = d3.scaleLinear().domain(d3.extent(yVals)).nice().range([h - m.b, m.t]);
  const c = d3.scaleSequential(d3.interpolateTurbo).domain(d3.extent(cVals));
  const s = d3.scaleLinear().domain(d3.extent(sVals)).range([3.2, 10]);

  svg.append("g").attr("transform", `translate(0,${h - m.b})`).call(d3.axisBottom(x));
  svg.append("g").attr("transform", `translate(${m.l},0)`).call(d3.axisLeft(y));

  svg
    .append("g")
    .selectAll("circle")
    .data(rows)
    .join("circle")
    .attr("cx", (d) => x(d[xk]))
    .attr("cy", (d) => y(d[yk]))
    .attr("r", (d) => s(d[sk]))
    .attr("fill", (d) => c(d[ck]))
    .attr("stroke", "#e8f3ff")
    .attr("stroke-width", 0.7)
    .append("title")
    .text((d) => `${d.name} (${d.family})`);

  const fit = linearFit(xVals, yVals);
  const [lx1, lx2] = d3.extent(xVals);
  const ly1 = fit.intercept + fit.slope * lx1;
  const ly2 = fit.intercept + fit.slope * lx2;

  svg
    .append("line")
    .attr("x1", x(lx1))
    .attr("x2", x(lx2))
    .attr("y1", y(ly1))
    .attr("y2", y(ly2))
    .attr("stroke", "#9cfdb9")
    .attr("stroke-width", 2)
    .attr("stroke-dasharray", "5 4");

  svg.append("text").attr("x", w / 2).attr("y", h - 12).attr("text-anchor", "middle").attr("fill", "#eaf8ff").text(FEATURE_META[xk].label);
  svg.append("text").attr("transform", `translate(16,${h / 2}) rotate(-90)`).attr("text-anchor", "middle").attr("fill", "#eaf8ff").text(FEATURE_META[yk].label);

  const r = pearson(xVals, yVals);
  document.getElementById("scatterStats").innerHTML = [
    `N=${rows.length}`,
    `Pearson r=${r.toFixed(3)}`,
    `β=${fit.slope.toFixed(3)}`,
    `Intercept=${fit.intercept.toFixed(3)}`,
    `Size=${FEATURE_META[sk].label}`
  ].map((xv) => `<span class="pill">${xv}</span>`).join("");
}

function drawPhylo(rows) {
  const svg = d3.select("#phylo");
  svg.selectAll("*").remove();
  if (!rows.length) return;

  const rootData = toHierarchy(rows);
  const root = d3.hierarchy(rootData);
  d3.tree().size([400, 650])(root);

  const g = svg.append("g").attr("transform", "translate(60,15)");

  g.selectAll("line")
    .data(root.links())
    .join("line")
    .attr("x1", (d) => d.source.y)
    .attr("y1", (d) => d.source.x)
    .attr("x2", (d) => d.target.y)
    .attr("y2", (d) => d.target.x)
    .attr("stroke", "#88b5ff");

  g.selectAll("circle")
    .data(root.descendants())
    .join("circle")
    .attr("cx", (d) => d.y)
    .attr("cy", (d) => d.x)
    .attr("r", (d) => (d.children ? 3.4 : 2.3))
    .attr("fill", (d) => (d.children ? "#7ef8ff" : "#ffd58e"));

  g.selectAll("text")
    .data(root.descendants().filter((d) => d.depth <= 1 || !d.children))
    .join("text")
    .attr("x", (d) => d.y + 7)
    .attr("y", (d) => d.x + 3)
    .attr("fill", "#eaf7ff")
    .attr("font-size", 10)
    .text((d) => d.data.name);
}

function toHierarchy(rows) {
  const root = { name: "World", children: {} };
  rows.forEach((r) => {
    const [a, b, c] = r.phylo;
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

function drawCorr(matrix) {
  const canvas = document.getElementById("corr");
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const n = FEATURE_KEYS.length;
  const m = 132;
  const size = Math.min(canvas.width - m - 8, canvas.height - m - 8);
  const cell = size / n;

  ctx.font = "11px Inter";
  ctx.fillStyle = "#dcf0ff";

  for (let i = 0; i < n; i++) {
    const label = short(FEATURE_META[FEATURE_KEYS[i]].label);
    ctx.fillText(label, 8, m + i * cell + cell * 0.7);
    ctx.save();
    ctx.translate(m + i * cell + cell * 0.75, m - 7);
    ctx.rotate(-0.56);
    ctx.fillText(label, 0, 0);
    ctx.restore();
  }

  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      const v = matrix[i][j];
      const x = m + j * cell;
      const y = m + i * cell;
      ctx.fillStyle = corrColor(v);
      ctx.fillRect(x, y, cell - 1, cell - 1);
      ctx.fillStyle = Math.abs(v) > 0.52 ? "#051024" : "#e7f8ff";
      ctx.fillText(v.toFixed(2), x + 6, y + cell / 1.65);
    }
  }
}

function drawNetwork(matrix) {
  const svg = d3.select("#network");
  svg.selectAll("*").remove();

  const w = 760;
  const h = 460;
  const cx = w / 2;
  const cy = h / 2;
  const radius = Math.min(w, h) * 0.35;

  const nodes = FEATURE_KEYS.map((k, i) => {
    const a = (i / FEATURE_KEYS.length) * Math.PI * 2 - Math.PI / 2;
    return { key: k, x: cx + radius * Math.cos(a), y: cy + radius * Math.sin(a), label: short(FEATURE_META[k].label) };
  });

  const links = [];
  for (let i = 0; i < FEATURE_KEYS.length; i++) {
    for (let j = i + 1; j < FEATURE_KEYS.length; j++) {
      const r = matrix[i][j];
      if (Math.abs(r) < 0.25) continue;
      links.push({ i, j, r });
    }
  }

  svg.append("g")
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("x1", (d) => nodes[d.i].x)
    .attr("y1", (d) => nodes[d.i].y)
    .attr("x2", (d) => nodes[d.j].x)
    .attr("y2", (d) => nodes[d.j].y)
    .attr("stroke", (d) => corrColor(d.r))
    .attr("stroke-width", (d) => 1.1 + Math.abs(d.r) * 5)
    .attr("stroke-opacity", 0.84);

  const nodeG = svg.append("g").selectAll("g").data(nodes).join("g");
  nodeG.append("circle")
    .attr("cx", (d) => d.x)
    .attr("cy", (d) => d.y)
    .attr("r", 22)
    .attr("fill", "#142d5b")
    .attr("stroke", "#b9d8ff")
    .attr("stroke-width", 1);

  nodeG.append("text")
    .attr("x", (d) => d.x)
    .attr("y", (d) => d.y + 4)
    .attr("text-anchor", "middle")
    .attr("fill", "#ecf8ff")
    .attr("font-size", 10)
    .text((d) => d.label);
}

function drawPCA(pca, labels, rows) {
  const svg = d3.select("#pca");
  svg.selectAll("*").remove();
  if (!rows.length) return;
  const w = 760;
  const h = 440;
  const m = { t: 20, r: 20, b: 48, l: 58 };

  const x = d3.scaleLinear().domain(d3.extent(pca.pc1)).nice().range([m.l, w - m.r]);
  const y = d3.scaleLinear().domain(d3.extent(pca.pc2)).nice().range([h - m.b, m.t]);

  svg.append("g").attr("transform", `translate(0,${h - m.b})`).call(d3.axisBottom(x));
  svg.append("g").attr("transform", `translate(${m.l},0)`).call(d3.axisLeft(y));

  svg.append("g")
    .selectAll("circle")
    .data(rows)
    .join("circle")
    .attr("cx", (_, i) => x(pca.pc1[i]))
    .attr("cy", (_, i) => y(pca.pc2[i]))
    .attr("r", 4.9)
    .attr("fill", (_, i) => `hsl(${(labels[i] * 79) % 360} 84% 67%)`)
    .attr("stroke", "#e9f8ff")
    .attr("stroke-width", 0.8)
    .append("title")
    .text((d) => d.name);

  svg.append("text").attr("x", w / 2).attr("y", h - 10).attr("text-anchor", "middle").attr("fill", "#e7f7ff").text("PC1");
  svg.append("text").attr("transform", `translate(14,${h / 2}) rotate(-90)`).attr("text-anchor", "middle").attr("fill", "#e7f7ff").text("PC2");

  document.getElementById("pcaStats").innerHTML = [
    `Explained PC1 ${(pca.explained[0] * 100).toFixed(1)}%`,
    `Explained PC2 ${(pca.explained[1] * 100).toFixed(1)}%`,
    `Clusters ${uniq(labels).length}`
  ].map((xv) => `<span class="pill">${xv}</span>`).join("");
}

function renderCovariates(report) {
  document.getElementById("covariates").innerHTML = report
    .slice(0, 16)
    .map((r) => `<div class="metric"><strong>${short(FEATURE_META[r.feature].label)} × ${r.cov}</strong><br>r=${r.r.toFixed(3)} · β=${r.beta.toFixed(3)} · q=${r.q.toFixed(3)}</div>`)
    .join("");
}

function renderClusterTable(rows, labels, silhouettes) {
  document.querySelector("#clusterTable tbody").innerHTML = rows
    .map((r, i) => `<tr>
      <td>${r.name}</td>
      <td>${r.family}</td>
      <td>${r.macroarea}</td>
      <td style="color:hsl(${(labels[i] * 79) % 360} 90% 75%);font-weight:700">${labels[i]}</td>
      <td>${silhouettes[i].toFixed(2)}</td>
    </tr>`)
    .join("");
}

function renderDistanceGrid(rows, matrix) {
  const pairs = [];
  const n = Math.min(rows.length, 15);
  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      pairs.push({ pair: `${rows[i].code}-${rows[j].code}`, d: matrix[i][j] });
    }
  }
  pairs.sort((a, b) => a.d - b.d);
  document.getElementById("distanceGrid").innerHTML = pairs.slice(0, 70)
    .map((p) => `<div class="mono-cell">${p.pair}<br>${p.d.toFixed(2)}</div>`)
    .join("");
}

function renderQA(rows, corr, clusters) {
  const lines = [];
  lines.push(`> rows_total=${LANGUAGES.length}`);
  lines.push(`> rows_filtered=${rows.length}`);
  lines.push(`> filters family=${STATE.family}, macroarea=${STATE.macroarea}, minTemp=${STATE.minTemp}, maxHum=${STATE.maxHumidity}`);
  lines.push(`> model cluster=${STATE.clusterMethod}, k=${STATE.k}, eps=${STATE.eps}`);
  lines.push(`> features x=${STATE.xFeature}, y=${STATE.yFeature}, color=${STATE.colorFeature}, size=${STATE.sizeFeature}`);

  const strong = [];
  for (let i = 0; i < FEATURE_KEYS.length; i++) {
    for (let j = i + 1; j < FEATURE_KEYS.length; j++) {
      const r = corr[i][j];
      if (Math.abs(r) > 0.45) strong.push(`${FEATURE_KEYS[i]}~${FEATURE_KEYS[j]}=${r.toFixed(2)}`);
    }
  }
  lines.push(`> strong_corr_pairs=${strong.length ? strong.slice(0, 20).join(", ") : "none"}`);

  const clusterFreq = countBy(clusters.labels);
  lines.push(`> cluster_sizes=${Object.entries(clusterFreq).map(([k, v]) => `${k}:${v}`).join(", ")}`);

  const miss = missingness(rows);
  lines.push(`> missingness=${miss.toFixed(4)}`);

  const conn = DATABASES.map((d) => `${d.name}:${d.status}`).join(", ");
  lines.push(`> connectors=${conn}`);
  document.getElementById("qa").textContent = lines.join("\n");
}

function runPermutation() {
  const rows = STATE.analysis.rows;
  if (rows.length < 3) return;
  const a = rows.map((r) => r[STATE.permFeature]);
  const b = rows.map((r) => r[STATE.permCovariate]);
  const obs = pearson(a, b);

  let extreme = 0;
  for (let i = 0; i < STATE.permN; i++) {
    const p = pearson(a, shuffle(b));
    if (Math.abs(p) >= Math.abs(obs)) extreme++;
  }
  const pVal = (extreme + 1) / (STATE.permN + 1);
  const verdict = pVal < 0.01 ? "very strong" : pVal < 0.05 ? "strong" : pVal < 0.1 ? "suggestive" : "weak";

  document.getElementById("permOutput").innerHTML = `Observed r=<strong>${obs.toFixed(3)}</strong><br>p≈<strong>${pVal.toFixed(4)}</strong><br>evidence=<strong>${verdict}</strong>`;
}

function runHypothesisLab() {
  const rows = STATE.analysis.rows;
  if (rows.length < 4) return;
  const a = rows.map((r) => r[STATE.hypA]);
  const b = rows.map((r) => r[STATE.hypB]);
  const c = rows.map((r) => r[STATE.hypControl]);

  const ar = residualize(a, c);
  const br = residualize(b, c);
  const partial = pearson(ar, br);
  const naive = pearson(a, b);

  document.getElementById("hypOutput").innerHTML = `
    naive r(${short(FEATURE_META[STATE.hypA].label)}, ${short(FEATURE_META[STATE.hypB].label)}) = <strong>${naive.toFixed(3)}</strong><br>
    partial r | ${STATE.hypControl} = <strong>${partial.toFixed(3)}</strong><br>
    interpretation: <strong>${interpretPartial(naive, partial)}</strong>
  `;
}

function runNearestNeighbors() {
  const rows = STATE.analysis.rows;
  const z = STATE.analysis.z;
  const idx = rows.findIndex((r) => r.name === STATE.nnLanguage);
  if (idx < 0 || !rows.length) return;

  const distances = rows.map((r, i) => ({ name: r.name, family: r.family, d: euclid(z[idx], z[i]) }));
  distances.sort((a, b) => a.d - b.d);

  document.getElementById("nnOutput").innerHTML = distances.slice(1, STATE.nnK + 1)
    .map((x) => `<div class="metric"><strong>${x.name}</strong> (${x.family})<br>distance=${x.d.toFixed(3)}</div>`)
    .join("");
}

function runSimulation() {
  const rows = STATE.analysis.rows;
  if (!rows.length) return;
  const years = STATE.yearsAhead;
  const tShift = STATE.tempDrift;
  const hShift = STATE.humDrift;
  const factor = years / 100;

  const predictions = rows.map((r) => {
    const toneShift = 0.015 * tShift * factor - 0.008 * hShift * factor;
    const morphShift = -0.08 * tShift * factor + 0.04 * hShift * factor;
    const lexShift = 0.03 * hShift * factor - 0.01 * tShift * factor;
    const tone = clamp(r.tones + toneShift, 0, 1);
    const morph = clamp(r.morphology + morphShift, 1, 4);
    const lex = clamp(r.lexicalDiversity + lexShift, 0, 1);
    return {
      name: r.name,
      tone,
      morph,
      lex,
      delta: Math.abs(tone - r.tones) + Math.abs(morph - r.morphology) + Math.abs(lex - r.lexicalDiversity)
    };
  }).sort((a, b) => b.delta - a.delta);

  document.getElementById("simOutput").innerHTML = predictions.slice(0, 8)
    .map((p) => `<div class="metric"><strong>${p.name}</strong><br>Δtone=${(p.tone).toFixed(2)} Δmorph=${(p.morph).toFixed(2)} Δlex=${(p.lex).toFixed(2)} | impact=${p.delta.toFixed(2)}</div>`)
    .join("");
}

function exportCsv() {
  const rows = STATE.analysis.rows;
  const cols = ["name", "code", "family", "macroarea", ...FEATURE_KEYS, ...COVARIATES];
  const csv = [cols.join(","), ...rows.map((r) => cols.map((c) => String(r[c])).join(","))].join("\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "typoverse-current-view.csv";
  a.click();
  URL.revokeObjectURL(url);
}

function cluster(vectors) {
  if (!vectors.length) return { labels: [] };
  switch (STATE.clusterMethod) {
    case "ward":
      return { labels: ward(vectors, STATE.k) };
    case "dbscan":
      return { labels: dbscanLike(vectors, STATE.eps, 3) };
    case "spectral":
      return { labels: spectralLite(vectors, STATE.k) };
    default:
      return { labels: kmeans(vectors, STATE.k) };
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
  const all = [];
  FEATURE_KEYS.forEach((f) => {
    COVARIATES.forEach((c) => {
      const x = rows.map((r) => r[f]);
      const y = rows.map((r) => r[c]);
      const lf = linearFit(x, y);
      const r = pearson(x, y);
      const q = pseudoFDR(Math.abs(r), rows.length);
      all.push({ feature: f, cov: c, r, beta: lf.slope, q });
    });
  });
  return all.sort((a, b) => Math.abs(b.r) - Math.abs(a.r));
}

function pca2(zData) {
  if (!zData.length) return { pc1: [], pc2: [], explained: [0, 0] };
  const cov = covarianceMatrix(zData);
  const eig1 = powerIteration(cov, 30);
  const covDeflated = deflate(cov, eig1.vector, eig1.value);
  const eig2 = powerIteration(covDeflated, 30);

  const pc1 = zData.map((row) => dot(row, eig1.vector));
  const pc2 = zData.map((row) => dot(row, eig2.vector));
  const trace = cov.reduce((s, row, i) => s + row[i], 0) || 1;
  return { pc1, pc2, explained: [Math.max(0, eig1.value / trace), Math.max(0, eig2.value / trace)] };
}

function covarianceMatrix(zData) {
  const p = zData[0].length;
  const cov = Array.from({ length: p }, () => Array(p).fill(0));
  for (let i = 0; i < p; i++) {
    for (let j = 0; j < p; j++) {
      cov[i][j] = mean(zData.map((r) => r[i] * r[j]));
    }
  }
  return cov;
}

function powerIteration(matrix, iters) {
  let v = Array(matrix.length).fill(0).map((_, i) => (i === 0 ? 1 : 0.5 / (i + 1)));
  for (let i = 0; i < iters; i++) {
    const mv = matVec(matrix, v);
    const norm = Math.sqrt(dot(mv, mv)) || 1;
    v = mv.map((x) => x / norm);
  }
  const lambda = dot(v, matVec(matrix, v));
  return { vector: v, value: lambda };
}

function deflate(matrix, vec, eigen) {
  return matrix.map((row, i) => row.map((v, j) => v - eigen * vec[i] * vec[j]));
}

function matVec(mat, vec) {
  return mat.map((row) => dot(row, vec));
}

function dot(a, b) {
  let s = 0;
  for (let i = 0; i < a.length; i++) s += a[i] * b[i];
  return s;
}

function kmeans(data, k) {
  const kk = Math.max(2, Math.min(k, data.length));
  let centroids = initCentroids(data, kk);
  let labels = Array(data.length).fill(0);
  for (let t = 0; t < 40; t++) {
    labels = data.map((x) => nearest(x, centroids));
    centroids = centroids.map((c, i) => {
      const members = data.filter((_, idx) => labels[idx] === i);
      if (!members.length) return c;
      return c.map((_, d) => mean(members.map((m) => m[d])));
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
      if (d > bestDist) {
        bestDist = d;
        best = p;
      }
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
    if (d < bd) {
      bd = d;
      bi = i;
    }
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

function centroid(indexes, data) {
  return data[0].map((_, d) => mean(indexes.map((i) => data[i][d])));
}

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
    const queue = [...nbs];
    while (queue.length) {
      const q = queue.pop();
      if (!visited[q]) {
        visited[q] = true;
        const qn = neighbors(q, data, eps);
        if (qn.length >= minPts) qn.forEach((x) => queue.push(x));
      }
      if (labels[q] < 0) labels[q] = clusterId;
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
      const d = euclid(data[i], data[j]);
      const w = Math.exp(-(d * d) / 2.2);
      W[i][j] = w;
      W[j][i] = w;
    }
  }
  const embed = W.map((row) => [mean(row), stdev(row), ...row.slice(0, 3)]);
  return kmeans(embed, k);
}

function silhouetteApprox(vectors, labels) {
  const out = [];
  for (let i = 0; i < vectors.length; i++) {
    const own = labels[i];
    const within = [];
    const other = {};
    for (let j = 0; j < vectors.length; j++) {
      if (i === j) continue;
      const d = euclid(vectors[i], vectors[j]);
      if (labels[j] === own) within.push(d);
      else {
        other[labels[j]] ??= [];
        other[labels[j]].push(d);
      }
    }
    const a = within.length ? mean(within) : 0;
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

function residualize(a, control) {
  const fit = linearFit(control, a);
  return a.map((v, i) => v - (fit.intercept + fit.slope * control[i]));
}

function interpretPartial(naive, partial) {
  const d = Math.abs(partial) - Math.abs(naive);
  if (d > 0.08) return "relationship strengthens after control";
  if (d < -0.08) return "relationship likely confounded";
  return "relationship stable under control";
}

function pseudoFDR(absR, n) {
  const z = absR * Math.sqrt(Math.max(1, n - 3));
  return 1 / (1 + Math.exp(1.6 * (z - 2.3)));
}

function short(label) {
  return label
    .replace("Morphological", "Morph.")
    .replace("inventory", "inv.")
    .replace("complexity", "cplx")
    .replace("dependency", "dep.")
    .split(" ")
    .slice(0, 3)
    .join(" ");
}

function corrColor(v) {
  const a = 0.22 + Math.min(0.76, Math.abs(v));
  if (v >= 0) return `rgba(108,246,201,${a})`;
  return `rgba(255,127,162,${a})`;
}

function colorRamp(t) {
  const hue = 240 - 220 * t;
  return `hsl(${hue} 84% 58%)`;
}

function missingness(rows) {
  let n = 0;
  let miss = 0;
  rows.forEach((r) => {
    [...FEATURE_KEYS, ...COVARIATES].forEach((k) => {
      n += 1;
      if (r[k] === null || r[k] === undefined || Number.isNaN(r[k])) miss += 1;
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

function mean(arr) {
  return arr.reduce((s, x) => s + x, 0) / (arr.length || 1);
}

function stdev(arr) {
  const m = mean(arr);
  return Math.sqrt(mean(arr.map((x) => (x - m) ** 2)));
}

function euclid(a, b) {
  let s = 0;
  for (let i = 0; i < a.length; i++) s += (a[i] - b[i]) ** 2;
  return Math.sqrt(s);
}

function extent(arr) {
  return [Math.min(...arr), Math.max(...arr)];
}

function normalize(x, min, max) {
  return (x - min) / ((max - min) || 1);
}

function clamp(v, min, max) {
  return Math.max(min, Math.min(max, v));
}

function uniq(arr) {
  return [...new Set(arr)];
}

function countBy(arr) {
  return arr.reduce((acc, x) => {
    acc[x] = (acc[x] || 0) + 1;
    return acc;
  }, {});
}

function text(id, value) {
  document.getElementById(id).textContent = value;
}
