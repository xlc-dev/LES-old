<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import Chart from 'chart.js/auto';
  import { efficiencyresultstore } from '../lib/stores';

  let chartContainer;
  let chart;

  // Subscribe to the store
  let efficiencyResults = [];
  const unsubscribe = efficiencyresultstore.subscribe(data => {
    efficiencyResults = data;
    updateChart();
  });

  function updateChart() {
    if (chart) {
      chart.data.datasets[0].data = efficiencyResults.map(r => r.solarEnergyIndividual);
      chart.data.datasets[1].data = efficiencyResults.map(r => r.solarEnergyTotal);
      chart.data.datasets[2].data = efficiencyResults.map(r => r.internalBoughtEnergyPrice);
      chart.data.datasets[3].data = efficiencyResults.map(r => r.totalAmountSaved);
      chart.update();
    }
  }

  onMount(() => {
    chart = new Chart(chartContainer.getContext('2d'), {
      type: 'bar', // or 'line', 'pie', etc.
      data: {
        labels: efficiencyResults.map((_, index) => `Data ${index + 1}`),
        datasets: [
          {
            label: '% Solar Energy (Individual)',
            data: [], // Data will be set via updateChart()
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
          },
          {
            label: '% Solar Energy (Total)',
            data: [],
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
          },
          {
            label: 'Internal Bought Energy Price',
            data: [],
            backgroundColor: 'rgba(255, 206, 86, 0.2)',
          },
          {
            label: 'Total Amount Saved',
            data: [],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
          }
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  });

  onDestroy(() => {
    if (chart) {
      chart.destroy();
    }
    unsubscribe();
  });
</script>

<canvas bind:this={chartContainer}></canvas>
