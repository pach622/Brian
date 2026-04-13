<script>
  import { onMount, onDestroy } from 'svelte';
  import { Chart } from 'chart.js/auto';

  export let labels = [];
  export let data = [];
  export let backgroundColors = [];
  export let title = '';
  export let aspectRatio = 1.4;

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
      tooltipBg: d ? '#1f2937' : '#ffffff',
      tooltipBorder: d ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
    };
  }

  function buildChart() {
    if (chart) chart.destroy();
    const c = colors();

    chart = new Chart(canvas, {
      type: 'doughnut',
      data: {
        labels,
        datasets: [{
          data,
          backgroundColor: backgroundColors,
          borderWidth: 2,
          borderColor: isDark() ? '#070919' : '#ffffff',
          hoverOffset: 8,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio,
        plugins: {
          title: {
            display: !!title,
            text: title,
            color: c.text,
            font: { size: 14, weight: '600', family: 'Inter, sans-serif' },
            padding: { bottom: 12 },
          },
          legend: {
            position: 'bottom',
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
            callbacks: {
              label: (ctx) => {
                const total = ctx.dataset.data.reduce((a, b) => a + b, 0);
                const pct = ((ctx.parsed / total) * 100).toFixed(1);
                return `${ctx.label}: ${ctx.parsed.toLocaleString()} (${pct}%)`;
              },
            },
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
