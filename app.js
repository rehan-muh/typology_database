const DATABASES = [
  { name: "WALS", status: "ok", features: 190 },
  { name: "PHOIBLE", status: "ok", features: 2411 },
  { name: "Glottolog", status: "ok", features: 58 },
  { name: "AUTOTYP", status: "warn", features: 540 },
  { name: "D-PLACE", status: "ok", features: 114 },
  { name: "ASJP", status: "ok", features: 40 },
  { name: "IDS", status: "ok", features: 1310 },
  { name: "Lexibank", status: "ok", features: 2800 },
  { name: "APiCS", status: "ok", features: 130 },
  { name: "SAILS", status: "warn", features: 210 },
  { name: "URIEL", status: "ok", features: 420 }
];

const FEATURE_META = {
  wordOrder: { label: "Word order index", min: 0, max: 2 },
  tones: { label: "Tonality", min: 0, max: 1 },
  ejectives: { label: "Ejectives", min: 0, max: 1 },
  morphology: { label: "Morphological synthesis", min: 1, max: 4 },
  alignment: { label: "Alignment complexity", min: 0, max: 3 },
  vowelInventory: { label: "Vowel inventory size", min: 3, max: 14 },
  consonantInventory: { label: "Consonant inventory size", min: 12, max: 60 },
  caseCount: { label: "Case count", min: 0, max: 18 },
  genders: { label: "Gender classes", min: 0, max: 6 },
  evidentiality: { label: "Evidentiality richness", min: 0, max: 4 },
  syllableComplexity: { label: "Syllable complexity", min: 1, max: 5 },
  lexicalDiversity: { label: "Lexical diversity index", min: 0, max: 1 }
};

const COVARIATES = ["temperature", "humidity", "elevation", "precipitation"];
const FEATURE_KEYS = Object.keys(FEATURE_META);

const LANGUAGES = [
  row("Quechua", "quy", "Quechuan", "South America", -13.5, -71.9, [2, 0, 0, 3, 2, 3, 25, 8, 0, 2, 3, 0.74], [11, 60, 3400, 720], ["Quechuan", "Southern", "Cusco-Collao"]),
  row("Aymara", "aym", "Aymaran", "South America", -16.5, -68.1, [2, 0, 0, 3, 1, 3, 26, 9, 0, 3, 3, 0.71], [9, 49, 3600, 480], ["Aymaran", "Central", "La Paz"]),
  row("Yoruba", "yor", "Niger-Congo", "Africa", 7.5, 3.9, [0, 1, 0, 1, 1, 7, 23, 0, 0, 0, 2, 0.82], [28, 82, 120, 1490], ["Niger-Congo", "Defoid", "Yoruboid"]),
  row("Zulu", "zul", "Niger-Congo", "Africa", -29.8, 30.9, [0, 1, 0, 2, 1, 5, 33, 0, 15, 0, 2, 0.77], [20, 71, 420, 1010], ["Niger-Congo", "Bantu", "Nguni"]),
  row("Georgian", "kat", "Kartvelian", "Eurasia", 42.1, 43.5, [1, 0, 1, 3, 2, 5, 33, 7, 0, 1, 4, 0.63], [14, 66, 450, 1090], ["Kartvelian", "Karto-Zan", "Georgian"]),
  row("Armenian", "hye", "Indo-European", "Eurasia", 40.2, 44.5, [1, 0, 0, 2, 2, 6, 31, 7, 0, 0, 3, 0.68], [13, 58, 970, 560], ["Indo-European", "Armenian", "Eastern"]),
  row("Japanese", "jpn", "Japonic", "East Asia", 36.2, 138.2, [2, 0, 0, 2, 1, 5, 23, 0, 0, 0, 2, 0.72], [16, 71, 438, 1670], ["Japonic", "Mainland", "Tokyo"]),
  row("Korean", "kor", "Koreanic", "East Asia", 36.6, 127.8, [2, 0, 0, 2, 1, 8, 19, 0, 0, 0, 2, 0.7], [14, 66, 82, 1300], ["Koreanic", "Core", "Seoul"]),
  row("Mandarin", "cmn", "Sino-Tibetan", "East Asia", 35.9, 104.2, [0, 1, 0, 1, 0, 6, 22, 0, 0, 0, 2, 0.84], [15, 55, 1840, 640], ["Sino-Tibetan", "Sinitic", "Mandarin"]),
  row("Maori", "mri", "Austronesian", "Pacific", -38.0, 176.0, [0, 0, 0, 1, 0, 5, 10, 0, 0, 0, 1, 0.88], [15, 76, 150, 1180], ["Austronesian", "Oceanic", "Polynesian"]),
  row("Tagalog", "tgl", "Austronesian", "Southeast Asia", 14.6, 121.0, [0, 0, 0, 1, 2, 5, 17, 0, 0, 1, 2, 0.81], [27, 78, 16, 2050], ["Austronesian", "Malayo-Polynesian", "Philippine"]),
  row("Nahuatl", "nhn", "Uto-Aztecan", "North America", 19.4, -98.2, [0, 0, 0, 2, 1, 4, 24, 0, 0, 1, 2, 0.75], [19, 68, 2240, 820], ["Uto-Aztecan", "Southern", "Central Nahuan"]),
  row("Navajo", "nav", "Na-Dene", "North America", 35.9, -109.0, [2, 1, 1, 3, 2, 4, 33, 0, 0, 1, 4, 0.67], [14, 39, 2100, 285], ["Na-Dene", "Athabaskan", "Southern"]),
  row("Hindi", "hin", "Indo-European", "South Asia", 26.8, 80.9, [2, 0, 0, 2, 1, 10, 37, 2, 2, 0, 3, 0.78], [27, 58, 123, 920], ["Indo-European", "Indo-Aryan", "Central"]),
  row("Bengali", "ben", "Indo-European", "South Asia", 23.8, 90.4, [2, 0, 0, 2, 1, 7, 30, 4, 0, 0, 2, 0.79], [26, 79, 8, 1750], ["Indo-European", "Indo-Aryan", "Eastern"]),
  row("Finnish", "fin", "Uralic", "Europe", 62.2, 25.7, [0, 0, 0, 3, 1, 8, 26, 15, 0, 0, 3, 0.69], [5, 73, 164, 650], ["Uralic", "Finnic", "Finnish"]),
  row("Turkish", "tur", "Turkic", "Eurasia", 39.0, 35.2, [2, 0, 0, 2, 1, 8, 29, 6, 0, 0, 3, 0.73], [13, 57, 1132, 590], ["Turkic", "Oghuz", "Turkish"]),
  row("Basque", "eus", "Basque", "Europe", 43.0, -2.7, [1, 0, 0, 2, 3, 5, 24, 15, 0, 0, 3, 0.66], [13, 75, 289, 1420], ["Basque", "Core", "Western"]),
  row("Arabic", "arb", "Afro-Asiatic", "Middle East", 24.7, 46.7, [1, 0, 0, 2, 1, 3, 28, 3, 2, 0, 3, 0.76], [31, 34, 612, 110], ["Afro-Asiatic", "Semitic", "Arabic"]),
  row("Amharic", "amh", "Afro-Asiatic", "Africa", 9.0, 38.7, [1, 0, 1, 2, 1, 7, 32, 2, 2, 0, 3, 0.74], [18, 58, 2355, 1160], ["Afro-Asiatic", "Semitic", "Ethiopian"]),
  row("Swahili", "swa", "Niger-Congo", "Africa", -6.2, 39.2, [0, 0, 0, 1, 1, 5, 28, 0, 12, 0, 2, 0.8], [27, 79, 31, 1080], ["Niger-Congo", "Bantu", "Sabaki"]),
  row("Tzeltal", "tzh", "Mayan", "North America", 16.7, -92.6, [2, 0, 1, 2, 1, 5, 25, 0, 0, 1, 3, 0.72], [21, 80, 1850, 2050], ["Mayan", "Tzeltalan", "Tzeltal"]),
  row("Inuktitut", "iku", "Eskimo-Aleut", "Arctic", 63.7, -68.5, [2, 0, 0, 4, 1, 3, 21, 2, 0, 0, 4, 0.64], [-8, 79, 18, 420], ["Eskimo-Aleut", "Inuit", "Inuktitut"]),
  row("Dyirbal", "dbl", "Pama-Nyungan", "Australia", -17.5, 145.4, [2, 0, 0, 2, 3, 3, 20, 4, 4, 1, 2, 0.7], [25, 74, 74, 1700], ["Pama-Nyungan", "Dyirbalic", "Dyirbal"]),
  row("Warlpiri", "wbp", "Pama-Nyungan", "Australia", -20.5, 132.7, [2, 0, 0, 3, 2, 3, 25, 8, 0, 2, 3, 0.68], [29, 37, 580, 420], ["Pama-Nyungan", "Ngumpin-Yapa", "Warlpiri"]),
  row("Samoan", "smo", "Austronesian", "Pacific", -13.8, -171.8, [0, 0, 0, 1, 0, 5, 10, 0, 0, 0, 1, 0.87], [27, 80, 12, 3100], ["Austronesian", "Oceanic", "Samoic"])
];

function row(name, code, family, macroarea, lat, lon, featureVals, covariates, phylo) {
  const payload = {
    name,
    code,
    family,
    macroarea,
    lat,
    lon,
    phylo
  };

  FEATURE_KEYS.forEach((k, i) => {
    payload[k] = featureVals[i];
  });

  payload.temperature = covariates[0];
  payload.humidity = covariates[1];
  payload.elevation = covariates[2];
  payload.precipitation = covariates[3];
  return payload;
}

const STATE = {
  family: "All",
  macroarea: "All",
  xFeature: "wordOrder",
  yFeature: "morphology",
  colorFeature: "tones",
  clusterMethod: "kmeans",
  k: 4,
  eps: 1.4,
  selectedPermFeature: "morphology",
  selectedPermCovariate: "temperature",
  permN: 400,
  analysis: null
};

let map;
let markerLayer;

init();

function init() {
  renderDatabaseChips();
  renderStaticSelectors();
  renderStats(LANGUAGES);
  initMap();
  bindEvents();
  recompute();
}

function bindEvents() {
  bind("familyFilter", "change", (e) => {
    STATE.family = e.target.value;
    recompute();
  });
  bind("macroareaFilter", "change", (e) => {
    STATE.macroarea = e.target.value;
    recompute();
  });
  bind("xFeature", "change", (e) => {
    STATE.xFeature = e.target.value;
    renderScatter(STATE.analysis.filtered);
  });
  bind("yFeature", "change", (e) => {
    STATE.yFeature = e.target.value;
    renderScatter(STATE.analysis.filtered);
  });
  bind("colorFeature", "change", (e) => {
    STATE.colorFeature = e.target.value;
    renderScatter(STATE.analysis.filtered);
    refreshMap();
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
  bind("densityEps", "input", (e) => {
    STATE.eps = Number(e.target.value);
    text("epsValue", STATE.eps.toFixed(1));
    recompute();
  });
  bind("permFeature", "change", (e) => {
    STATE.selectedPermFeature = e.target.value;
  });
  bind("permCovariate", "change", (e) => {
    STATE.selectedPermCovariate = e.target.value;
  });
  bind("permN", "input", (e) => {
    STATE.permN = Number(e.target.value);
    text("permNVal", String(STATE.permN));
  });
  bind("runPermBtn", "click", () => runPermutation());
  bind("rerunBtn", "click", () => recompute());
}

function bind(id, event, fn) {
  document.getElementById(id).addEventListener(event, fn);
}

function recompute() {
  const filtered = applyFilters(LANGUAGES);
  const zRows = zscoreRows(filtered, FEATURE_KEYS);
  const corrMatrix = correlationMatrix(filtered, FEATURE_KEYS);
  const clusters = computeClusters(zRows);
  const silhouettes = approximateSilhouette(zRows, clusters.labels);
  const covariance = covariateReport(filtered);
  const dist = distanceMatrix(zRows).slice(0, 12);

  STATE.analysis = {
    filtered,
    zRows,
    corrMatrix,
    clusters,
    silhouettes,
    covariance,
    dist
  };

  renderStats(filtered);
  refreshMap();
  renderTree(filtered);
  renderScatter(filtered);
  renderCorrCanvas(corrMatrix);
  renderFeatureNetwork(corrMatrix);
  renderCovariates(covariance);
  renderClusterTable(filtered, clusters.labels, silhouettes);
  renderDistanceMatrix(filtered.slice(0, 12), dist);
  renderLog(filtered, corrMatrix, clusters);
}

function applyFilters(rows) {
  return rows.filter((r) => {
    const fam = STATE.family === "All" || r.family === STATE.family;
    const area = STATE.macroarea === "All" || r.macroarea === STATE.macroarea;
    return fam && area;
  });
}

function renderStaticSelectors() {
  const families = ["All", ...new Set(LANGUAGES.map((d) => d.family).sort())];
  const macroareas = ["All", ...new Set(LANGUAGES.map((d) => d.macroarea).sort())];

  setOptions("familyFilter", families);
  setOptions("macroareaFilter", macroareas);

  const featureOpts = FEATURE_KEYS.map((k) => `<option value="${k}">${FEATURE_META[k].label}</option>`).join("");
  ["xFeature", "yFeature", "colorFeature", "permFeature"].forEach((id) => {
    document.getElementById(id).innerHTML = featureOpts;
  });

  document.getElementById("xFeature").value = STATE.xFeature;
  document.getElementById("yFeature").value = STATE.yFeature;
  document.getElementById("colorFeature").value = STATE.colorFeature;
  document.getElementById("permFeature").value = STATE.selectedPermFeature;
}

function setOptions(id, values) {
  document.getElementById(id).innerHTML = values.map((v) => `<option value="${v}">${v}</option>`).join("");
}

function renderDatabaseChips() {
  const chips = DATABASES.map((d) => `<span class="db-chip ${d.status}">${d.name} · ${d.features}</span>`).join("");
  document.getElementById("dbChips").innerHTML = chips;
}

function renderStats(rows) {
  const avgTemp = mean(rows.map((r) => r.temperature)).toFixed(1);
  const famCount = new Set(rows.map((r) => r.family)).size;
  const covCount = COVARIATES.length;

  document.getElementById("stats").innerHTML = `
    <div class="stat"><strong>${rows.length}</strong><br/>languages in view</div>
    <div class="stat"><strong>${famCount}</strong><br/>families represented</div>
    <div class="stat"><strong>${FEATURE_KEYS.length}</strong><br/>feature axes active</div>
    <div class="stat"><strong>${covCount}</strong><br/>covariates modeled</div>
    <div class="stat"><strong>${avgTemp}°C</strong><br/>mean climate temperature</div>
  `;
}

function initMap() {
  map = L.map("map", { zoomControl: false }).setView([16, 10], 2);
  L.control.zoom({ position: "bottomright" }).addTo(map);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors"
  }).addTo(map);
  markerLayer = L.layerGroup().addTo(map);
}

function refreshMap() {
  markerLayer.clearLayers();
  const rows = STATE.analysis.filtered;
  const f = STATE.colorFeature;
  const [minV, maxV] = extent(rows.map((r) => r[f]));

  rows.forEach((row, i) => {
    const t = normalize(row[f], minV, maxV || minV + 1);
    const color = gradientColor(t);
    const cluster = STATE.analysis.clusters.labels[i];
    const marker = L.circleMarker([row.lat, row.lon], {
      radius: 5 + Math.max(0, (row.morphology - 1) * 1.2),
      color: "#ffffff",
      weight: 1,
      fillColor: color,
      fillOpacity: 0.88
    });
    marker
      .addTo(markerLayer)
      .bindPopup(
        `<strong>${row.name}</strong><br>${row.family} · ${row.macroarea}<br>Cluster: ${cluster}<br>${FEATURE_META[f].label}: ${row[f]}`
      );
  });
}

function renderScatter(rows) {
  const svg = d3.select("#featureScatter");
  svg.selectAll("*").remove();

  const xk = STATE.xFeature;
  const yk = STATE.yFeature;
  const ck = STATE.colorFeature;

  const width = 700;
  const height = 440;
  const margin = { top: 20, right: 20, bottom: 54, left: 62 };
  const xVals = rows.map((r) => r[xk]);
  const yVals = rows.map((r) => r[yk]);

  const xScale = d3
    .scaleLinear()
    .domain(d3.extent(xVals))
    .nice()
    .range([margin.left, width - margin.right]);

  const yScale = d3
    .scaleLinear()
    .domain(d3.extent(yVals))
    .nice()
    .range([height - margin.bottom, margin.top]);

  const colorScale = d3.scaleSequential(d3.interpolateTurbo).domain(d3.extent(rows.map((r) => r[ck])));

  svg.append("g").attr("transform", `translate(0,${height - margin.bottom})`).call(d3.axisBottom(xScale));
  svg.append("g").attr("transform", `translate(${margin.left},0)`).call(d3.axisLeft(yScale));

  svg
    .append("g")
    .selectAll("circle")
    .data(rows)
    .join("circle")
    .attr("cx", (d) => xScale(d[xk]))
    .attr("cy", (d) => yScale(d[yk]))
    .attr("r", 5.1)
    .attr("fill", (d) => colorScale(d[ck]))
    .attr("stroke", "#dfefff")
    .attr("stroke-width", 0.8)
    .append("title")
    .text((d) => `${d.name} (${d.family})`);

  const fit = linearFit(xVals, yVals);
  const xLine = d3.extent(xVals);
  const yLine = xLine.map((x) => fit.intercept + fit.slope * x);

  svg
    .append("line")
    .attr("x1", xScale(xLine[0]))
    .attr("x2", xScale(xLine[1]))
    .attr("y1", yScale(yLine[0]))
    .attr("y2", yScale(yLine[1]))
    .attr("stroke", "#9effb6")
    .attr("stroke-width", 2.2)
    .attr("stroke-dasharray", "5 4");

  svg
    .append("text")
    .attr("x", width / 2)
    .attr("y", height - 12)
    .attr("text-anchor", "middle")
    .attr("fill", "#e7f7ff")
    .text(FEATURE_META[xk].label);

  svg
    .append("text")
    .attr("transform", `translate(16,${height / 2}) rotate(-90)`)
    .attr("text-anchor", "middle")
    .attr("fill", "#e7f7ff")
    .text(FEATURE_META[yk].label);

  const pear = pearson(xVals, yVals);
  const stats = [
    `N = ${rows.length}`,
    `Pearson r = ${pear.toFixed(3)}`,
    `Slope = ${fit.slope.toFixed(3)}`,
    `Intercept = ${fit.intercept.toFixed(3)}`
  ];

  document.getElementById("scatterStats").innerHTML = stats.map((s) => `<span class="pill">${s}</span>`).join("");
}

function renderTree(rows) {
  const nested = treeFromRows(rows);
  const root = d3.hierarchy(nested);
  const layout = d3.tree().size([400, 640]);
  layout(root);

  const svg = d3.select("#tree");
  svg.selectAll("*").remove();
  const g = svg.append("g").attr("transform", "translate(60,15)");

  g
    .selectAll("line")
    .data(root.links())
    .join("line")
    .attr("x1", (d) => d.source.y)
    .attr("y1", (d) => d.source.x)
    .attr("x2", (d) => d.target.y)
    .attr("y2", (d) => d.target.x)
    .attr("stroke", "#87b3ff");

  g
    .selectAll("circle")
    .data(root.descendants())
    .join("circle")
    .attr("cx", (d) => d.y)
    .attr("cy", (d) => d.x)
    .attr("r", (d) => (d.children ? 3.5 : 2.7))
    .attr("fill", (d) => (d.children ? "#79f4ff" : "#ffd37f"));

  g
    .selectAll("text")
    .data(root.descendants().filter((d) => d.depth < 2 || !d.children))
    .join("text")
    .attr("x", (d) => d.y + 7)
    .attr("y", (d) => d.x + 3)
    .attr("font-size", 10)
    .attr("fill", "#e8f6ff")
    .text((d) => d.data.name);
}

function treeFromRows(rows) {
  const root = { name: "World", children: {} };

  rows.forEach((row) => {
    const [a, b, c] = row.phylo;
    if (!root.children[a]) root.children[a] = { name: a, children: {} };
    if (!root.children[a].children[b]) root.children[a].children[b] = { name: b, children: {} };
    if (!root.children[a].children[b].children[c]) root.children[a].children[b].children[c] = { name: c, children: [] };
    root.children[a].children[b].children[c].children.push({ name: row.name });
  });

  return toHierarchy(root);
}

function toHierarchy(node) {
  if (Array.isArray(node.children)) return node;
  return {
    name: node.name,
    children: Object.values(node.children).map((child) => toHierarchy(child))
  };
}

function renderCorrCanvas(matrix) {
  const canvas = document.getElementById("corrCanvas");
  const ctx = canvas.getContext("2d");
  const n = FEATURE_KEYS.length;
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const margin = 130;
  const size = Math.min(canvas.width - margin - 10, canvas.height - margin - 10);
  const cell = size / n;

  ctx.fillStyle = "#dff1ff";
  ctx.font = "11px Inter";

  for (let i = 0; i < n; i++) {
    const y = margin + i * cell;
    const x = margin + i * cell;
    ctx.fillText(shortLabel(FEATURE_META[FEATURE_KEYS[i]].label), 8, y + cell * 0.7);
    ctx.save();
    ctx.translate(x + cell * 0.7, margin - 8);
    ctx.rotate(-0.55);
    ctx.fillText(shortLabel(FEATURE_META[FEATURE_KEYS[i]].label), 0, 0);
    ctx.restore();
  }

  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      const v = matrix[i][j];
      const x = margin + j * cell;
      const y = margin + i * cell;
      ctx.fillStyle = corrColor(v);
      ctx.fillRect(x, y, cell - 1, cell - 1);
      ctx.fillStyle = Math.abs(v) > 0.47 ? "#001022" : "#e6f5ff";
      ctx.fillText(v.toFixed(2), x + 6, y + cell / 1.6);
    }
  }

  document.getElementById("coOccurrenceLegend").innerHTML = [
    "r ≈ -1 strong inverse",
    "r ≈ 0 weak",
    "r ≈ +1 strong positive"
  ]
    .map((t) => `<span class="pill">${t}</span>`)
    .join("");
}

function renderFeatureNetwork(matrix) {
  const svg = d3.select("#network");
  svg.selectAll("*").remove();

  const width = 720;
  const height = 420;
  const centerX = width / 2;
  const centerY = height / 2;
  const radius = Math.min(width, height) * 0.34;

  const nodes = FEATURE_KEYS.map((k, i) => {
    const angle = (i / FEATURE_KEYS.length) * Math.PI * 2 - Math.PI / 2;
    return {
      key: k,
      x: centerX + radius * Math.cos(angle),
      y: centerY + radius * Math.sin(angle),
      label: shortLabel(FEATURE_META[k].label)
    };
  });

  const links = [];
  for (let i = 0; i < FEATURE_KEYS.length; i++) {
    for (let j = i + 1; j < FEATURE_KEYS.length; j++) {
      const r = matrix[i][j];
      if (Math.abs(r) < 0.22) continue;
      links.push({ i, j, r });
    }
  }

  svg
    .append("g")
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("x1", (d) => nodes[d.i].x)
    .attr("y1", (d) => nodes[d.i].y)
    .attr("x2", (d) => nodes[d.j].x)
    .attr("y2", (d) => nodes[d.j].y)
    .attr("stroke", (d) => corrColor(d.r))
    .attr("stroke-width", (d) => 1.2 + Math.abs(d.r) * 5)
    .attr("stroke-opacity", 0.8);

  const nodeG = svg.append("g").selectAll("g").data(nodes).join("g");

  nodeG
    .append("circle")
    .attr("cx", (d) => d.x)
    .attr("cy", (d) => d.y)
    .attr("r", 22)
    .attr("fill", "#132c59")
    .attr("stroke", "#b8d8ff")
    .attr("stroke-width", 1);

  nodeG
    .append("text")
    .attr("x", (d) => d.x)
    .attr("y", (d) => d.y + 4)
    .attr("text-anchor", "middle")
    .attr("font-size", 10)
    .attr("fill", "#edfbff")
    .text((d) => d.label);
}

function renderCovariates(reportRows) {
  const html = reportRows
    .map((r) => `<div class="metric"><strong>${r.feature} × ${r.covariate}</strong><br>Pearson r = ${r.r.toFixed(3)} · β = ${r.beta.toFixed(3)}</div>`)
    .join("");
  document.getElementById("covariates").innerHTML = html;
}

function runPermutation() {
  const rows = STATE.analysis.filtered;
  const f = STATE.selectedPermFeature;
  const cov = STATE.selectedPermCovariate;
  const a = rows.map((r) => r[f]);
  const b = rows.map((r) => r[cov]);

  const observed = pearson(a, b);
  let moreExtreme = 0;

  for (let i = 0; i < STATE.permN; i++) {
    const shuffled = shuffleCopy(b);
    const rp = pearson(a, shuffled);
    if (Math.abs(rp) >= Math.abs(observed)) moreExtreme++;
  }

  const p = (moreExtreme + 1) / (STATE.permN + 1);
  const significance = p < 0.01 ? "very strong" : p < 0.05 ? "strong" : p < 0.1 ? "suggestive" : "weak";

  document.getElementById("permOutput").innerHTML = `
    Observed r = <strong>${observed.toFixed(3)}</strong><br>
    Approx. p-value = <strong>${p.toFixed(4)}</strong><br>
    Evidence strength: <strong>${significance}</strong>
  `;
}

function renderClusterTable(rows, labels, silhouettes) {
  const body = rows
    .map((row, i) => {
      const c = labels[i];
      const sil = silhouettes[i];
      const color = `hsl(${(c * 77) % 360} 85% 75%)`;
      return `<tr>
        <td>${row.name}</td>
        <td>${row.family}</td>
        <td>${row.macroarea}</td>
        <td style="color:${color};font-weight:700">${c}</td>
        <td>${sil.toFixed(2)}</td>
      </tr>`;
    })
    .join("");
  document.querySelector("#clusterTable tbody").innerHTML = body;
}

function renderDistanceMatrix(rows, distMatrix) {
  const maxCells = 72;
  const n = Math.min(rows.length, 12);
  const cells = [];

  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      cells.push({
        pair: `${rows[i].code}-${rows[j].code}`,
        d: distMatrix[i][j]
      });
    }
  }

  cells.sort((a, b) => a.d - b.d);

  document.getElementById("distanceMatrix").innerHTML = cells
    .slice(0, maxCells)
    .map((c) => `<div class="mono-cell">${c.pair}<br>${c.d.toFixed(2)}</div>`)
    .join("");
}

function renderLog(rows, corrMatrix, clusters) {
  const lines = [];
  lines.push(`> loaded_rows=${rows.length}`);
  lines.push(`> cluster_method=${STATE.clusterMethod}`);
  lines.push(`> k=${STATE.k}, eps=${STATE.eps.toFixed(1)}`);
  lines.push(`> selected_features=${STATE.xFeature}, ${STATE.yFeature}, color:${STATE.colorFeature}`);

  const strongPairs = [];
  for (let i = 0; i < FEATURE_KEYS.length; i++) {
    for (let j = i + 1; j < FEATURE_KEYS.length; j++) {
      const r = corrMatrix[i][j];
      if (Math.abs(r) >= 0.45) {
        strongPairs.push(`${FEATURE_KEYS[i]}~${FEATURE_KEYS[j]}:${r.toFixed(2)}`);
      }
    }
  }
  lines.push(`> strong_corr_pairs=${strongPairs.length ? strongPairs.join(", ") : "none"}`);

  const clusterCounts = frequencyMap(clusters.labels);
  lines.push(`> cluster_sizes=${Object.entries(clusterCounts)
    .map(([k, v]) => `${k}:${v}`)
    .join(", ")}`);

  const missingness = estimateMissingness(rows);
  lines.push(`> missingness_estimate=${missingness.toFixed(3)} (demo data is mostly complete)`);

  document.getElementById("qaLog").textContent = lines.join("\n");
}

function computeClusters(vectors) {
  if (!vectors.length) {
    return { labels: [] };
  }
  if (STATE.clusterMethod === "kmeans") {
    return { labels: kmeans(vectors, STATE.k) };
  }
  if (STATE.clusterMethod === "ward") {
    return { labels: agglomerative(vectors, STATE.k) };
  }
  return { labels: densityCluster(vectors, STATE.eps, 2) };
}

function zscoreRows(rows, keys) {
  const means = {};
  const stds = {};

  keys.forEach((k) => {
    means[k] = mean(rows.map((r) => r[k]));
    stds[k] = stdev(rows.map((r) => r[k])) || 1;
  });

  return rows.map((r) => keys.map((k) => (r[k] - means[k]) / stds[k]));
}

function correlationMatrix(rows, keys) {
  return keys.map((k1) => keys.map((k2) => pearson(rows.map((r) => r[k1]), rows.map((r) => r[k2]))));
}

function covariateReport(rows) {
  const out = [];
  FEATURE_KEYS.forEach((fk) => {
    COVARIATES.forEach((cv) => {
      const x = rows.map((r) => r[fk]);
      const y = rows.map((r) => r[cv]);
      const fit = linearFit(x, y);
      out.push({ feature: shortLabel(FEATURE_META[fk].label), covariate: cv, r: pearson(x, y), beta: fit.slope });
    });
  });
  return out.sort((a, b) => Math.abs(b.r) - Math.abs(a.r)).slice(0, 12);
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

function kmeans(data, k) {
  const kk = Math.max(2, Math.min(k, data.length));
  const dims = data[0].length;
  const centroids = seededCentroids(data, kk);
  let labels = Array(data.length).fill(0);

  for (let iter = 0; iter < 35; iter++) {
    labels = data.map((p) => nearestCentroid(p, centroids));

    for (let c = 0; c < kk; c++) {
      const members = data.filter((_, i) => labels[i] === c);
      if (!members.length) continue;
      centroids[c] = Array.from({ length: dims }, (_, d) => mean(members.map((m) => m[d])));
    }
  }
  return labels;
}

function seededCentroids(data, k) {
  const centroids = [data[0].slice()];
  while (centroids.length < k) {
    let bestPoint = data[0];
    let bestDistance = -Infinity;

    data.forEach((point) => {
      const d = Math.min(...centroids.map((c) => euclid(point, c)));
      if (d > bestDistance) {
        bestDistance = d;
        bestPoint = point;
      }
    });
    centroids.push(bestPoint.slice());
  }
  return centroids;
}

function nearestCentroid(point, centroids) {
  let best = 0;
  let bestD = Infinity;
  centroids.forEach((c, i) => {
    const d = euclid(point, c);
    if (d < bestD) {
      best = i;
      bestD = d;
    }
  });
  return best;
}

function agglomerative(data, k) {
  let clusters = data.map((_, i) => [i]);
  const kk = Math.max(2, Math.min(k, data.length));

  while (clusters.length > kk) {
    let bestI = 0;
    let bestJ = 1;
    let bestD = Infinity;

    for (let i = 0; i < clusters.length; i++) {
      for (let j = i + 1; j < clusters.length; j++) {
        const d = wardDistance(clusters[i], clusters[j], data);
        if (d < bestD) {
          bestD = d;
          bestI = i;
          bestJ = j;
        }
      }
    }

    clusters[bestI] = clusters[bestI].concat(clusters[bestJ]);
    clusters.splice(bestJ, 1);
  }

  const labels = Array(data.length).fill(0);
  clusters.forEach((c, idx) => c.forEach((rowIndex) => (labels[rowIndex] = idx)));
  return labels;
}

function wardDistance(c1, c2, data) {
  const m1 = centroidOf(c1, data);
  const m2 = centroidOf(c2, data);
  const dist = euclid(m1, m2);
  return (c1.length * c2.length) / (c1.length + c2.length) * dist * dist;
}

function centroidOf(idxList, data) {
  return data[0].map((_, d) => mean(idxList.map((i) => data[i][d])));
}

function densityCluster(data, eps, minPts) {
  const labels = Array(data.length).fill(-1);
  let currentCluster = 0;
  const visited = new Set();

  for (let i = 0; i < data.length; i++) {
    if (visited.has(i)) continue;
    visited.add(i);
    const neighbors = regionQuery(i, data, eps);

    if (neighbors.length < minPts) {
      labels[i] = -1;
      continue;
    }

    labels[i] = currentCluster;
    const seedQueue = neighbors.filter((n) => n !== i);
    while (seedQueue.length) {
      const n = seedQueue.pop();
      if (!visited.has(n)) {
        visited.add(n);
        const nbs = regionQuery(n, data, eps);
        if (nbs.length >= minPts) {
          nbs.forEach((idx) => {
            if (!seedQueue.includes(idx)) seedQueue.push(idx);
          });
        }
      }
      if (labels[n] === -1) labels[n] = currentCluster;
      if (labels[n] < 0) labels[n] = currentCluster;
    }

    currentCluster++;
  }

  // convert noise labels to their own deterministic buckets for UI readability
  return labels.map((l, i) => (l >= 0 ? l : currentCluster + (i % 2)));
}

function regionQuery(index, data, eps) {
  const result = [];
  for (let i = 0; i < data.length; i++) {
    if (euclid(data[index], data[i]) <= eps) result.push(i);
  }
  return result;
}

function approximateSilhouette(vectors, labels) {
  const out = [];
  for (let i = 0; i < vectors.length; i++) {
    const own = labels[i];
    const same = [];
    const otherByCluster = {};

    for (let j = 0; j < vectors.length; j++) {
      if (i === j) continue;
      const d = euclid(vectors[i], vectors[j]);
      if (labels[j] === own) {
        same.push(d);
      } else {
        if (!otherByCluster[labels[j]]) otherByCluster[labels[j]] = [];
        otherByCluster[labels[j]].push(d);
      }
    }

    const a = same.length ? mean(same) : 0;
    const bCandidates = Object.values(otherByCluster).map((arr) => mean(arr));
    const b = bCandidates.length ? Math.min(...bCandidates) : 0;
    const s = b === 0 && a === 0 ? 0 : (b - a) / Math.max(a, b || 1);
    out.push(s);
  }
  return out;
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
  const intercept = my - slope * mx;
  return { slope, intercept };
}

function pearson(x, y) {
  if (x.length < 2) return 0;
  const mx = mean(x);
  const my = mean(y);
  let num = 0;
  let dx = 0;
  let dy = 0;
  for (let i = 0; i < x.length; i++) {
    const ax = x[i] - mx;
    const ay = y[i] - my;
    num += ax * ay;
    dx += ax * ax;
    dy += ay * ay;
  }
  return num / Math.sqrt((dx || 1) * (dy || 1));
}

function mean(arr) {
  return arr.reduce((s, x) => s + x, 0) / (arr.length || 1);
}

function stdev(arr) {
  const m = mean(arr);
  const v = mean(arr.map((x) => (x - m) ** 2));
  return Math.sqrt(v);
}

function normalize(v, minV, maxV) {
  return (v - minV) / ((maxV - minV) || 1);
}

function gradientColor(t) {
  const hue = 235 - 210 * t;
  return `hsl(${hue} 85% 58%)`;
}

function corrColor(r) {
  if (r >= 0) {
    const alpha = 0.22 + Math.min(0.78, Math.abs(r));
    return `rgba(101, 248, 199, ${alpha})`;
  }
  const alpha = 0.22 + Math.min(0.78, Math.abs(r));
  return `rgba(255, 124, 156, ${alpha})`;
}

function shortLabel(s) {
  return s
    .replace("Morphological", "Morph.")
    .replace("inventory", "inv.")
    .replace("complexity", "cplx")
    .replace("evidentiality", "evid.")
    .split(" ")
    .slice(0, 3)
    .join(" ");
}

function euclid(a, b) {
  let s = 0;
  for (let i = 0; i < a.length; i++) s += (a[i] - b[i]) ** 2;
  return Math.sqrt(s);
}

function extent(arr) {
  return [Math.min(...arr), Math.max(...arr)];
}

function shuffleCopy(arr) {
  const out = arr.slice();
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function frequencyMap(arr) {
  return arr.reduce((acc, x) => {
    acc[x] = (acc[x] || 0) + 1;
    return acc;
  }, {});
}

function estimateMissingness(rows) {
  let n = 0;
  let miss = 0;
  rows.forEach((r) => {
    [...FEATURE_KEYS, ...COVARIATES].forEach((k) => {
      n++;
      if (r[k] === null || Number.isNaN(r[k]) || r[k] === undefined) miss++;
    });
  });
  return miss / (n || 1);
}

function text(id, value) {
  document.getElementById(id).textContent = value;
}
