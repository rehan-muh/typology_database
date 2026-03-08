const databases = [
  "WALS",
  "PHOIBLE",
  "Glottolog",
  "AUTOTYP",
  "D-PLACE",
  "ASJP",
  "IDS",
  "Lexibank",
  "SAILS",
  "APiCS"
];

const languages = [
  { name: "Quechua", code: "quy", family: "Quechuan", lat: -13.5, lon: -71.9, wordOrder: 2, tones: 0, ejectives: 0, morphology: 3, temp: 11, humidity: 60, phylo: ["Quechuan", "Southern", "Cusco"] },
  { name: "Yoruba", code: "yor", family: "Niger-Congo", lat: 7.5, lon: 3.9, wordOrder: 0, tones: 1, ejectives: 0, morphology: 1, temp: 28, humidity: 82, phylo: ["Niger-Congo", "Defoid", "Yoruboid"] },
  { name: "Georgian", code: "kat", family: "Kartvelian", lat: 42.1, lon: 43.5, wordOrder: 1, tones: 0, ejectives: 1, morphology: 3, temp: 14, humidity: 66, phylo: ["Kartvelian", "Karto-Zan", "Georgian"] },
  { name: "Japanese", code: "jpn", family: "Japonic", lat: 36.2, lon: 138.2, wordOrder: 2, tones: 0, ejectives: 0, morphology: 2, temp: 16, humidity: 71, phylo: ["Japonic", "Mainland", "Tokyo"] },
  { name: "Maori", code: "mri", family: "Austronesian", lat: -38.0, lon: 176.0, wordOrder: 0, tones: 0, ejectives: 0, morphology: 1, temp: 15, humidity: 76, phylo: ["Austronesian", "Oceanic", "Polynesian"] },
  { name: "Nahuatl", code: "nhn", family: "Uto-Aztecan", lat: 19.4, lon: -98.2, wordOrder: 0, tones: 0, ejectives: 0, morphology: 2, temp: 19, humidity: 68, phylo: ["Uto-Aztecan", "Southern", "Central Nahuan"] },
  { name: "Hindi", code: "hin", family: "Indo-European", lat: 26.8, lon: 80.9, wordOrder: 2, tones: 0, ejectives: 0, morphology: 2, temp: 27, humidity: 58, phylo: ["Indo-European", "Indo-Aryan", "Central Zone"] },
  { name: "Finnish", code: "fin", family: "Uralic", lat: 62.2, lon: 25.7, wordOrder: 0, tones: 0, ejectives: 0, morphology: 3, temp: 5, humidity: 73, phylo: ["Uralic", "Finnic", "Finnish"] },
  { name: "Navajo", code: "nav", family: "Na-Dene", lat: 35.9, lon: -109.0, wordOrder: 2, tones: 1, ejectives: 1, morphology: 3, temp: 14, humidity: 39, phylo: ["Na-Dene", "Athabaskan", "Southern"] },
  { name: "Arabic", code: "arb", family: "Afro-Asiatic", lat: 24.7, lon: 46.7, wordOrder: 1, tones: 0, ejectives: 0, morphology: 2, temp: 31, humidity: 34, phylo: ["Afro-Asiatic", "Semitic", "Arabic"] }
];

const featureKeys = ["wordOrder", "tones", "ejectives", "morphology"];
const featureLabel = {
  wordOrder: "SOV index",
  tones: "Tonality",
  ejectives: "Ejectives",
  morphology: "Morphological synthesis"
};

const state = { family: "All", k: 3, clusterMethod: "kmeans" };

init();

function init() {
  populateFilters();
  renderDatabaseChips();
  renderStats();
  renderMap();
  renderTree();
  renderAllPanels();
  bindEvents();
}

function bindEvents() {
  document.querySelector("#familyFilter").addEventListener("change", (e) => {
    state.family = e.target.value;
    renderAllPanels();
  });

  document.querySelector("#clusterMethod").addEventListener("change", (e) => {
    state.clusterMethod = e.target.value;
    renderAllPanels();
  });

  document.querySelector("#kClusters").addEventListener("input", (e) => {
    state.k = Number(e.target.value);
    document.querySelector("#kValue").textContent = state.k;
    renderClusters();
  });
}

function filteredLanguages() {
  return state.family === "All"
    ? languages
    : languages.filter((l) => l.family === state.family);
}

function populateFilters() {
  const families = ["All", ...new Set(languages.map((l) => l.family))];
  const sel = document.querySelector("#familyFilter");
  sel.innerHTML = families.map((f) => `<option>${f}</option>`).join("");
}

function renderDatabaseChips() {
  document.querySelector("#dbChips").innerHTML = databases
    .map((d) => `<span class="db-chip">${d}</span>`)
    .join("");
}

function renderStats() {
  document.querySelector("#stats").innerHTML = `
    <div class="stat"><strong>${languages.length}</strong><br/>languages fused</div>
    <div class="stat"><strong>${databases.length}</strong><br/>typological sources</div>
    <div class="stat"><strong>${featureKeys.length}</strong><br/>cross-walked features</div>
  `;
}

let map;
let layerGroup;
function renderMap() {
  map = L.map("map").setView([20, 0], 2);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors"
  }).addTo(map);
  layerGroup = L.layerGroup().addTo(map);
  refreshMapMarkers();
}

function refreshMapMarkers() {
  layerGroup.clearLayers();
  filteredLanguages().forEach((l) => {
    const color = `hsl(${Math.abs(hash(l.family)) % 360} 80% 55%)`;
    L.circleMarker([l.lat, l.lon], {
      radius: 8,
      fillColor: color,
      color: "#fff",
      weight: 1,
      fillOpacity: 0.85
    })
      .addTo(layerGroup)
      .bindPopup(`<strong>${l.name}</strong><br/>${l.family}<br/>Temp: ${l.temp}°C, Humidity: ${l.humidity}%`);
  });
}

function renderTree() {
  const roots = {};
  languages.forEach((l) => {
    const [a, b, c] = l.phylo;
    roots[a] ??= { name: a, children: {} };
    roots[a].children[b] ??= { name: b, children: {} };
    roots[a].children[b].children[c] ??= { name: c, children: [] };
    roots[a].children[b].children[c].children.push({ name: l.name });
  });
  const hierarchy = {
    name: "World",
    children: Object.values(roots).map((a) => ({
      name: a.name,
      children: Object.values(a.children).map((b) => ({
        name: b.name,
        children: Object.values(b.children)
      }))
    }))
  };

  const svg = d3.select("#tree");
  svg.selectAll("*").remove();
  const g = svg.append("g").attr("transform", "translate(70,15)");
  const root = d3.hierarchy(hierarchy);
  const layout = d3.tree().size([380, 600]);
  layout(root);

  g.selectAll("line")
    .data(root.links())
    .enter()
    .append("line")
    .attr("x1", (d) => d.source.y)
    .attr("y1", (d) => d.source.x)
    .attr("x2", (d) => d.target.y)
    .attr("y2", (d) => d.target.x)
    .attr("stroke", "#89a8ff");

  g.selectAll("circle")
    .data(root.descendants())
    .enter()
    .append("circle")
    .attr("cx", (d) => d.y)
    .attr("cy", (d) => d.x)
    .attr("r", 3.3)
    .attr("fill", (d) => (d.children ? "#7af5ff" : "#ffd28a"));

  g.selectAll("text")
    .data(root.descendants().filter((d) => !d.children || d.depth < 2))
    .enter()
    .append("text")
    .attr("x", (d) => d.y + 7)
    .attr("y", (d) => d.x + 4)
    .attr("fill", "#e5f5ff")
    .attr("font-size", 10)
    .text((d) => d.data.name);
}

function renderAllPanels() {
  refreshMapMarkers();
  renderCoOccurrence();
  renderClusters();
  renderCovariates();
}

function renderCoOccurrence() {
  const data = filteredLanguages();
  const out = [];
  for (let i = 0; i < featureKeys.length; i++) {
    for (let j = i + 1; j < featureKeys.length; j++) {
      const a = featureKeys[i];
      const b = featureKeys[j];
      const corr = pearson(data.map((x) => x[a]), data.map((x) => x[b]));
      out.push({ pair: `${featureLabel[a]} × ${featureLabel[b]}`, corr });
    }
  }

  const max = Math.max(...out.map((o) => Math.abs(o.corr)), 0.01);
  document.querySelector("#coOccurrence").innerHTML = out
    .map((o) => {
      const alpha = Math.abs(o.corr) / max;
      const color = o.corr >= 0 ? `rgba(112,255,215,${alpha})` : `rgba(255,120,140,${alpha})`;
      return `<div class="co-cell" style="background:${color}"><strong>${o.pair}</strong><br/>r = ${o.corr.toFixed(2)}</div>`;
    })
    .join("");
}

function renderClusters() {
  const data = filteredLanguages();
  const vectors = data.map((l) => featureKeys.map((k) => l[k]));
  const clusters =
    state.clusterMethod === "kmeans"
      ? kmeans(vectors, state.k)
      : agglomerative(vectors, state.k);

  document.querySelector("#clusterTable tbody").innerHTML = data
    .map(
      (l, i) =>
        `<tr><td>${l.name}</td><td>${l.family}</td><td style="color:hsl(${clusters[i] * 70},90%,70%)">${clusters[i]}</td></tr>`
    )
    .join("");
}

function renderCovariates() {
  const data = filteredLanguages();
  const entries = featureKeys.flatMap((f) => [
    { label: `${featureLabel[f]} vs Temperature`, value: pearson(data.map((d) => d[f]), data.map((d) => d.temp)) },
    { label: `${featureLabel[f]} vs Humidity`, value: pearson(data.map((d) => d[f]), data.map((d) => d.humidity)) }
  ]);

  document.querySelector("#covariates").innerHTML = entries
    .map((e) => `<div class="metric"><strong>${e.label}</strong><br/>Pearson r = ${e.value.toFixed(2)}</div>`)
    .join("");
}

function pearson(a, b) {
  if (a.length < 2) return 0;
  const avgA = a.reduce((s, x) => s + x, 0) / a.length;
  const avgB = b.reduce((s, x) => s + x, 0) / b.length;
  let num = 0,
    da = 0,
    db = 0;
  for (let i = 0; i < a.length; i++) {
    const xa = a[i] - avgA;
    const xb = b[i] - avgB;
    num += xa * xb;
    da += xa * xa;
    db += xb * xb;
  }
  return num / Math.sqrt((da || 1) * (db || 1));
}

function kmeans(data, k) {
  const dims = data[0].length;
  const centroids = data.slice(0, k).map((x) => [...x]);
  let labels = new Array(data.length).fill(0);

  for (let iter = 0; iter < 20; iter++) {
    labels = data.map((point) => {
      let best = 0;
      let bestDist = Infinity;
      centroids.forEach((c, i) => {
        const dist = euclid(point, c);
        if (dist < bestDist) {
          best = i;
          bestDist = dist;
        }
      });
      return best;
    });

    for (let i = 0; i < k; i++) {
      const members = data.filter((_, idx) => labels[idx] === i);
      if (!members.length) continue;
      centroids[i] = Array.from({ length: dims }, (_, d) => members.reduce((s, m) => s + m[d], 0) / members.length);
    }
  }
  return labels;
}

function agglomerative(data, k) {
  let clusters = data.map((_, i) => [i]);
  while (clusters.length > k) {
    let bestI = 0,
      bestJ = 1,
      best = Infinity;
    for (let i = 0; i < clusters.length; i++) {
      for (let j = i + 1; j < clusters.length; j++) {
        const d = wardDistance(clusters[i], clusters[j], data);
        if (d < best) {
          best = d;
          bestI = i;
          bestJ = j;
        }
      }
    }
    clusters[bestI] = [...clusters[bestI], ...clusters[bestJ]];
    clusters.splice(bestJ, 1);
  }

  const labels = new Array(data.length).fill(0);
  clusters.forEach((cluster, idx) => cluster.forEach((i) => (labels[i] = idx)));
  return labels;
}

function wardDistance(c1, c2, data) {
  const mean = (cluster) => {
    const dims = data[0].length;
    return Array.from({ length: dims }, (_, d) => cluster.reduce((s, i) => s + data[i][d], 0) / cluster.length);
  };
  return euclid(mean(c1), mean(c2));
}

function euclid(a, b) {
  return Math.sqrt(a.reduce((s, x, i) => s + (x - b[i]) ** 2, 0));
}

function hash(s) {
  return s.split("").reduce((acc, c) => acc * 33 + c.charCodeAt(0), 7);
}
