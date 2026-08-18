/* Precision-cliff research atlas — vanilla JS + d3 v7 */
(function () {
  'use strict';

  // ---------------------------------------------------------------- constants

  var KIND_STYLE = {
    arm:       { color: '#6ea8fe', symbol: d3.symbolCircle,  size: 300, label: 'Arm' },
    wave:      { color: '#f0a35e', symbol: d3.symbolSquare,  size: 300, label: 'Wave' },
    control:   { color: '#9b8cff', symbol: d3.symbolTriangle,size: 340, label: 'Control' },
    analysis:  { color: '#4ec9a6', symbol: d3.symbolDiamond, size: 340, label: 'Analysis' },
    extension: { color: '#e06ac2', symbol: d3.symbolStar,    size: 380, label: 'Extension' },
    claim:     { color: '#ffd166', symbol: d3.symbolCircle,  size: 1000, label: 'Claim' },
    paper:     { color: '#ffd166', symbol: d3.symbolCircle,  size: 1000, label: 'Paper / claim' },
    other:     { color: '#7d8796', symbol: d3.symbolCircle,  size: 260, label: 'Other' }
  };

  var LINK_STYLE = {
    informs:          { color: '#6ea8fe', dash: null,    label: 'informs' },
    feeds:            { color: '#4ec9a6', dash: null,    label: 'feeds' },
    replicates:       { color: '#58c37a', dash: null,    label: 'replicates' },
    extends:          { color: '#f0a35e', dash: null,    label: 'extends' },
    controls_for:     { color: '#9b8cff', dash: '5,4',   label: 'controls for' },
    disconfirms:      { color: '#ff6b6b', dash: '7,4',   label: 'disconfirms' },
    scopes:           { color: '#d6b64f', dash: '2,4',   label: 'scopes' },
    contrasts_with:   { color: '#e06ac2', dash: '9,5',   label: 'contrasts with' },
    // graph.json relations
    references:            { color: '#5f7fb0', dash: null,  label: 'references' },
    cites:                 { color: '#8f7fd8', dash: null,  label: 'cites' },
    rationale_for:         { color: '#4ec9a6', dash: null,  label: 'rationale for' },
    conceptually_related_to:{ color: '#6b7480', dash: '4,4', label: 'conceptually related' },
    semantically_similar_to:{ color: '#a08b5f', dash: '2,4', label: 'semantically similar' },
    other:            { color: '#6b7480', dash: '3,3',   label: 'other' }
  };

  var VERDICT_COLOR = {
    held: '#4ec98a', disconfirmed: '#ff6b6b', partial: '#f0b45e', descriptive: '#8d97a8'
  };

  // flowchart geometry
  var FLOW = { w: 184, h: 52, xgap: 62, ygap: 14, pad: 36 };

  var COMMUNITY_LABELS = [
    'Provenance and alias audit',
    'Parent-echo cliff evidence',
    'Three-tier ladder arms',
    'Anchoring in discovery loops',
    'Closed-form rule and arm M',
    'Trace elicitation and faithfulness',
    'Quantization ladder infrastructure',
    'Quantization literature',
    'Task-generality waves',
    'Family-generality arms',
    'Choice-versus-execution probes',
    'Templates and seeded parents'
  ];

  var COMMUNITY_COLORS = [
    '#6ea8fe', '#ff6b6b', '#4ec9a6', '#f0a35e',
    '#c792ea', '#5fd0d8', '#e06ac2', '#a6c85c',
    '#ffd166', '#7f9cf5', '#f2836b', '#66c2a5'
  ];

  // ---------------------------------------------------------------- dom refs

  var el = {
    tabs:        document.getElementById('tabs'),
    search:      document.getElementById('search'),
    searchCount: document.getElementById('search-count'),
    stage:       document.getElementById('stage'),
    stageTitle:  document.getElementById('stage-title'),
    stageSub:    document.getElementById('stage-sub'),
    wrap:        document.getElementById('canvas-wrap'),
    svg:         d3.select('#graph'),
    empty:       document.getElementById('empty'),
    legend:      document.getElementById('legend'),
    viewmode:    document.getElementById('viewmode'),
    linktip:     document.getElementById('linktip'),
    about:       document.getElementById('about'),
    panelEmpty:  document.getElementById('panel-empty'),
    panelBody:   document.getElementById('panel-body'),
    toast:       document.getElementById('toast'),
    reset:       document.getElementById('btn-reset'),
    expand:      document.getElementById('btn-expand'),
    subWrap:     document.getElementById('stage-sub-wrap'),
    subToggle:   document.getElementById('btn-sub-toggle')
  };

  // ---------------------------------------------------------------- state

  var state = {
    view: 'paper1',
    arms: null,          // arms.json payload (or null)
    armsError: null,
    graph: null,         // graph.json payload (or null)
    graphError: null,
    views: {},           // viewId -> {nodes, links, byId, sim, layers, zoom}
    selected: {},        // viewId -> node id
    modes: { paper1: 'network', paper2: 'network' },  // viewId -> 'network' | 'flow'
    subOpen: {},         // viewId -> summary expanded? (in-memory only)
    expanded: false,     // fullscreen-ish stage
    query: ''
  };

  // ---------------------------------------------------------------- helpers

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function kindStyle(kind) {
    return KIND_STYLE[String(kind || '').toLowerCase()] || KIND_STYLE.other;
  }

  function linkStyle(type) {
    return LINK_STYLE[String(type || '').toLowerCase()] || LINK_STYLE.other;
  }

  function verdictClass(v) {
    var s = String(v || '').toLowerCase();
    if (/disconfirm|refut|fail|reject|not\s+support/.test(s)) return 'disconfirmed';
    if (/partial|mixed|qualified|weak/.test(s)) return 'partial';
    if (/held|confirm|support|replicat|survive|robust/.test(s)) return 'held';
    return 'descriptive';
  }

  function verdictWord(v) {
    var c = verdictClass(v);
    return c === 'held' ? 'held'
      : c === 'disconfirmed' ? 'disconfirmed'
      : c === 'partial' ? 'partial' : 'descriptive';
  }

  function truncate(s, n) {
    s = String(s == null ? '' : s);
    return s.length > n ? s.slice(0, n - 1) + '…' : s;
  }

  // greedy word wrap into at most maxLines lines of ~maxChars, ellipsing leftovers
  function wrapLabel(s, maxChars, maxLines) {
    var words = String(s == null ? '' : s).split(/\s+/).filter(Boolean);
    var lines = [], cur = '', dropped = false;
    words.forEach(function (w) {
      if (lines.length >= maxLines) { dropped = true; return; }
      var test = cur ? cur + ' ' + w : w;
      if (test.length <= maxChars) { cur = test; return; }
      if (cur) { lines.push(cur); cur = w; }
      else { lines.push(truncate(w, maxChars)); cur = ''; }
    });
    if (cur) {
      if (lines.length < maxLines) lines.push(cur);
      else dropped = true;
    }
    if (dropped && lines.length) {
      var last = lines.length - 1;
      lines[last] = lines[last].slice(0, Math.max(1, maxChars - 2)) + '…';
    }
    return lines.length ? lines : [''];
  }

  var toastTimer = null;
  function toast(msg) {
    el.toast.textContent = msg;
    el.toast.classList.remove('hidden');
    // force reflow so the transition runs on repeat calls
    void el.toast.offsetWidth;
    el.toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      el.toast.classList.remove('show');
      setTimeout(function () { el.toast.classList.add('hidden'); }, 220);
    }, 1500);
  }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(
        function () { toast('copied'); },
        function () { fallbackCopy(text); }
      );
    } else {
      fallbackCopy(text);
    }
  }

  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    toast(ok ? 'copied' : 'copy failed — select manually');
  }

  // ---------------------------------------------------------------- data load

  function loadJSON(path) {
    return fetch(path, { cache: 'no-store' }).then(function (r) {
      if (!r.ok) throw new Error(path + ' → HTTP ' + r.status);
      return r.json();
    });
  }

  function loadAll() {
    var a = loadJSON('arms.json').then(
      function (d) { state.arms = d; state.armsError = null; },
      function (e) { state.arms = null; state.armsError = e.message || String(e); }
    );
    var g = loadJSON('graph.json').then(
      function (d) { state.graph = d; state.graphError = null; },
      function (e) { state.graph = null; state.graphError = e.message || String(e); }
    );
    var m = loadJSON('meta.json').then(
      function (d) { state.meta = d; },
      function () { state.meta = null; }
    );
    return Promise.all([a, g, m]);
  }

  function updWhen(key) {
    return (state.meta && state.meta[key]) || null;
  }

  function stampTitle(dateStr) {
    if (!dateStr) return;
    var s = document.createElement('span');
    s.className = 'updated-tag';
    s.textContent = 'updated ' + dateStr;
    el.stageTitle.appendChild(s);
  }

  // ---------------------------------------------------------------- model build

  function paperMeta(paperId) {
    var papers = (state.arms && state.arms.papers) || [];
    for (var i = 0; i < papers.length; i++) {
      if (papers[i].id === paperId) return papers[i];
    }
    return null;
  }

  function buildAtlasModel(paperId) {
    if (!state.arms || !Array.isArray(state.arms.arms)) return null;

    var nodes = state.arms.arms
      .filter(function (a) { return a && a.paper === paperId; })
      .map(function (a) {
        return {
          id: a.id,
          label: a.label || a.id,
          kind: String(a.kind || 'other').toLowerCase(),
          design: a.design, result: a.result, verdict: a.verdict,
          caveats: a.caveats, stats: a.stats, raw: a
        };
      });

    var byId = {};
    nodes.forEach(function (n) { byId[n.id] = n; });

    var links = ((state.arms.links) || [])
      .filter(function (l) {
        var s = typeof l.source === 'object' ? l.source.id : l.source;
        var t = typeof l.target === 'object' ? l.target.id : l.target;
        return byId[s] && byId[t];
      })
      .map(function (l, i) {
        return {
          id: 'l' + i,
          source: typeof l.source === 'object' ? l.source.id : l.source,
          target: typeof l.target === 'object' ? l.target.id : l.target,
          type: String(l.type || 'other').toLowerCase(),
          note: l.note || '',
          opacity: 0.75
        };
      });

    return { nodes: nodes, links: links, byId: byId, mode: 'atlas', paperId: paperId };
  }

  function buildConceptModel() {
    if (!state.graph || !Array.isArray(state.graph.nodes)) return null;

    var nodes = state.graph.nodes.map(function (n) {
      return {
        id: n.id,
        label: n.label || n.id,
        kind: n.file_type === 'paper' ? 'paper' : 'other',
        community: (typeof n.community === 'number') ? n.community : -1,
        sourceFile: n.source_file,
        sourceLocation: n.source_location,
        sourceUrl: n.source_url,
        author: n.author,
        raw: n
      };
    });

    var byId = {};
    nodes.forEach(function (n) { byId[n.id] = n; });

    var links = (state.graph.links || [])
      .filter(function (l) {
        var s = typeof l.source === 'object' ? l.source.id : l.source;
        var t = typeof l.target === 'object' ? l.target.id : l.target;
        return byId[s] && byId[t];
      })
      .map(function (l, i) {
        var cs = (typeof l.confidence_score === 'number') ? l.confidence_score : 0.6;
        return {
          id: 'g' + i,
          source: typeof l.source === 'object' ? l.source.id : l.source,
          target: typeof l.target === 'object' ? l.target.id : l.target,
          type: String(l.relation || 'other').toLowerCase(),
          note: (l.confidence ? l.confidence + ' · ' : '') +
                'confidence ' + cs.toFixed(2) +
                (l.source_location ? ' · ' + l.source_location : '') +
                (l.source_file ? ' · ' + l.source_file : ''),
          opacity: Math.max(0.12, Math.min(0.9, cs * 0.85))
        };
      });

    return { nodes: nodes, links: links, byId: byId, mode: 'concept' };
  }

  // ---------------------------------------------------------------- rendering

  function nodeColor(model, n) {
    if (model.mode === 'concept') {
      if (n.community >= 0 && n.community < COMMUNITY_COLORS.length) {
        return COMMUNITY_COLORS[n.community];
      }
      return '#7d8796';
    }
    return kindStyle(n.kind).color;
  }

  function nodeSize(model, n) {
    if (model.mode === 'concept') return n.kind === 'paper' ? 420 : 200;
    return kindStyle(n.kind).size;
  }

  function nodeSymbol(model, n) {
    if (model.mode === 'concept') return d3.symbolCircle;
    return kindStyle(n.kind).symbol;
  }

  function nodeRadius(model, n) {
    return Math.sqrt(nodeSize(model, n) / Math.PI) + 3;
  }

  function ensureDefs(svg, model) {
    var defs = svg.select('defs');
    if (defs.empty()) defs = svg.append('defs');
    var types = {};
    model.links.forEach(function (l) { types[l.type] = true; });
    var ids = Object.keys(types);

    var markers = defs.selectAll('marker').data(ids, function (d) { return d; });
    markers.exit().remove();
    markers.enter().append('marker')
      .attr('id', function (d) { return 'arrow-' + d.replace(/[^a-z0-9_]/gi, '_'); })
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 10).attr('refY', 0)
      .attr('markerWidth', 6).attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,-4L9,0L0,4')
      .attr('fill', function (d) { return linkStyle(d).color; });
  }

  function renderGraph(viewId, model) {
    var svg = el.svg;
    svg.selectAll('*').remove();

    var box = el.wrap.getBoundingClientRect();
    var W = Math.max(320, box.width), H = Math.max(280, box.height);
    svg.attr('viewBox', '0 0 ' + W + ' ' + H);

    ensureDefs(svg, model);

    var root = svg.append('g').attr('class', 'root');
    var linkLayer = root.append('g').attr('class', 'links');
    var hitLayer  = root.append('g').attr('class', 'link-hits');
    var nodeLayer = root.append('g').attr('class', 'nodes');

    var linkSel = linkLayer.selectAll('path')
      .data(model.links, function (d) { return d.id; })
      .join('path')
      .attr('class', 'link')
      .attr('stroke', function (d) { return linkStyle(d.type).color; })
      .attr('stroke-width', 1.4)
      .attr('stroke-opacity', function (d) { return d.opacity; })
      .attr('stroke-dasharray', function (d) { return linkStyle(d.type).dash; })
      .attr('marker-end', function (d) {
        return 'url(#arrow-' + d.type.replace(/[^a-z0-9_]/gi, '_') + ')';
      });

    var hitSel = hitLayer.selectAll('path')
      .data(model.links, function (d) { return d.id; })
      .join('path')
      .attr('class', 'link-hit')
      .on('mousemove', function (event, d) { showLinkTip(event, d, model); })
      .on('mouseleave', hideLinkTip);

    var nodeSel = nodeLayer.selectAll('g')
      .data(model.nodes, function (d) { return d.id; })
      .join('g')
      .attr('class', function (d) {
        return 'node' + ((d.kind === 'claim' || d.kind === 'paper') ? ' is-claim' : '');
      })
      .on('click', function (event, d) {
        event.stopPropagation();
        selectNode(viewId, d.id);
      });

    nodeSel.append('path')
      .attr('class', 'shape')
      .attr('d', function (d) {
        return d3.symbol().type(nodeSymbol(model, d)).size(nodeSize(model, d))();
      })
      .attr('fill', function (d) { return nodeColor(model, d); });

    nodeSel.append('title').text(function (d) { return d.label; });

    nodeSel.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', function (d) { return nodeRadius(model, d) + 12; })
      .text(function (d) { return truncate(d.label, model.mode === 'concept' ? 30 : 34); });

    var linkDistance = model.mode === 'concept' ? 90 : 130;
    var charge = model.mode === 'concept' ? -260 : -520;

    var sim = d3.forceSimulation(model.nodes)
      .force('link', d3.forceLink(model.links).id(function (d) { return d.id; })
        .distance(linkDistance).strength(0.5))
      .force('charge', d3.forceManyBody().strength(charge))
      .force('center', d3.forceCenter(W / 2, H / 2))
      .force('collide', d3.forceCollide().radius(function (d) {
        return nodeRadius(model, d) + (model.mode === 'concept' ? 14 : 28);
      }))
      .force('x', d3.forceX(W / 2).strength(0.03))
      .force('y', d3.forceY(H / 2).strength(0.05));

    sim.on('tick', function () {
      linkSel.attr('d', linkPath(model));
      hitSel.attr('d', linkPath(model));
      nodeSel.attr('transform', function (d) {
        return 'translate(' + d.x + ',' + d.y + ')';
      });
    });

    nodeSel.call(d3.drag()
      .on('start', function (event, d) {
        if (!event.active) sim.alphaTarget(0.3).restart();
        d.fx = d.x; d.fy = d.y;
      })
      .on('drag', function (event, d) { d.fx = event.x; d.fy = event.y; })
      .on('end', function (event, d) {
        if (!event.active) sim.alphaTarget(0);
        d.fx = null; d.fy = null;
      }));

    var zoom = d3.zoom().scaleExtent([0.15, 6]).on('zoom', function (event) {
      root.attr('transform', event.transform);
    });
    svg.call(zoom);
    svg.on('click', function () { clearSelection(viewId); });

    var view = {
      model: model, svg: svg, root: root, sim: sim, zoom: zoom,
      nodeSel: nodeSel, linkSel: linkSel, hitSel: hitSel, W: W, H: H,
      layout: 'network', resetTransform: d3.zoomIdentity
    };
    state.views[viewId] = view;
    return view;
  }

  function linkPath(model) {
    return function (d) {
      var sx = d.source.x, sy = d.source.y, tx = d.target.x, ty = d.target.y;
      if (sx == null || tx == null) return 'M0,0L0,0';
      var dx = tx - sx, dy = ty - sy;
      var dist = Math.sqrt(dx * dx + dy * dy) || 1;
      var rT = nodeRadius(model, d.target) + 6;
      var rS = nodeRadius(model, d.source) + 2;
      var x1 = sx + (dx / dist) * rS, y1 = sy + (dy / dist) * rS;
      var x2 = tx - (dx / dist) * rT, y2 = ty - (dy / dist) * rT;
      return 'M' + x1 + ',' + y1 + 'L' + x2 + ',' + y2;
    };
  }

  // links carry either raw string ids (flow view) or node objects (after forceLink)
  function endpointNode(model, ref) {
    if (ref && typeof ref === 'object') return ref;
    return model.byId[ref] || null;
  }

  function showLinkTip(event, d, model) {
    var wrapBox = el.wrap.getBoundingClientRect();
    var st = linkStyle(d.type);
    var sN = model ? endpointNode(model, d.source) : d.source;
    var tN = model ? endpointNode(model, d.target) : d.target;
    var sLabel = (sN && sN.label) || d.source;
    var tLabel = (tN && tN.label) || d.target;
    el.linktip.innerHTML =
      '<b>' + esc(st.label) + '</b><br>' +
      esc(truncate(sLabel, 46)) + ' → ' + esc(truncate(tLabel, 46)) +
      (d.note ? '<br><span style="color:#9aa4b4">' + esc(d.note) + '</span>' : '');
    el.linktip.classList.remove('hidden');
    var x = event.clientX - wrapBox.left + 14;
    var y = event.clientY - wrapBox.top + 14;
    var tw = el.linktip.offsetWidth, th = el.linktip.offsetHeight;
    if (x + tw > wrapBox.width - 8) x = wrapBox.width - tw - 8;
    if (y + th > wrapBox.height - 8) y = y - th - 28;
    el.linktip.style.left = Math.max(8, x) + 'px';
    el.linktip.style.top = Math.max(8, y) + 'px';
  }

  function hideLinkTip() { el.linktip.classList.add('hidden'); }

  // ---------------------------------------------------------------- flowchart

  // Adjacency for the current model, with cycles broken.
  // Back edges are found by an iterative DFS (a child still grey is on the
  // recursion stack, so that edge closes a cycle) and dropped from the DAG.
  function flowTopology(model) {
    var ids = model.nodes.map(function (n) { return n.id; });
    var adj = {}, preds = {}, succs = {};
    ids.forEach(function (id) { adj[id] = []; preds[id] = []; succs[id] = []; });

    var edges = model.links.map(function (l) {
      return {
        s: (l.source && l.source.id) || l.source,
        t: (l.target && l.target.id) || l.target,
        type: l.type, note: l.note
      };
    }).filter(function (e) { return adj[e.s] && adj[e.t] && e.s !== e.t; });

    edges.forEach(function (e) { adj[e.s].push(e.t); });

    var color = {}, back = {};
    ids.forEach(function (id) { color[id] = 0; });
    ids.forEach(function (root) {
      if (color[root] !== 0) return;
      color[root] = 1;
      var stack = [{ id: root, i: 0 }];
      while (stack.length) {
        var top = stack[stack.length - 1];
        var kids = adj[top.id];
        if (top.i < kids.length) {
          var c = kids[top.i++];
          if (color[c] === 1) back[top.id + '>' + c] = true;
          else if (color[c] === 0) { color[c] = 1; stack.push({ id: c, i: 0 }); }
        } else {
          color[top.id] = 2;
          stack.pop();
        }
      }
    });

    edges.forEach(function (e) {
      if (back[e.s + '>' + e.t]) return;
      preds[e.t].push(e.s);
      succs[e.s].push(e.t);
    });

    // longest-path layering over the acyclic remainder
    var indeg = {}, layer = {};
    ids.forEach(function (id) { indeg[id] = preds[id].length; layer[id] = 0; });
    var queue = ids.filter(function (id) { return indeg[id] === 0; });
    while (queue.length) {
      var id = queue.shift();
      succs[id].forEach(function (t) {
        if (layer[t] < layer[id] + 1) layer[t] = layer[id] + 1;
        if (--indeg[t] === 0) queue.push(t);
      });
    }

    return { layer: layer, preds: preds, succs: succs, broken: Object.keys(back).length };
  }

  function fitTransform(contentW, contentH, W, H) {
    var k = Math.min(W / contentW, H / contentH) * 0.94;
    k = Math.max(0.08, Math.min(1.15, k));
    return d3.zoomIdentity
      .translate((W - contentW * k) / 2, (H - contentH * k) / 2)
      .scale(k);
  }

  // Assigns node.x / node.y (centres, in content space) for the layered layout.
  function layoutFlow(model) {
    var topo = flowTopology(model);
    var maxL = 0;
    model.nodes.forEach(function (n) { maxL = Math.max(maxL, topo.layer[n.id]); });

    var cols = [];
    for (var i = 0; i <= maxL; i++) cols.push([]);
    model.nodes.forEach(function (n) { cols[topo.layer[n.id]].push(n.id); });

    var pos = {};
    cols.forEach(function (c) { c.forEach(function (id, i) { pos[id] = i; }); });

    function bary(id, map) {
      var ns = map[id], s = 0, k = 0;
      for (var j = 0; j < ns.length; j++) {
        if (pos[ns[j]] != null) { s += pos[ns[j]]; k++; }
      }
      return k ? s / k : pos[id];
    }

    // barycentre sweeps, alternating direction, to thin out crossings
    for (var pass = 0; pass < 6; pass++) {
      var down = pass % 2 === 0;
      for (var step = 0; step <= maxL; step++) {
        var ci = down ? step : maxL - step;
        var map = down ? topo.preds : topo.succs;
        var keyed = cols[ci].map(function (id, i) {
          return { id: id, k: bary(id, map), i: i };
        });
        keyed.sort(function (a, b) { return (a.k - b.k) || (a.i - b.i); });
        cols[ci] = keyed.map(function (o) { return o.id; });
        cols[ci].forEach(function (id, i) { pos[id] = i; });
      }
    }

    var maxRows = 1;
    cols.forEach(function (c) { maxRows = Math.max(maxRows, c.length); });

    var stepX = FLOW.w + FLOW.xgap;
    var stepY = FLOW.h + FLOW.ygap;
    var bandH = maxRows * stepY;

    cols.forEach(function (col, ci) {
      var n = col.length;
      col.forEach(function (id, i) {
        var node = model.byId[id];
        node.x = FLOW.pad + FLOW.w / 2 + ci * stepX;
        node.y = FLOW.pad + bandH / 2 + (i - (n - 1) / 2) * stepY;
        node.layer = ci;
      });
    });

    return {
      cols: cols,
      layers: maxL + 1,
      broken: topo.broken,
      contentW: FLOW.pad * 2 + maxL * stepX + FLOW.w,
      contentH: FLOW.pad * 2 + bandH
    };
  }

  function flowLinkPath(model) {
    var hw = FLOW.w / 2;
    return function (d) {
      var s = endpointNode(model, d.source), t = endpointNode(model, d.target);
      if (!s || !t || s.x == null || t.x == null) return 'M0,0L0,0';
      if (t.x > s.x) {
        var x1 = s.x + hw, x2 = t.x - hw - 5;
        var dx = Math.max(38, (x2 - x1) * 0.55);
        return 'M' + x1 + ',' + s.y +
               'C' + (x1 + dx) + ',' + s.y + ' ' + (x2 - dx) + ',' + t.y + ' ' + x2 + ',' + t.y;
      }
      // same-layer or cycle-closing edge: bow out to the left
      var bx1 = s.x - hw, bx2 = t.x - hw - 5;
      var bow = 70 + Math.abs(t.y - s.y) * 0.25;
      var my = Math.min(s.y, t.y) - 46;
      return 'M' + bx1 + ',' + s.y +
             'C' + (bx1 - bow) + ',' + my + ' ' + (bx2 - bow) + ',' + my + ' ' + bx2 + ',' + t.y;
    };
  }

  function renderFlow(viewId, model) {
    var svg = el.svg;
    svg.selectAll('*').remove();

    var box = el.wrap.getBoundingClientRect();
    var W = Math.max(320, box.width), H = Math.max(280, box.height);
    svg.attr('viewBox', '0 0 ' + W + ' ' + H);

    ensureDefs(svg, model);

    var lay = layoutFlow(model);
    var root = svg.append('g').attr('class', 'root');
    var linkLayer = root.append('g').attr('class', 'links');
    var hitLayer  = root.append('g').attr('class', 'link-hits');
    var nodeLayer = root.append('g').attr('class', 'nodes');

    var pathFn = flowLinkPath(model);

    var linkSel = linkLayer.selectAll('path')
      .data(model.links, function (d) { return d.id; })
      .join('path')
      .attr('class', 'link')
      .attr('d', pathFn)
      .attr('stroke', function (d) { return linkStyle(d.type).color; })
      .attr('stroke-width', 1.4)
      .attr('stroke-opacity', function (d) { return d.opacity; })
      .attr('stroke-dasharray', function (d) { return linkStyle(d.type).dash; })
      .attr('marker-end', function (d) {
        return 'url(#arrow-' + d.type.replace(/[^a-z0-9_]/gi, '_') + ')';
      });

    var hitSel = hitLayer.selectAll('path')
      .data(model.links, function (d) { return d.id; })
      .join('path')
      .attr('class', 'link-hit')
      .attr('d', pathFn)
      .on('mousemove', function (event, d) { showLinkTip(event, d, model); })
      .on('mouseleave', hideLinkTip);

    var nodeSel = nodeLayer.selectAll('g')
      .data(model.nodes, function (d) { return d.id; })
      .join('g')
      .attr('class', function (d) {
        return 'node flow' + ((d.kind === 'claim' || d.kind === 'paper') ? ' is-claim' : '');
      })
      .attr('transform', function (d) { return 'translate(' + d.x + ',' + d.y + ')'; })
      .on('click', function (event, d) {
        event.stopPropagation();
        selectNode(viewId, d.id);
      });

    nodeSel.append('rect').attr('class', 'shape')
      .attr('x', -FLOW.w / 2).attr('y', -FLOW.h / 2)
      .attr('width', FLOW.w).attr('height', FLOW.h).attr('rx', 9);

    nodeSel.append('rect').attr('class', 'stripe')
      .attr('x', -FLOW.w / 2 + 1.5).attr('y', -FLOW.h / 2 + 1.5)
      .attr('width', 4).attr('height', FLOW.h - 3).attr('rx', 2)
      .attr('fill', function (d) { return kindStyle(d.kind).color; });

    nodeSel.append('circle').attr('class', 'vdot')
      .attr('cx', FLOW.w / 2 - 13).attr('cy', -FLOW.h / 2 + 13).attr('r', 4.5)
      .attr('fill', function (d) {
        return VERDICT_COLOR[verdictClass(d.verdict)] || VERDICT_COLOR.descriptive;
      });

    nodeSel.append('text').attr('class', 'nkind')
      .attr('x', -FLOW.w / 2 + 13).attr('y', -FLOW.h / 2 + 16)
      .text(function (d) { return kindStyle(d.kind).label; });

    nodeSel.append('title').text(function (d) {
      return d.label + (d.verdict ? ' — ' + d.verdict : '');
    });

    nodeSel.each(function (d) {
      var g = d3.select(this);
      wrapLabel(d.label, 27, 2).forEach(function (line, i) {
        g.append('text').attr('class', 'nlabel')
          .attr('x', -FLOW.w / 2 + 13).attr('y', 5 + i * 13)
          .text(line);
      });
    });

    var zoom = d3.zoom().scaleExtent([0.06, 6]).on('zoom', function (event) {
      root.attr('transform', event.transform);
    });
    svg.call(zoom);
    var t0 = fitTransform(lay.contentW, lay.contentH, W, H);
    svg.call(zoom.transform, t0);
    svg.on('click', function () { clearSelection(viewId); });

    var view = {
      model: model, svg: svg, root: root, sim: null, zoom: zoom,
      nodeSel: nodeSel, linkSel: linkSel, hitSel: hitSel, W: W, H: H,
      layout: 'flow', resetTransform: t0,
      contentW: lay.contentW, contentH: lay.contentH,
      layers: lay.layers, broken: lay.broken
    };
    state.views[viewId] = view;
    return view;
  }

  // ---------------------------------------------------------------- legend

  function renderLegend(model) {
    if (model.mode === 'concept') {
      var communities = {};
      model.nodes.forEach(function (n) { communities[n.community] = true; });
      var comms = Object.keys(communities).map(Number).sort(function (a, b) { return a - b; });

      var html = '<h4>Communities</h4><ul>';
      comms.forEach(function (c) {
        var color = (c >= 0 && c < COMMUNITY_COLORS.length) ? COMMUNITY_COLORS[c] : '#7d8796';
        var label = (c >= 0 && c < COMMUNITY_LABELS.length) ? COMMUNITY_LABELS[c] : 'Unassigned';
        html += '<li><span class="swatch" style="background:' + color + '"></span>' +
                '<span>' + c + ' · ' + esc(label) + '</span></li>';
      });
      html += '</ul><h4>Edges</h4><ul>';
      var seen = {};
      model.links.forEach(function (l) { seen[l.type] = true; });
      Object.keys(seen).forEach(function (t) {
        var st = linkStyle(t);
        html += '<li><span class="dash" style="border-top-color:' + st.color +
                ';border-top-style:' + (st.dash ? 'dashed' : 'solid') + '"></span>' +
                '<span>' + esc(st.label) + '</span></li>';
      });
      html += '</ul><p class="muted" style="margin:6px 0 0;font-size:11.5px">Edge opacity tracks extraction confidence.</p>';
      el.legend.innerHTML = html;
      el.legend.classList.remove('hidden');
      return;
    }

    var kinds = {};
    model.nodes.forEach(function (n) { kinds[n.kind] = true; });
    var h = '<h4>Node kinds</h4><ul>';
    Object.keys(kinds).forEach(function (k) {
      var st = kindStyle(k);
      var path = d3.symbol().type(st.symbol).size(Math.min(st.size, 220))();
      h += '<li><svg width="16" height="16" viewBox="-8 -8 16 16">' +
           '<path d="' + path + '" fill="' + st.color + '"></path></svg>' +
           '<span>' + esc(st.label) + '</span></li>';
    });
    h += '</ul><h4>Edge types</h4><ul>';
    var types = {};
    model.links.forEach(function (l) { types[l.type] = true; });
    Object.keys(types).forEach(function (t) {
      var st = linkStyle(t);
      h += '<li><span class="dash" style="border-top-color:' + st.color +
           ';border-top-style:' + (st.dash ? 'dashed' : 'solid') + '"></span>' +
           '<span>' + esc(st.label) + '</span></li>';
    });
    h += '</ul>';
    el.legend.innerHTML = h;
    el.legend.classList.remove('hidden');
  }

  // ---------------------------------------------------------------- selection + panel

  function neighborsOf(model, id) {
    var out = [];
    model.links.forEach(function (l) {
      var s = l.source.id || l.source, t = l.target.id || l.target;
      if (s === id) out.push({ other: model.byId[t], type: l.type, note: l.note, dir: 'out' });
      else if (t === id) out.push({ other: model.byId[s], type: l.type, note: l.note, dir: 'in' });
    });
    return out.filter(function (n) { return n.other; });
  }

  function clearSelection(viewId) {
    state.selected[viewId] = null;
    var view = state.views[viewId];
    if (view) view.nodeSel.classed('selected', false);
    el.panelBody.classList.add('hidden');
    el.panelEmpty.classList.remove('hidden');
    if (document.body.classList.contains('is-expanded') &&
        document.body.classList.contains('has-selection')) {
      document.body.classList.remove('has-selection');
      requestAnimationFrame(refit);
    } else {
      document.body.classList.remove('has-selection');
    }
  }

  function selectNode(viewId, id) {
    var view = state.views[viewId];
    if (!view) return;
    var model = view.model;
    var node = model.byId[id];
    if (!node) return;

    state.selected[viewId] = id;
    view.nodeSel.classed('selected', function (d) { return d.id === id; });
    var panelWasHidden = document.body.classList.contains('is-expanded') &&
      !document.body.classList.contains('has-selection');
    document.body.classList.add('has-selection');
    if (panelWasHidden) requestAnimationFrame(refit);
    renderPanel(viewId, node);
  }

  function statsTable(stats) {
    if (!stats || typeof stats !== 'object') return '';
    var keys = Object.keys(stats);
    if (!keys.length) return '';
    var rows = keys.map(function (k) {
      var v = stats[k];
      if (v && typeof v === 'object') v = JSON.stringify(v);
      return '<tr><td class="k">' + esc(k.replace(/_/g, ' ')) + '</td>' +
             '<td class="v">' + esc(v) + '</td></tr>';
    }).join('');
    return '<div class="field"><div class="k">Key figures</div>' +
           '<table class="stats">' + rows + '</table></div>';
  }

  // ---------------------------------------------------------------- lineage strip

  // Breadth-first walk up (predecessors) and down (successors) from a node.
  // `seen` is shared per direction so converging paths do not repeat a node.
  function lineageChains(model, id, maxDepth) {
    var preds = {}, succs = {};
    model.nodes.forEach(function (n) { preds[n.id] = []; succs[n.id] = []; });
    model.links.forEach(function (l) {
      var s = (l.source && l.source.id) || l.source;
      var t = (l.target && l.target.id) || l.target;
      if (!preds[t] || !succs[s]) return;
      preds[t].push({ id: s, type: l.type });
      succs[s].push({ id: t, type: l.type });
    });

    function walk(map) {
      var levels = [], seen = {}, frontier = [id];
      seen[id] = true;
      for (var d = 0; d < maxDepth && frontier.length; d++) {
        var row = [], next = [];
        frontier.forEach(function (fid) {
          (map[fid] || []).forEach(function (e) {
            if (seen[e.id] || !model.byId[e.id]) return;
            seen[e.id] = true;
            row.push({ id: e.id, type: e.type, from: fid });
            next.push(e.id);
          });
        });
        if (!row.length) break;
        levels.push(row);
        frontier = next;
      }
      return levels;
    }

    return { up: walk(preds), down: walk(succs) };
  }

  function lineageSVG(model, node) {
    var chains = lineageChains(model, node.id, 3);
    if (!chains.up.length && !chains.down.length) {
      return '<div class="v muted">Isolated — no upstream or downstream chain.</div>';
    }

    var VW = 336, BH = 30, ROW = 58, PADT = 14;
    var rows = [];
    for (var i = chains.up.length - 1; i >= 0; i--) rows.push({ band: 'up', items: chains.up[i] });
    rows.push({ band: 'self', items: [{ id: node.id, type: null, from: null }] });
    chains.down.forEach(function (r) { rows.push({ band: 'down', items: r }); });

    var placed = {}, boxes = [], edges = [];
    rows.forEach(function (row, ri) {
      var y = PADT + ri * ROW;
      var n = Math.min(row.items.length, 4);
      var shown = row.items.slice(0, 4);
      var extra = row.items.length - shown.length;
      var gap = 7;
      var bw = Math.max(62, Math.min(160, (VW - 8 - (n - 1) * gap) / n));
      var totalW = n * bw + (n - 1) * gap;
      var x0 = (VW - totalW) / 2;
      shown.forEach(function (it, k) {
        var x = x0 + k * (bw + gap);
        placed[it.id] = { x: x + bw / 2, y: y, h: BH };
        boxes.push({ it: it, x: x, y: y, w: bw, band: row.band });
      });
      if (extra > 0) boxes.push({ more: extra, x: x0, y: y + BH + 1, w: totalW });
      if (row.band !== 'self') {
        shown.forEach(function (it) { edges.push({ it: it, band: row.band }); });
      }
    });

    var H = PADT + rows.length * ROW - (ROW - BH) + 12;
    var out = '<svg class="lineage" viewBox="0 0 ' + VW + ' ' + H + '" height="' + H + '">';

    // self-contained markers so the strip does not depend on the stage <defs>
    var mtypes = {};
    edges.forEach(function (e) { mtypes[e.it.type] = true; });
    out += '<defs>';
    Object.keys(mtypes).forEach(function (t) {
      out += '<marker id="ln-arrow-' + t.replace(/[^a-z0-9_]/gi, '_') + '" viewBox="0 -5 10 10"' +
             ' refX="10" refY="0" markerWidth="5" markerHeight="5" orient="auto">' +
             '<path d="M0,-4L9,0L0,4" fill="' + linkStyle(t).color + '"></path></marker>';
    });
    out += '</defs>';

    edges.forEach(function (e) {
      var a = placed[e.it.id], b = placed[e.it.from];
      if (!a || !b) return;
      // arrow always points downstream: upstream rows flow into their child
      var from = e.band === 'up' ? a : b;
      var to   = e.band === 'up' ? b : a;
      var y1 = from.y + from.h, y2 = to.y - 5;
      var st = linkStyle(e.it.type);
      var mid = (y1 + y2) / 2;
      out += '<path class="ln-edge" d="M' + from.x + ',' + y1 +
             'C' + from.x + ',' + mid + ' ' + to.x + ',' + mid + ' ' + to.x + ',' + y2 + '"' +
             ' stroke="' + st.color + '"' +
             (st.dash ? ' stroke-dasharray="' + st.dash + '"' : '') +
             ' marker-end="url(#ln-arrow-' + e.it.type.replace(/[^a-z0-9_]/gi, '_') + ')"></path>';
      out += '<text class="ln-rel" x="' + ((from.x + to.x) / 2 + 5) + '" y="' + (mid + 3) + '">' +
             esc(st.label) + '</text>';
    });

    boxes.forEach(function (b) {
      if (b.more) {
        out += '<text class="ln-band" x="' + b.x + '" y="' + (b.y + 9) + '">+' + b.more + ' more</text>';
        return;
      }
      var n2 = model.byId[b.it.id];
      var isSelf = b.band === 'self';
      var chars = Math.max(6, Math.floor(b.w / 5.4));
      out += '<g class="ln-g' + (isSelf ? ' self' : '') + '"' +
             (isSelf ? '' : ' data-goto="' + esc(b.it.id) + '"') + '>' +
             '<title>' + esc(n2.label) + '</title>' +
             '<rect class="ln-box" x="' + b.x + '" y="' + b.y + '" width="' + b.w +
             '" height="' + BH + '" rx="7"></rect>' +
             '<rect x="' + (b.x + 1.5) + '" y="' + (b.y + 1.5) + '" width="3.5" height="' + (BH - 3) +
             '" rx="1.8" fill="' + kindStyle(n2.kind).color + '"></rect>' +
             '<circle cx="' + (b.x + b.w - 8) + '" cy="' + (b.y + 8) + '" r="3.2" fill="' +
             (VERDICT_COLOR[verdictClass(n2.verdict)] || VERDICT_COLOR.descriptive) + '"></circle>';
      wrapLabel(n2.label, chars, 2).forEach(function (line, li) {
        out += '<text class="ln-text" x="' + (b.x + 9) + '" y="' + (b.y + 13 + li * 11) + '">' +
               esc(line) + '</text>';
      });
      out += '</g>';
    });

    out += '</svg>';
    return out;
  }

  function findingsBlock(node) {
    if (!node.verdict && !node.result && !node.caveats) return '';
    var cls = verdictClass(node.verdict);
    var h = '<div class="findings"><div class="hdr">Findings</div>';
    if (node.verdict) {
      h += '<p class="verdict-line v-' + cls + '"><span class="lede">' +
           esc(verdictWord(node.verdict).charAt(0).toUpperCase() + verdictWord(node.verdict).slice(1)) +
           ' —</span> ' + esc(node.verdict) + '</p>';
    }
    h += field('Result', node.result);
    h += field('Caveats', node.caveats);
    h += '</div>';
    return h;
  }

  function linkNotesBlock(nbrs) {
    var ins = nbrs.filter(function (n) { return n.dir === 'in'; });
    var outs = nbrs.filter(function (n) { return n.dir === 'out'; });
    if (!ins.length && !outs.length) return '';

    function list(items, heading) {
      if (!items.length) return '';
      var h = '<div class="field"><div class="k">' + heading + ' (' + items.length + ')</div>' +
              '<ul class="linknotes">';
      items.forEach(function (n) {
        var st = linkStyle(n.type);
        h += '<li><span class="rel" style="color:' + st.color + '">' + esc(st.label) + '</span> ' +
             '<span class="peer">' + esc(n.other.label) + '</span>' +
             (n.note ? '<span class="note">' + esc(n.note) + '</span>' : '') +
             '</li>';
      });
      return h + '</ul></div>';
    }

    return list(ins, 'Incoming links') + list(outs, 'Outgoing links');
  }

  function field(label, value) {
    if (value == null || value === '') return '';
    return '<div class="field"><div class="k">' + esc(label) + '</div>' +
           '<div class="v">' + esc(value) + '</div></div>';
  }

  function renderPanel(viewId, node) {
    var view = state.views[viewId];
    var model = view.model;
    var nbrs = neighborsOf(model, node.id);
    var html = '';

    html += '<h3>' + esc(node.label) + '</h3>';
    html += '<div class="badges">';
    if (model.mode === 'concept') {
      var cLabel = (node.community >= 0 && node.community < COMMUNITY_LABELS.length)
        ? node.community + ' · ' + COMMUNITY_LABELS[node.community] : 'unassigned';
      html += '<span class="badge kind">' + esc(node.raw.file_type || 'node') + '</span>';
      html += '<span class="badge kind" style="border-color:' + nodeColor(model, node) +
              ';color:' + nodeColor(model, node) + '">' + esc(cLabel) + '</span>';
    } else {
      html += '<span class="badge kind">' + esc(kindStyle(node.kind).label) + '</span>';
      if (node.verdict) {
        html += '<span class="badge verdict-' + verdictClass(node.verdict) + '">' +
                esc(verdictWord(node.verdict)) + '</span>';
      }
    }
    html += '</div>';

    if (model.mode === 'concept') {
      html += field('Source file', node.sourceFile);
      html += field('Location', node.sourceLocation);
      html += field('Author', node.author);
      if (node.sourceUrl) {
        html += '<div class="field"><div class="k">Source URL</div><div class="v">' +
                '<a href="' + esc(node.sourceUrl) + '" target="_blank" rel="noopener noreferrer" ' +
                'style="color:#6ea8fe">' + esc(truncate(node.sourceUrl, 60)) + '</a></div></div>';
      }
    } else {
      html += findingsBlock(node);
      html += '<div class="field"><div class="k">Lineage</div>' +
              lineageSVG(model, node) + '</div>';
      html += field('Design', node.design);
      html += statsTable(node.stats);
    }

    html += '<div class="field"><div class="k">Connections (' + nbrs.length + ')</div>';
    if (!nbrs.length) {
      html += '<div class="v muted">No recorded links.</div>';
    } else {
      html += '<ul class="neighbors">';
      nbrs.forEach(function (n) {
        var st = linkStyle(n.type);
        var arrow = n.dir === 'out' ? '→' : '←';
        html += '<li><button data-goto="' + esc(n.other.id) + '">' +
                '<span class="rel" style="color:' + st.color + '">' + arrow + ' ' + esc(st.label) + '</span>' +
                esc(n.other.label) +
                ((model.mode === 'concept' && n.note)
                  ? '<span class="note">' + esc(truncate(n.note, 150)) + '</span>' : '') +
                '</button></li>';
      });
      html += '</ul>';
    }
    html += '</div>';

    if (model.mode === 'atlas') {
      html += linkNotesBlock(nbrs);
    }

    if (model.mode === 'atlas') {
      html += '<button class="ask" id="ask-ai">Ask AI ↗</button>';
    }

    el.panelBody.innerHTML = html;
    el.panelBody.classList.remove('hidden');
    el.panelEmpty.classList.add('hidden');
    el.panelBody.scrollTop = 0;
    el.panelBody.parentElement.scrollTop = 0;

    Array.prototype.forEach.call(
      el.panelBody.querySelectorAll('[data-goto]'),
      function (btn) {
        btn.addEventListener('click', function () {
          selectNode(viewId, btn.getAttribute('data-goto'));
          centerOn(viewId, btn.getAttribute('data-goto'));
        });
      }
    );

    var ask = document.getElementById('ask-ai');
    if (ask) {
      ask.addEventListener('click', function () {
        var meta = paperMeta(model.paperId);
        var title = (meta && meta.title) || model.paperId;
        var names = nbrs.map(function (n) { return n.other.label; });
        var q = 'In "' + title + '", explain ' + node.label +
                ': its design, result (' + verdictWord(node.verdict) + '), and how it connects to ' +
                (names.length ? names.join('; ') : 'the rest of the paper') + '.';
        copyText(q);
      });
    }
  }

  function centerOn(viewId, id) {
    var view = state.views[viewId];
    if (!view) return;
    var node = view.model.byId[id];
    if (!node || node.x == null) return;
    var t = d3.zoomTransform(view.svg.node());
    var k = view.layout === 'flow' ? t.k : Math.max(t.k, 1);
    var tx = view.W / 2 - node.x * k;
    var ty = view.H / 2 - node.y * k;
    view.svg.transition().duration(500)
      .call(view.zoom.transform, d3.zoomIdentity.translate(tx, ty).scale(k));
  }

  // ---------------------------------------------------------------- search

  function applySearch() {
    var q = state.query.trim().toLowerCase();
    var view = state.views[state.view];
    if (!view) { el.searchCount.textContent = ''; return; }

    if (!q) {
      view.nodeSel.classed('dim', false).classed('hit', false);
      view.linkSel.classed('dim', false);
      el.searchCount.textContent = '';
      return;
    }

    var hits = {};
    view.model.nodes.forEach(function (n) {
      var hay = (n.label + ' ' + (n.kind || '') + ' ' + (n.design || '') + ' ' +
                 (n.result || '') + ' ' + (n.verdict || '') + ' ' +
                 (n.sourceFile || '') + ' ' + n.id).toLowerCase();
      if (hay.indexOf(q) !== -1) hits[n.id] = true;
    });

    var count = Object.keys(hits).length;
    view.nodeSel
      .classed('hit', function (d) { return !!hits[d.id]; })
      .classed('dim', function (d) { return !hits[d.id]; });
    view.linkSel.classed('dim', function (d) {
      var s = d.source.id || d.source, t = d.target.id || d.target;
      return !(hits[s] && hits[t]);
    });
    el.searchCount.textContent = count + ' match' + (count === 1 ? '' : 'es');
  }

  // ---------------------------------------------------------------- views

  function showEmpty(msg) {
    syncSummary();
    el.empty.innerHTML = msg;
    el.empty.classList.remove('hidden');
    el.legend.classList.add('hidden');
    el.svg.selectAll('*').remove();
    el.searchCount.textContent = '';
  }

  var ABOUT_HTML = [
    '<header class="about-hero">',
    '<h2>Precision-cliff research programme</h2>',
    '<p class="about-lede">Two companion papers on what an LLM proposal is actually made of: the template the model emits, and the served precision behind it. Both run on the same benchmark — circle packing, scored by an exact local evaluator rather than a judge — so every source of variance sits on the model side of the interface.</p>',
    '<p class="about-byline">Soham Shailesh Gugale · Independent researcher · <a href="mailto:28gugales@gmail.com">28gugales@gmail.com</a></p>',
    '</header>',

    '<div class="card paper-card">',
    '<div class="paper-tag">Paper 1</div>',
    '<h3>A Closed Form for What the Model Emits</h3>',
    '<p class="paper-sub">Template anchoring in unconditioned zero-shot circle packing.</p>',
    '<p>Asked to place N circles in a unit square with no parent program, no fitness feedback and no evaluator in context, a weak-tier model does not search. It reaches for a k×k grid of radius 1/(2k), sometimes with corner fillers, and truncates it when N does not fill the grid. Which template it reaches for is predictable in closed form: a nearest-square order k*(N) = round(√N) plus a value function over grid order and filler count fixes the modal output, and therefore its score, before any sampling. The predicted mode matched the empirical mode at all seven tested N; per-sample agreement runs 56–86% by cell, which is the modal frequency itself. Across three tiers, constructive ambition rises with nominal tier while execution validity rises then collapses — 78% → 100% → 13% valid at the primary 1e-6 tolerance. The anchoring is a property of unconditioned calls only: given a provably better in-family parent, 0 of 26 valid mutation samples return to the template, which is the regime discovery loops actually run in. A probe that lists the whole recipe family in the prompt separates choice from execution — the model picks the recipe the stated score table favours, then cannot build it, failing off-template in 30 of 31 invalid attempts. Point predictions and prompt hashes were registered before sampling, and two registered falsifiers triggered; both are reported as such.</p>',
    '<p class="paper-links"><a href="paper1.pdf" target="_blank" rel="noopener">Read the paper (PDF)</a> · <a href="https://github.com/28gugales-dev/precision-cliff-research" target="_blank" rel="noopener">Code, ledgers &amp; preregistrations</a><span class="updated-tag" id="upd-p1"></span></p>',
    '</div>',

    '<div class="card paper-card">',
    '<div class="paper-tag">Paper 2 · under review at TMLR</div>',
    '<h3>Served Precision Is Part of the Model</h3>',
    '<p class="paper-sub">A quantization cliff in proposal variation, and the limits of alias-addressed study.</p>',
    '<p>Quantizing a proposer\'s weights can leave every metric a discovery loop watches unchanged while collapsing the variation the loop depends on. Down a quantization ladder at 14B, viability and validity move by no amount detectable at n = 50 per rung, but at the 2-bit rung the proposer largely stops departing from its parent. Two registered outcomes carry the claim: an echo bound written into the runner before the run held on five never-sampled seeds at 79% (19/24) coordinate-verified parent-echo against 6% (1/17), and a must-differ probe returned coordinate-identical copies in 5 of 5 valid outputs under an explicit instruction not to copy. The failed proposals are coherent, well-formed near-copies, which is why every pass/fail instrument reports health. The cost is visible only at loop level: the 2-bit rung takes 1 accepted hill-climb step in 50 calls against 14–16 at the upper rungs, while final best score separates the rungs nowhere. The second half asks what this means for studies that address a model by alias, since served quantization is one of several serving-path variables an alias leaves unattested — and one the dependent measure is now known to be sensitive to. A forensic arm addressed only as <code>opus_alias</code> became untestable within six days: byte-identical prompts returned 30/30 valid against the original 4/30, so the hypothesis pair under test turned out to presuppose a stable referent it does not have. The paper closes with a repair protocol audited against itself, including one proposed instrument that was run on its own rows and withdrawn.</p>',
    '<p class="paper-links"><a href="paper2.pdf" target="_blank" rel="noopener">Read the paper (PDF)</a> · <a href="https://github.com/28gugales-dev/precision-cliff-research" target="_blank" rel="noopener">Code, ledgers &amp; preregistrations</a><span class="updated-tag" id="upd-p2"></span></p>',
    '</div>',

    '<div class="card">',
    '<h3>How to read the atlas</h3>',
    '<ul>',
    '<li><b>Paper 1 atlas / Paper 2 atlas</b> put every arm, wave, control, analysis, extension and headline claim on the map as a node — 55 in total, with 87 directed edges between them.</li>',
    '<li><b>Network or Flowchart.</b> Network is a force layout, good for seeing clusters. Flowchart lays the same nodes out left to right by dependency: anything with no prerequisite starts in the first column, everything else sits one column past its deepest prerequisite.</li>',
    '<li><b>Click any node</b> for its design, result, verdict and caveats, plus a lineage strip of what fed it and what it fed. Verdicts are colour-coded — green held, red disconfirmed, amber partial, grey descriptive. Node colour and shape encode kind; claim nodes are larger and gold.</li>',
    '<li><b>Edges are typed</b>: <i>feeds</i> and <i>informs</i> for supply of evidence, <i>controls_for</i> for a probe that bounds a result, <i>replicates</i>, <i>extends</i> and <i>scopes</i> for reach, <i>contrasts_with</i> and <i>disconfirms</i> for tension. Hover an edge to read the annotation behind it.</li>',
    '<li><b>Concept graph</b> shows 178 concepts auto-extracted across both papers, coloured by community, with edge opacity tracking extraction confidence. It is a reading aid, not a result.</li>',
    '<li><b>Search</b> filters the active view — matches stay lit, the rest dims. <b>Expand</b> takes the graph full-window (Esc to leave); <b>Reset view</b> restores the default zoom. Scroll to zoom, drag the background to pan, drag a node to pin it somewhere else.</li>',
    '</ul>',
    '</div>',

    '<div class="card">',
    '<h3>Provenance</h3>',
    '<p>Every figure on this map traces to a released script and a raw ledger row. Preregistrations are git ancestors of the sampling they govern, so the registration date is checkable rather than asserted — the full repository, including every ledger, replay script and preregistration, is public at <a href="https://github.com/28gugales-dev/precision-cliff-research" target="_blank" rel="noopener">github.com/28gugales-dev/precision-cliff-research</a>. Prose in both papers was model-assisted under the author\'s direction and disclosed there.</p>',
    '<p class="muted small">This atlas is generated from two data files: <code>arms.json</code>, the per-paper experiment ledger, and <code>graph.json</code>, a node-link export of the extracted concept graph. Both load at runtime.</p>',
    '<p id="about-status" class="muted small"></p>',
    '</div>',

    '<footer class="about-foot">Questions, or a request for the underlying data: <a href="mailto:28gugales@gmail.com">28gugales@gmail.com</a><span class="updated-tag" id="upd-site"></span></footer>'
  ].join('');

  function renderAbout() {
    el.stageTitle.textContent = 'About';
    el.stageSub.textContent = 'The research programme in three minutes, and how to use this atlas.';
    document.body.classList.add('is-about');
    syncSummary();
    el.wrap.classList.add('hidden');
    el.about.classList.remove('hidden');
    el.about.innerHTML = ABOUT_HTML;
    el.searchCount.textContent = '';

    var status = document.getElementById('about-status');
    if (status) {
      var bits = [];
      bits.push(state.arms
        ? 'arms.json loaded: ' + ((state.arms.arms || []).length) + ' nodes, ' +
          ((state.arms.links || []).length) + ' links' +
          (updWhen('arms_updated') ? ' · updated ' + esc(updWhen('arms_updated')) : '') + '.'
        : 'arms.json unavailable (' + esc(state.armsError || 'not found') + ').');
      bits.push(state.graph
        ? 'graph.json loaded: ' + ((state.graph.nodes || []).length) + ' nodes, ' +
          ((state.graph.links || []).length) + ' edges' +
          (updWhen('graph_updated') ? ' · updated ' + esc(updWhen('graph_updated')) : '') + '.'
        : 'graph.json unavailable (' + esc(state.graphError || 'not found') + ').');
      status.innerHTML = bits.join('<br>');
    }

    var u1 = document.getElementById('upd-p1');
    if (u1 && updWhen('paper1_pdf_updated')) {
      u1.textContent = 'PDF updated ' + updWhen('paper1_pdf_updated') +
        (updWhen('paper1_revision') ? ' (' + updWhen('paper1_revision') + ')' : '');
    }
    var u2 = document.getElementById('upd-p2');
    if (u2 && updWhen('paper2_pdf_updated')) {
      u2.textContent = 'PDF updated ' + updWhen('paper2_pdf_updated') +
        (updWhen('paper2_revision') ? ' (' + updWhen('paper2_revision') + ')' : '');
    }
    var us = document.getElementById('upd-site');
    if (us && updWhen('site_updated')) {
      us.textContent = 'site updated ' + updWhen('site_updated');
    }
  }

  function renderView(viewId) {
    state.view = viewId;
    document.body.classList.remove('is-about');
    el.about.classList.add('hidden');
    el.wrap.classList.remove('hidden');
    el.empty.classList.add('hidden');
    hideLinkTip();
    clearSelection(viewId);

    var isPaper = (viewId === 'paper1' || viewId === 'paper2');
    el.viewmode.classList.toggle('hidden', !isPaper);
    if (isPaper) {
      var mode = state.modes[viewId] || 'network';
      Array.prototype.forEach.call(el.viewmode.querySelectorAll('.mode'), function (b) {
        b.classList.toggle('is-active', b.getAttribute('data-mode') === mode);
      });
    }

    if (viewId === 'about') { renderAbout(); return; }

    var model = null;
    if (viewId === 'concept') {
      el.stageTitle.textContent = 'Concept graph';
      model = buildConceptModel();
      if (!model) {
        el.stageSub.textContent = '';
        showEmpty('<div><strong>graph.json could not be loaded</strong>' +
                  esc(state.graphError || 'unknown error') + '</div>');
        return;
      }
      el.stageSub.textContent = model.nodes.length + ' concepts · ' + model.links.length +
        ' edges · 12 communities. Colour is community, opacity is extraction confidence.';
      stampTitle(updWhen('graph_updated'));
    } else {
      var meta = paperMeta(viewId);
      el.stageTitle.textContent = (viewId === 'paper1' ? 'Paper 1 atlas' : 'Paper 2 atlas');
      model = buildAtlasModel(viewId);

      if (!model) {
        el.stageSub.textContent = '';
        showEmpty('<div><strong>dataset still generating — refresh</strong>' +
                  'arms.json is not available yet (' + esc(state.armsError || 'not found') +
                  '). The concept graph tab works in the meantime.</div>');
        return;
      }
      if (!model.nodes.length) {
        el.stageSub.textContent = '';
        showEmpty('<div><strong>No experiments recorded for this paper yet</strong>' +
                  'arms.json loaded, but it contains no entries with paper = "' + esc(viewId) + '".</div>');
        return;
      }
      el.stageSub.textContent = (meta && meta.claim)
        ? meta.claim
        : ((meta && meta.title) || '') + ' — ' + model.nodes.length + ' experiment nodes.';
      if (meta && meta.title && meta.claim) {
        el.stageTitle.textContent = meta.title;
      }
      stampTitle(updWhen('arms_updated'));
    }

    if (isPaper && state.modes[viewId] === 'flow') {
      var fv = renderFlow(viewId, model);
      el.stageSub.textContent += ' · flowchart: ' + fv.layers + ' layers' +
        (fv.broken ? ', ' + fv.broken + ' cycle edge' + (fv.broken === 1 ? '' : 's') + ' re-routed' : '');
    } else {
      renderGraph(viewId, model);
    }
    renderLegend(model);
    applySearch();
    syncSummary();
  }

  // ---------------------------------------------------------------- events

  el.tabs.addEventListener('click', function (e) {
    var btn = e.target.closest('.tab');
    if (!btn) return;
    Array.prototype.forEach.call(el.tabs.querySelectorAll('.tab'), function (b) {
      b.classList.toggle('is-active', b === btn);
    });
    renderView(btn.getAttribute('data-view'));
  });

  el.viewmode.addEventListener('click', function (e) {
    var btn = e.target.closest('.mode');
    if (!btn) return;
    var mode = btn.getAttribute('data-mode');
    if (state.modes[state.view] === mode) return;
    state.modes[state.view] = mode;
    renderView(state.view);
  });

  el.search.addEventListener('input', function () {
    state.query = el.search.value;
    applySearch();
  });

  el.reset.addEventListener('click', function () {
    var view = state.views[state.view];
    if (!view) return;
    view.svg.transition().duration(400)
      .call(view.zoom.transform, view.resetTransform || d3.zoomIdentity);
  });

  // re-measure the stage and re-fit / re-centre the active graph
  function refit() {
    var view = state.views[state.view];
    if (!view || el.wrap.classList.contains('hidden')) return;
    var box = el.wrap.getBoundingClientRect();
    var W = Math.max(320, box.width), H = Math.max(280, box.height);
    view.W = W; view.H = H;
    view.svg.attr('viewBox', '0 0 ' + W + ' ' + H);

    if (view.layout === 'flow') {
      var t = fitTransform(view.contentW, view.contentH, W, H);
      view.resetTransform = t;
      view.svg.call(view.zoom.transform, t);
      return;
    }
    if (!view.sim) return;

    view.sim.force('center', d3.forceCenter(W / 2, H / 2));
    view.sim.force('x', d3.forceX(W / 2).strength(0.03));
    view.sim.force('y', d3.forceY(H / 2).strength(0.05));
    view.sim.alpha(0.3).restart();
  }

  var resizeTimer = null;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(refit, 160);
  });

  // --------------------------------------------------- summary collapse

  function syncSummary() {
    var open = !!state.subOpen[state.view];
    el.stageSub.classList.toggle('is-clamped', !open);
    var overflows = open || el.stageSub.scrollHeight - el.stageSub.clientHeight > 1;
    el.subToggle.classList.toggle('hidden', !overflows);
    el.subToggle.textContent = open ? 'Show less' : 'Show more';
    el.subToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  el.subToggle.addEventListener('click', function () {
    state.subOpen[state.view] = !state.subOpen[state.view];
    syncSummary();
    refit();
  });

  // --------------------------------------------------- expanded stage

  function setExpanded(on) {
    if (state.expanded === on) return;
    state.expanded = on;
    document.body.classList.toggle('is-expanded', on);
    el.expand.textContent = on ? 'Exit' : 'Expand';
    if (!on) syncSummary();
    requestAnimationFrame(refit);
  }

  el.expand.addEventListener('click', function () { setExpanded(!state.expanded); });

  // phones: legend renders collapsed (CSS); tapping it toggles open.
  // max-height set inline because some mobile renderers miss the late
  // class-rule recalc inside the media block.
  el.legend.addEventListener('click', function () {
    if (window.matchMedia('(max-width:640px)').matches) {
      var open = el.legend.classList.toggle('open');
      el.legend.style.maxHeight = open ? '34vh' : '';
      el.legend.style.overflow = open ? 'auto' : '';
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement !== el.search) {
      e.preventDefault();
      setExpanded(false);   // search box lives behind the expanded stage
      el.search.focus();
    } else if (e.key === 'Escape') {
      if (state.expanded) {
        setExpanded(false);
      } else if (document.activeElement === el.search) {
        el.search.value = ''; state.query = ''; applySearch(); el.search.blur();
      } else {
        clearSelection(state.view);
      }
    }
  });

  // ---------------------------------------------------------------- boot

  showEmpty('<div><strong>Loading data…</strong>Reading arms.json and graph.json.</div>');

  loadAll().then(function () { renderView('paper1'); });
})();
