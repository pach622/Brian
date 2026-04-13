<script>
  import { onMount, onDestroy } from 'svelte';
  import { Chart } from 'chart.js/auto';

  export let labels = [];
  export let datasets = [];
  export let title = '';
  export let subtitle = '';
  export let xLabel = '';
  export let yLabel = '';
  export let horizontal = false;
  export let stacked = false;
  export let showLegend = true;
  export let aspectRatio = 1.8;
  export let formatValues = '';

  let canvas;
  let chart;
  let observer;

  function isDark() {
    return document.documentElement.classList.contains('dark');
  }

  function colors() {
    const d = isDark();
    return {
      text: d ? '#d1d5db' : '#374151',
      grid: d ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.05)',
      tooltipBg: d ? '#1f2937' : '#ffffff',
      tooltipBorder: d ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
    };
  }

  function buildChart() {
    if (chart) chart.destroy();
    const c = colors();

    const processedDatasets = datasets.map(ds => ({
      ...ds,
      borderRadius: ds.borderRadius ?? 4,
      borderSkipped: false,
    }));

    chart = new Chart(canvas, {
      type: 'bar',
      data: { labels, datasets: processedDatasets },
      options: {
        indexAxis: horizontal ? 'y' : 'x',
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          title: {
            display: !!title,
            text: title,
            color: c.text,
            font: { size: 14, weight: '600', family: 'Inter, sans-serif' },
            padding: { bottom: subtitle ? 0 : 12 },
          },
          subtitle: {
            display: !!subtitle,
            text: subtitle,
            color: c.text + '99',
            font: { size: 12, family: 'Inter, sans-serif' },
            padding: { bottom: 12 },
          },
          legend: {
            display: showLegend && datasets.length > 1,
            labels: {
              color: c.text,
              usePointStyle: true,
              pointStyle: 'rectRounded',
              padding: 16,
              font: { size: 12, family: 'Inter, sans-serif' },
            },
          },
          tooltip: {
            backgroundColor: c.tooltipBg,
            titleColor: c.text,
            bodyColor: c.text,
            borderColor: c.tooltipBorder,
            borderWidth: 1,
            cornerRadius: 8,
            padding: 10,
            titleFont: { family: 'Inter, sans-serif' },
            bodyFont: { family: 'Inter, sans-serif' },
            callbacks: formatValues === 'percent' ? {
              label: (ctx) => `${ctx.dataset.label}: ${ctx.parsed[horizontal ? 'x' : 'y'].toFixed(1)}%`
            } : formatValues === 'compact' ? {
              label: (ctx) => {
                const val = ctx.parsed[horizontal ? 'x' : 'y'];
                const formatted = val >= 1000 ? (val / 1000).toFixed(0) + 'K' : val;
                return `${ctx.dataset.label}: ${formatted}`;
              }
            } : {},
          },
        },
        scales: {
          x: {
            stacked,
            title: { display: !!xLabel, text: xLabel, color: c.text, font: { size: 12, family: 'Inter, sans-serif' } },
            ticks: {
              color: c.text,
              font: { size: 11, family: 'Inter, sans-serif' },
              maxRotation: horizontal ? 0 : 45,
            },
            grid: { color: c.grid, drawBorder: false },
            border: { display: false },
          },
          y: {
            stacked,
            title: { display: !!yLabel, text: yLabel, color: c.text, font: { size: 12, family: 'Inter, sans-serif' } },
            ticks: {
              color: c.text,
              font: { size: 11, family: 'Inter, sans-serif' },
              callback: formatValues === 'compact' ? function(value) {
                return value >= 1000 ? (value / 1000).toFixed(0) + 'K' : value;
              } : undefined,
            },
            grid: { color: c.grid, drawBorder: false },
            border: { display: false },
          },
        },
      },
    });
  }

  onMount(() => {
    buildChart();
    observer = new MutationObserver(() => buildChart());
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  });

  onDestroy(() => {
    if (chart) chart.destroy();
    if (observer) observer.disconnect();
  });
</script>

<div class="chart-wrap">
  <canvas bind:this={canvas}></canvas>
</div>

<style>
  .chart-wrap {
    position: relative;
    width: 100%;
  }
</style>
