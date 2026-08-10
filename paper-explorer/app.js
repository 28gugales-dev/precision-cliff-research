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
    linktip:     document.getElementById('linktip'),
    about:       document.getElementById('about'),
    panelEmpty:  document.getElementById('panel-empty'),
    panelBody:   document.getElementById('panel-body'),
    toast:       document.getElementById('toast'),
    reset:       document.getElementById('btn-reset')
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
    return Promise.all([a, g]);
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
      .on('mousemove', function (event, d) { showLinkTip(event, d); })
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
      nodeSel: nodeSel, linkSel: linkSel, hitSel: hitSel, W: W, H: H
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

  function showLinkTip(event, d) {
    var wrapBox = el.wrap.getBoundingClientRect();
    var st = linkStyle(d.type);
    var sLabel = (d.source && d.source.label) || d.source;
    var tLabel = (d.target && d.target.label) || d.target;
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
  }

  function selectNode(viewId, id) {
    var view = state.views[viewId];
    if (!view) return;
    var model = view.model;
    var node = model.byId[id];
    if (!node) return;

    state.selected[viewId] = id;
    view.nodeSel.classed('selected', function (d) { return d.id === id; });
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
      html += field('Design', node.design);
      html += field('Result', node.result);
      html += field('Verdict', node.verdict);
      html += field('Caveats', node.caveats);
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
                (n.note ? '<span class="note">' + esc(truncate(n.note, 150)) + '</span>' : '') +
                '</button></li>';
      });
      html += '</ul>';
    }
    html += '</div>';

    if (model.mode === 'atlas') {
      html += '<button class="ask" id="ask-ai">Ask AI ↗</button>';
    }

    el.panelBody.innerHTML = html;
    el.panelBody.classList.remove('hidden');
    el.panelEmpty.classList.add('hidden');
    el.panelBody.scrollTop = 0;
    el.panelBody.parentElement.scrollTop = 0;

    Array.prototype.forEach.call(
      el.panelBody.querySelectorAll('button[data-goto]'),
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
    var k = Math.max(t.k, 1);
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
    el.empty.innerHTML = msg;
    el.empty.classList.remove('hidden');
    el.legend.classList.add('hidden');
    el.svg.selectAll('*').remove();
    el.searchCount.textContent = '';
  }

  var ABOUT_HTML = [
    '<div class="card">',
    '<h3 style="margin-top:0">What this is</h3>',
    '<p>An interactive map of the experiments behind two precision-cliff papers. Each atlas view shows one paper\'s arms, waves, controls, analyses and extensions as a force-directed graph, with directed edges recording how one piece of evidence informs, controls for, disconfirms, scopes or extends another.</p>',
    '</div>',
    '<div class="card">',
    '<h3 style="margin-top:0">How to read it</h3>',
    '<ul>',
    '<li><b>Node colour and shape</b> encode kind — arm, wave, control, analysis, extension. Claim nodes are larger and gold.</li>',
    '<li><b>Edge colour and dashing</b> encode link type; hover an edge for the annotation behind it.</li>',
    '<li><b>Click a node</b> for design, result, verdict, caveats, key figures and every connection. Verdicts are colour-coded: green held, red disconfirmed, amber partial, grey descriptive.</li>',
    '<li><b>Ask AI ↗</b> copies a ready-to-paste question about the selected experiment and its neighbours.</li>',
    '<li><b>Concept graph</b> renders the full extracted knowledge graph, coloured by community, with edge opacity tracking extraction confidence.</li>',
    '</ul>',
    '</div>',
    '<div class="card">',
    '<h3 style="margin-top:0">Controls</h3>',
    '<ul>',
    '<li>Scroll or pinch to zoom, drag the background to pan, drag a node to reposition it.</li>',
    '<li>The search box filters the active view — matches keep full colour, everything else dims.</li>',
    '<li><code>Reset view</code> restores the default zoom.</li>',
    '</ul>',
    '</div>',
    '<div class="card">',
    '<h3 style="margin-top:0">Data</h3>',
    '<p><code>arms.json</code> holds the per-paper experiment ledger; <code>graph.json</code> is a networkx node-link export of the extracted concept graph. Both are loaded at runtime, so refreshing picks up regenerated data without a rebuild.</p>',
    '<p id="about-status" class="muted"></p>',
    '</div>'
  ].join('');

  function renderAbout() {
    el.stageTitle.textContent = 'About';
    el.stageSub.textContent = 'How the atlas is built and how to read it.';
    el.wrap.classList.add('hidden');
    el.about.classList.remove('hidden');
    el.about.innerHTML = ABOUT_HTML;
    el.searchCount.textContent = '';

    var status = document.getElementById('about-status');
    if (status) {
      var bits = [];
      bits.push(state.arms
        ? 'arms.json loaded: ' + ((state.arms.arms || []).length) + ' nodes, ' +
          ((state.arms.links || []).length) + ' links.'
        : 'arms.json unavailable (' + esc(state.armsError || 'not found') + ').');
      bits.push(state.graph
        ? 'graph.json loaded: ' + ((state.graph.nodes || []).length) + ' nodes, ' +
          ((state.graph.links || []).length) + ' edges.'
        : 'graph.json unavailable (' + esc(state.graphError || 'not found') + ').');
      status.innerHTML = bits.join('<br>');
    }
  }

  function renderView(viewId) {
    state.view = viewId;
    el.about.classList.add('hidden');
    el.wrap.classList.remove('hidden');
    el.empty.classList.add('hidden');
    hideLinkTip();
    clearSelection(viewId);

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
    }

    renderGraph(viewId, model);
    renderLegend(model);
    applySearch();
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

  el.search.addEventListener('input', function () {
    state.query = el.search.value;
    applySearch();
  });

  el.reset.addEventListener('click', function () {
    var view = state.views[state.view];
    if (!view) return;
    view.svg.transition().duration(400).call(view.zoom.transform, d3.zoomIdentity);
  });

  var resizeTimer = null;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      var view = state.views[state.view];
      if (!view || el.wrap.classList.contains('hidden')) return;
      var box = el.wrap.getBoundingClientRect();
      var W = Math.max(320, box.width), H = Math.max(280, box.height);
      view.W = W; view.H = H;
      view.svg.attr('viewBox', '0 0 ' + W + ' ' + H);
      view.sim.force('center', d3.forceCenter(W / 2, H / 2));
      view.sim.force('x', d3.forceX(W / 2).strength(0.03));
      view.sim.force('y', d3.forceY(H / 2).strength(0.05));
      view.sim.alpha(0.3).restart();
    }, 160);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement !== el.search) {
      e.preventDefault(); el.search.focus();
    } else if (e.key === 'Escape') {
      if (document.activeElement === el.search) {
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
