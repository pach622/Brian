<script>
  import { onMount, onDestroy } from 'svelte';
  import { Chart } from 'chart.js/auto';

  export let labels = [];
  export let datasets = [];
  export let title = '';
  export let xLabel = '';
  export let yLabel = '';
  export let aspectRatio = 1.4;
  export let yMin = undefined;
  export let yMax = undefined;

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
      tension: 0.3,
      pointRadius: 3,
      pointHoverRadius: 6,
      borderWidth: ds.borderWidth ?? 2.5,
      fill: false,
    }));

    chart = new Chart(canvas, {
      type: 'line',
      data: { labels, datasets: processedDatasets },
      options: {
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
            padding: { bottom: 12 },
          },
          legend: {
            labels: {
              color: c.text,
              usePointStyle: true,
              pointStyle: 'line',
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
          },
        },
        scales: {
          x: {
            title: { display: !!xLabel, text: xLabel, color: c.text, font: { size: 12, family: 'Inter, sans-serif' } },
            ticks: { color: c.text, font: { size: 11, family: 'Inter, sans-serif' } },
            grid: { color: c.grid, drawBorder: false },
            border: { display: false },
          },
          y: {
            min: yMin,
            max: yMax,
            title: { display: !!yLabel, text: yLabel, color: c.text, font: { size: 12, family: 'Inter, sans-serif' } },
            ticks: { color: c.text, font: { size: 11, family: 'Inter, sans-serif' } },
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
