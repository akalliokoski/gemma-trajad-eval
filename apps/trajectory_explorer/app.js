const dataBundle = window.__TRAJAD_EXPLORER_DATA__ || {};
const overview = dataBundle.overview || {};
const samplesPayload = dataBundle.samples || { samples: [] };
const training = dataBundle.training || {};
const evaluation = dataBundle.evaluation || {};

const roleColors = {
  system: '#fbbf24',
  user: '#22d3ee',
  assistant: '#34d399',
  tool: '#a78bfa',
};

let selectedSample = samplesPayload.samples[0] || null;
let selectedStepIndex = selectedSample?.messages?.[0]?.absolute_index ?? null;
let selectedTaxonomyId = selectedSample?.anomaly_type ?? null;

function $(id) {
  return document.getElementById(id);
}

function fmtLabel(value) {
  return String(value).replaceAll('_', ' ');
}

function setSelectedSample(sample) {
  selectedSample = sample || selectedSample;
  selectedStepIndex = selectedSample?.bad_step ?? selectedSample?.messages?.[0]?.absolute_index ?? null;
  selectedTaxonomyId = selectedSample?.anomaly_type ?? selectedTaxonomyId ?? null;
}

function findSampleForTaxonomy(taxonomyId) {
  if (!taxonomyId) return samplesPayload.samples[0] || null;
  return samplesPayload.samples.find((sample) => sample.anomaly_type === taxonomyId)
    || samplesPayload.samples.find((sample) => sample.sample_kind === 'anomalous')
    || samplesPayload.samples[0]
    || null;
}

function buildHero() {
  const pills = [
    'Static HTML/CSS/JS first slice',
    `Reference: ${overview.project?.reference_visualization?.github || 'interactive-turboquant'}`,
    'Canvas timeline + exported payload bundle',
    'Training + evaluation future path included from day one',
  ];
  $('hero-pills').innerHTML = pills.map((pill) => `<div class="pill">${pill}</div>`).join('');

  const counts = overview.counts || {};
  const stats = [
    ['Raw traces', counts.raw_traces ?? '—'],
    ['Processed examples', counts.processed_examples ?? '—'],
    ['Normal examples', counts.normal_examples ?? '—'],
    ['Anomalous examples', counts.anomalous_examples ?? '—'],
    ['Train split', counts.train ?? '—'],
    ['Dev split', counts.dev ?? '—'],
    ['Test split', counts.test ?? '—'],
  ];
  $('hero-stats').innerHTML = stats
    .map(([label, value]) => `<div class="stat"><strong>${value}</strong>${label}</div>`)
    .join('');
}

function buildPipeline() {
  const stages = [
    ['Sources', 'Hermes filtered traces + optional reasoning traces'],
    ['Dataset builder', 'Normalize trajectories and generate perturbation variants'],
    ['Processed artifacts', 'Train/dev/test JSONL plus diagnostics'],
    ['SFT formatting', 'Prepare binary, localize, and joint chat training sets'],
    ['Training', 'Local-first Gemma adapters on E2B first, E4B later'],
    ['Evaluation', 'Diagnostics now, run metrics later'],
  ];
  $('pipeline-overview').innerHTML = stages
    .map(([title, body]) => `<div class="stage"><div class="stage-title">${title}</div><p>${body}</p></div>`)
    .join('');
}

function buildTrajectoryControls() {
  $('trajectory-controls').innerHTML = samplesPayload.samples
    .map((sample) => {
      const active = selectedSample?.id === sample.id ? 'active' : '';
      return `<button class="selector ${active}" data-sample-id="${sample.id}">${sample.sample_kind}: ${sample.id}</button>`;
    })
    .join('');

  document.querySelectorAll('button.selector').forEach((button) => {
    button.addEventListener('click', () => {
      const sample = samplesPayload.samples.find((entry) => entry.id === button.dataset.sampleId) || selectedSample;
      setSelectedSample(sample);
      renderTrajectorySection();
      buildDatasetSummary();
    });
  });
}

function drawTrajectoryCanvas() {
  const canvas = $('trajectory-canvas');
  const ctx = canvas.getContext('2d');
  const rootStyle = getComputedStyle(document.documentElement);
  const bg = '#020617';
  const border = rootStyle.getPropertyValue('--border').trim();
  const accent = rootStyle.getPropertyValue('--accent').trim();
  const danger = rootStyle.getPropertyValue('--danger').trim();
  const text = rootStyle.getPropertyValue('--text').trim();
  const muted = rootStyle.getPropertyValue('--muted').trim();

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  if (!selectedSample || !selectedSample.messages?.length) {
    ctx.fillStyle = text;
    ctx.font = '16px sans-serif';
    ctx.fillText('No sample data loaded.', 24, 40);
    return;
  }

  const messages = selectedSample.messages;
  const paddingX = 40;
  const y = 120;
  const stepGap = (canvas.width - paddingX * 2) / Math.max(1, messages.length - 1);

  ctx.strokeStyle = border;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(paddingX, y);
  ctx.lineTo(canvas.width - paddingX, y);
  ctx.stroke();

  ctx.fillStyle = text;
  ctx.font = '14px sans-serif';
  ctx.fillText(`Window ${selectedSample.window.start}–${selectedSample.window.end - 1} of ${selectedSample.message_count} total steps`, 24, 34);
  ctx.fillStyle = muted;
  ctx.fillText('Click a step card below to inspect the message excerpt.', 24, 56);

  messages.forEach((message, index) => {
    const x = paddingX + stepGap * index;
    const isFocused = selectedSample.diff_hints.focus_indexes.includes(message.absolute_index);
    const isSelected = selectedStepIndex === message.absolute_index;
    ctx.fillStyle = isFocused ? danger : roleColors[message.role] || accent;
    ctx.beginPath();
    ctx.arc(x, y, isSelected ? 14 : 10, 0, Math.PI * 2);
    ctx.fill();

    if (isSelected) {
      ctx.strokeStyle = accent;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(x, y, 20, 0, Math.PI * 2);
      ctx.stroke();
    }

    ctx.fillStyle = text;
    ctx.font = '12px sans-serif';
    ctx.fillText(String(message.absolute_index), x - 8, y - 24);
    ctx.fillStyle = muted;
    ctx.fillText(message.role, x - 20, y + 34);

    if (message.absolute_index === selectedSample.bad_step) {
      ctx.fillStyle = danger;
      ctx.fillText('bad_step', x - 20, y + 54);
    }
  });
}

function buildTrajectoryBadges() {
  if (!selectedSample) return;
  const badges = [
    `sample: ${selectedSample.sample_kind}`,
    `split: ${selectedSample.split}`,
    `messages: ${selectedSample.message_count}`,
    `anomalous: ${selectedSample.is_anomalous}`,
  ];

  if (selectedSample.anomaly_type) badges.push(`type: ${fmtLabel(selectedSample.anomaly_type)}`);
  if (selectedSample.anomaly_class) badges.push(`class: ${fmtLabel(selectedSample.anomaly_class)}`);
  if (selectedSample.generation_rule) badges.push(`rule: ${selectedSample.generation_rule}`);
  if (selectedSample.bad_step !== null && selectedSample.bad_step !== undefined) badges.push(`bad_step: ${selectedSample.bad_step}`);

  $('trajectory-badges').innerHTML = badges.map((badge) => `<span class="label">${badge}</span>`).join('');
}

function buildLocalizationSummary() {
  if (!selectedSample) {
    $('localization-summary').innerHTML = '<div class="empty-state">No localization data loaded.</div>';
    return;
  }

  const totalSteps = selectedSample.message_count ?? selectedSample.messages.length;
  const badStep = selectedSample.bad_step;
  const mode = badStep === null || badStep === undefined ? 'normal trajectory' : `bad_step at ${badStep}`;
  $('localization-summary').innerHTML = `
    <div class="message-index">Localization view</div>
    <p>${mode}. Window ${selectedSample.window.start}–${selectedSample.window.end - 1} is currently exported for detailed inspection.</p>
    <div class="message-meta">Total steps: ${totalSteps} • focused indexes: ${(selectedSample.diff_hints.focus_indexes || []).join(', ') || 'none'}</div>
  `;
}

function buildLocalizationStrip() {
  if (!selectedSample) {
    $('localization-strip').innerHTML = '';
    return;
  }

  const totalSteps = selectedSample.message_count ?? selectedSample.messages.length;
  const visibleIndexes = new Set(selectedSample.messages.map((message) => message.absolute_index));
  $('localization-strip').innerHTML = Array.from({ length: totalSteps }, (_, index) => {
    const classes = ['message-card'];
    if (index === selectedSample.bad_step) classes.push('active');
    const tags = [];
    if (visibleIndexes.has(index)) tags.push('window');
    if (index === selectedSample.bad_step) tags.push('bad_step');
    return `
      <button class="${classes.join(' ')}" data-localization-step="${index}">
        <span class="message-index">${index}</span>
        <div class="message-meta">${tags.join(' • ') || 'step'}</div>
      </button>
    `;
  }).join('');

  document.querySelectorAll('[data-localization-step]').forEach((button) => {
    button.addEventListener('click', () => {
      selectedStepIndex = Number(button.dataset.localizationStep);
      renderTrajectorySection();
    });
  });
}

function buildMessageGrid() {
  $('trajectory-messages').innerHTML = selectedSample.messages
    .map((message) => {
      const active = selectedStepIndex === message.absolute_index ? 'active' : '';
      return `
        <button class="message-card ${active}" data-step-index="${message.absolute_index}">
          <span class="message-index">Step ${message.absolute_index}</span>
          <div class="message-meta role-${message.role}">${message.role}${message.tool_name ? ` • ${message.tool_name}` : ''}</div>
          <div>${message.content_excerpt}</div>
        </button>
      `;
    })
    .join('');

  document.querySelectorAll('.message-card').forEach((button) => {
    button.addEventListener('click', () => {
      selectedStepIndex = Number(button.dataset.stepIndex);
      renderTrajectorySection();
    });
  });
}

function buildTrajectoryDetail() {
  const message = selectedSample.messages.find((item) => item.absolute_index === selectedStepIndex) || selectedSample.messages[0];
  if (!message) {
    $('trajectory-detail').innerHTML = '<div class="empty-state">No message selected.</div>';
    return;
  }

  $('trajectory-detail').innerHTML = `
    <div class="message-index">Selected step ${message.absolute_index}</div>
    <div class="message-meta role-${message.role}">${message.role}${message.tool_name ? ` • ${message.tool_name}` : ''}</div>
    <p>${message.content_excerpt}</p>
    <div>${message.has_tool_call ? '<span class="label">tool_call</span>' : ''}${message.has_tool_response ? '<span class="label">tool_response</span>' : ''}</div>
  `;
}

function buildSourcePairDetail() {
  if (!selectedSample.source_pair) {
    $('source-pair-detail').innerHTML = '<div class="message-index">Source pair</div><p class="empty-state">No source-pair comparison exported for this sample.</p>';
    $('source-pair-grid').innerHTML = '';
    return;
  }

  const sourceMessage = selectedSample.source_pair.messages.find((item) => item.absolute_index === selectedStepIndex);
  $('source-pair-detail').innerHTML = `
    <div class="message-index">Source pair ${selectedSample.source_pair.id}</div>
    <p>${sourceMessage ? sourceMessage.content_excerpt : 'This source step falls outside the currently exported window.'}</p>
    <div class="message-meta">Changed indexes: ${selectedSample.diff_hints.changed_message_indexes.join(', ') || 'none'}</div>
  `;

  $('source-pair-grid').innerHTML = selectedSample.source_pair.messages
    .map((message) => {
      const changed = selectedSample.diff_hints.changed_message_indexes.includes(message.absolute_index);
      const active = selectedStepIndex === message.absolute_index ? 'active' : '';
      return `
        <div class="message-card ${active}">
          <span class="message-index">Source step ${message.absolute_index}</span>
          <div class="message-meta role-${message.role}">${message.role}${message.tool_name ? ` • ${message.tool_name}` : ''}${changed ? ' • changed' : ''}</div>
          <div>${message.content_excerpt}</div>
        </div>
      `;
    })
    .join('');
}

function renderTrajectorySection() {
  buildTrajectoryControls();
  drawTrajectoryCanvas();
  buildTrajectoryBadges();
  buildLocalizationSummary();
  buildLocalizationStrip();
  buildMessageGrid();
  buildTrajectoryDetail();
  buildSourcePairDetail();
}

function buildDatasetSummary() {
  const counts = overview.counts || {};
  const stats = [
    ['Unique source traces', counts.raw_traces ?? '—'],
    ['Processed examples', counts.processed_examples ?? '—'],
    ['Normal examples', counts.normal_examples ?? '—'],
    ['Anomalous examples', counts.anomalous_examples ?? '—'],
    ['Train', counts.train ?? '—'],
    ['Dev', counts.dev ?? '—'],
    ['Test', counts.test ?? '—'],
  ];
  $('dataset-stats').innerHTML = stats
    .map(([label, value]) => `<div class="stat"><strong>${value}</strong>${label}</div>`)
    .join('');

  const selectedTaxonomyLabel = selectedTaxonomyId ? fmtLabel(selectedTaxonomyId) : 'none selected';
  const taxonomyMode = overview.taxonomy_mode || 'unknown';
  $('taxonomy-status').innerHTML = `
    <div class="message-index">Taxonomy interaction</div>
    <p>Click a taxonomy card to jump to the matching anomalous sample when one is available in the exported slice.</p>
    <div class="message-meta">Selected taxonomy: ${selectedTaxonomyLabel} • mode: ${taxonomyMode}</div>
  `;

  $('taxonomy-grid').innerHTML = (overview.taxonomy || [])
    .map((entry) => {
      const active = selectedTaxonomyId === entry.id ? 'active' : '';
      return `
        <button class="rule-card selector ${active}" data-taxonomy-id="${entry.id}">
          <div class="metric-value">${entry.count ?? '—'}</div>
          <div>${fmtLabel(entry.label || entry.id)}</div>
          <div class="meta">class: ${fmtLabel(entry.anomaly_class || 'unknown')}</div>
        </button>
      `;
    })
    .join('');

  document.querySelectorAll('[data-taxonomy-id]').forEach((button) => {
    button.addEventListener('click', () => {
      selectedTaxonomyId = button.dataset.taxonomyId;
      const sample = findSampleForTaxonomy(selectedTaxonomyId);
      if (sample) {
        setSelectedSample(sample);
        renderTrajectorySection();
      }
      buildDatasetSummary();
    });
  });

  $('rule-coverage').innerHTML = (evaluation.perturbation_rules || [])
    .map((rule) => `
      <div class="rule-card">
        <div class="metric-value">${Math.round((rule.success_rate || 0) * 100)}%</div>
        <div>${rule.rule_name}</div>
        <div class="meta">eligible ${rule.eligible} • failed ${rule.failed}</div>
      </div>
    `)
    .join('');
}

function buildTrainingLifecycle() {
  $('training-stages').innerHTML = (training.training_stages || [])
    .map((stage) => `
      <div class="task-card">
        <div class="task-title">${stage.label}</div>
        <div class="meta"><code>${stage.script}</code></div>
        <p>Input: <code>${stage.input_artifact}</code></p>
        <p>Output: <code>${stage.output_artifact}</code></p>
      </div>
    `)
    .join('');

  $('task-modes').innerHTML = (training.task_modes || [])
    .map((task) => `
      <div class="task-card">
        <div class="task-title">${task.task}</div>
        <p>train ${task.train_rows} • dev ${task.dev_rows} • test ${task.test_rows}</p>
        <div class="meta"><code>${task.prompt_file}</code></div>
      </div>
    `)
    .join('');

  $('training-notes').innerHTML = (training.run_notes || [])
    .map((note) => `<div class="note-card">${note}</div>`)
    .join('');
}

function buildEvaluationSummary() {
  const splitCounts = evaluation.split_counts || {};
  const stats = [
    ['Train examples', splitCounts.train ?? '—'],
    ['Dev examples', splitCounts.dev ?? '—'],
    ['Test examples', splitCounts.test ?? '—'],
    ['Normal examples', evaluation.normal_examples ?? '—'],
    ['Anomalous examples', evaluation.anomalous_examples ?? '—'],
    ['Rule diagnostics', (evaluation.perturbation_rules || []).length],
    ['Committed run reports', (evaluation.reported_runs || []).length],
  ];
  $('evaluation-stats').innerHTML = stats
    .map(([label, value]) => `<div class="stat"><strong>${value}</strong>${label}</div>`)
    .join('');

  $('anomaly-type-grid').innerHTML = (evaluation.anomaly_type_distribution || [])
    .map((entry) => `
      <div class="rule-card">
        <div class="metric-value">${entry.count ?? '—'}</div>
        <div>${fmtLabel(entry.label || entry.id)}</div>
      </div>
    `)
    .join('');

  $('evaluation-notes').innerHTML = (evaluation.notes || [])
    .map((note) => `<div class="note-card">${note}</div>`)
    .join('');
}

buildHero();
buildPipeline();
renderTrajectorySection();
buildDatasetSummary();
buildTrainingLifecycle();
buildEvaluationSummary();
