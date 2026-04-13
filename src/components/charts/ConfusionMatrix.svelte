<script>
  export let matrix = [[0,0],[0,0]];
  export let labels = ['Uninfected', 'Parasitized'];
  export let title = '';

  function getColor(value, max) {
    const ratio = max > 0 ? value / max : 0;
    if (ratio > 0.7) return { bg: 'rgba(99, 102, 241, 0.75)', text: '#ffffff' };
    if (ratio > 0.4) return { bg: 'rgba(99, 102, 241, 0.45)', text: '#ffffff' };
    if (ratio > 0.15) return { bg: 'rgba(99, 102, 241, 0.22)', text: 'var(--cm-text)' };
    return { bg: 'rgba(99, 102, 241, 0.08)', text: 'var(--cm-text)' };
  }

  $: maxVal = Math.max(...matrix.flat());
  $: total = matrix.flat().reduce((a, b) => a + b, 0);
  $: accuracy = total > 0 ? ((matrix[0][0] + matrix[1][1]) / total * 100).toFixed(1) : '0';
</script>

<div class="cm-wrapper">
  {#if title}
    <p class="cm-title">{title}</p>
  {/if}

  <div class="cm-layout">
    <!-- Y axis label -->
    <div class="cm-y-axis">
      <span class="cm-axis-text">Actual</span>
    </div>

    <!-- Y row labels + grid -->
    <div class="cm-body">
      <div class="cm-row-labels">
        <span>{labels[0]}</span>
        <span>{labels[1]}</span>
      </div>
      <div class="cm-grid">
        {#each matrix as row, i}
          {#each row as val, j}
            {@const c = getColor(val, maxVal)}
            <div class="cm-cell" style="background-color: {c.bg}; color: {c.text};">
              <span class="cm-value">{val.toLocaleString()}</span>
            </div>
          {/each}
        {/each}
      </div>
    </div>
  </div>

  <!-- X col labels -->
  <div class="cm-col-labels">
    <span>{labels[0]}</span>
    <span>{labels[1]}</span>
  </div>
  <p class="cm-x-axis-text">Predicted</p>
  <p class="cm-accuracy">Accuracy: {accuracy}%</p>
</div>

<style>
  .cm-wrapper {
    --cm-text: #374151;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.75rem 0;
  }
  :global(.dark) .cm-wrapper {
    --cm-text: #d1d5db;
  }
  .cm-title {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--cm-text);
    margin: 0 0 0.75rem 0;
  }
  .cm-layout {
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }
  .cm-y-axis {
    display: flex;
    align-items: center;
  }
  .cm-axis-text {
    writing-mode: vertical-lr;
    transform: rotate(180deg);
    font-size: 0.6875rem;
    font-weight: 500;
    color: var(--cm-text);
    opacity: 0.6;
  }
  .cm-body {
    display: flex;
    align-items: center;
    gap: 0.375rem;
  }
  .cm-row-labels {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    height: 180px;
    font-size: 0.625rem;
    color: var(--cm-text);
    opacity: 0.7;
    text-align: right;
  }
  .cm-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3px;
    width: 180px;
    height: 180px;
  }
  .cm-cell {
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
    transition: transform 0.15s;
    cursor: default;
  }
  .cm-cell:hover {
    transform: scale(1.04);
  }
  .cm-value {
    font-size: 0.8125rem;
    font-weight: 700;
    font-family: 'Inter', sans-serif;
  }
  .cm-col-labels {
    display: flex;
    justify-content: space-around;
    width: 180px;
    margin-left: auto;
    margin-right: auto;
    margin-top: 0.25rem;
    font-size: 0.625rem;
    color: var(--cm-text);
    opacity: 0.7;
  }
  .cm-x-axis-text {
    font-size: 0.6875rem;
    font-weight: 500;
    color: var(--cm-text);
    opacity: 0.6;
    margin: 0.25rem 0 0 0;
  }
  .cm-accuracy {
    font-size: 0.75rem;
    color: var(--cm-text);
    opacity: 0.5;
    margin: 0.5rem 0 0 0;
  }
</style>
