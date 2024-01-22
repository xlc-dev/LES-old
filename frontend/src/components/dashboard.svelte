<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import Chart from "chart.js/auto";
  import { efficiencyresultstore, runtime, stepperData } from "../lib/stores";

  let chartContainers = [];
  let charts = [];
  const maxDataPoints = 51;

  $: if ($efficiencyresultstore.length > 0) {
    updateCharts($efficiencyresultstore);
  }

  $: numberOfHouseholds = $stepperData.households.length;
  $: costModelAlgorithm = $stepperData.costmodel.algorithm;
  $: costModelFixedPriceRatio = $stepperData.costmodel.fixed_price_ratio;
  $: costModelPriceNetworkBuyConsumer = $stepperData.costmodel.price_network_buy_consumer;
  $: costModelPriceNetworkSellConsumer = $stepperData.costmodel.price_network_sell_consumer;
  $: twinWorldEnergyUsageFactor = $stepperData.twinworld.energy_usage_factor;
  $: twinWorldSolarPanelsFactor = $stepperData.twinworld.solar_panels_factor;
  $: algorithmMaxTemperature = $stepperData.algorithm.max_temperature;

  onMount(() => {
    initializeCharts();
    updateCharts($efficiencyresultstore);
  });

  onDestroy(() => {
    charts.forEach((chart) => chart?.destroy());
  });

  function initializeCharts() {
    chartContainers.forEach((container, index) => {
      charts[index] = new Chart(container.getContext("2d"), {
        type: "line",
        data: {
          labels: [],
          datasets: [
            {
              label: getChartLabel(index),
              data: [],
              backgroundColor: getChartFillColor(index),
              borderColor: getChartColor(index),
              fill: true,
            },
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
  }

  function updateCharts(data) {
    console.log("Updating charts with mapped data:", data);
    charts.forEach((chart, index) => {
      const latestData = data.slice(-maxDataPoints);

      chart.data.labels = latestData.map((_, i) => `Day ${data.length - maxDataPoints + i + 1}`);
      chart.data.datasets[0].data = latestData.map((item) => {
        switch (index) {
          case 0:
            return item.solarEnergyIndividual;
          case 1:
            return item.solarEnergyTotal;
          case 2:
            return item.internalBoughtEnergyPrice;
          case 3:
            return item.totalAmountSaved;
        }
      });
      console.log(`Chart ${index} data:`, chart.data.datasets[0].data);
      chart.update();
    });
  }

  function getChartLabel(index) {
    switch (index) {
      case 0:
        return "% Solar Energy (Individual)";
      case 1:
        return "% Solar Energy (Total)";
      case 2:
        return "Internal Bought Energy Price";
      case 3:
        return "Total Amount Saved";
    }
  }

  function getChartFillColor(index) {
    const fillColors = [
      "rgba(255, 0, 0, 0.2)",
      "rgba(255, 255, 0, 0.2)",
      "rgba(0, 0, 255, 0.2)",
      "rgba(0, 128, 0, 0.2)",
    ];
    return fillColors[index] || "rgba(0, 0, 0, 0.2)";
  }

  function getChartColor(index) {
    const colors = ["#f23f44", "#cbba07", "#1565c0", "#008000"];
    return colors[index] || "#000000";
  }
</script>

<div class="max-w-5xl mx-auto pt-8">
  <div
    class="mt-8 bg-white rounded-lg p-4 mb-8 border-4 border-gray-400 shadow grid grid-cols-2 gap-4">
    {#each Array(4) as _, index (index)}
      <div class="chart-container">
        <canvas bind:this={chartContainers[index]}></canvas>
      </div>
    {/each}
  </div>
  <div
    class="mt-8 bg-white rounded-lg p-4 mb-8 border-4 border-gray-400 shadow grid grid-cols-2 gap-4">
    <p>Number of Households: {numberOfHouseholds}</p>
    <p>Cost model algorithm: {costModelAlgorithm}</p>
    <p>Cost model fixed price ratio: {costModelFixedPriceRatio}</p>
    <p>Cost model price network buy consumer: {costModelPriceNetworkBuyConsumer}</p>
    <p>Cost model price network sell consumer: {costModelPriceNetworkSellConsumer}</p>
    <p>Twin world energy usage factor: {twinWorldEnergyUsageFactor}</p>
    <p>Twin world solar panels factor: {twinWorldSolarPanelsFactor}</p>
    <p>Algorithm max temperature: {algorithmMaxTemperature}</p>
    <p>Runtime: {$runtime} seconds</p>
  </div>
</div>
