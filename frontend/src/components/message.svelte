<script lang="ts">
  /**
   *  Message component to show messages to the user in the top right.
   */

  import { onMount, afterUpdate } from "svelte";
  import { fade } from "svelte/transition";

  import { messages } from "../lib/stores";

  export let message = "";
  export let id: number;

  let visible = true;

  /**
   * Deletes a message from the collection of messages.
   * @returns {void}
   */
  const deleteMessage = () => {
    messages.update((e) => e.filter((msg) => msg.id !== id));
  };

  /*
   * Contains logic that runs at initialisation, as soon as the component has been mounted.
   * In this component it sets a timer for how long a message is displayed.
   */
  onMount(() => {
    setTimeout(() => {
      visible = false;
    }, 5000);
  });

  /*
    Contains logic that runs immediately after the component has been updated.
    In this component it deletes a displayed message after the timer for that message has finished counting.
   */
  afterUpdate(() => {
    if (!visible) {
      deleteMessage();
    }
  });
</script>

{#if visible}
  <div class="z-50 flex flex-col items-end transition-colors duration-200 hover:brightness-110">
    <button
      class="relative mr-2 mt-2 w-80 cursor-pointer rounded bg-les-red p-4 shadow transition"
      on:click={deleteMessage}
      on:keydown
      transition:fade>
      <button class="absolute right-2 top-2">
        <svg
          class="h-4 w-4 fill-current text-white transition-colors duration-200 hover:text-les-highlight"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24">
          <path
            d="M12 10.586l4.95-4.95a1 1 0 111.414 1.414L13.414 12l4.95 4.95a1 1 0 11-1.414 1.414L12 13.414l-4.95 4.95a1 1 0 11-1.414-1.414L10.586 12 5.636 7.05a1 1 0 111.414-1.414L12 10.586z" />
        </svg>
      </button>
      <p>{@html message}</p>
      <div
        class="progress-bar mt-2 h-2 rounded bg-les-red-dark"
        style={`animation-duration: 5000ms`} />
    </button>
  </div>
{/if}

<style>
  .progress-bar {
    animation-name: progress;
    animation-timing-function: linear;
    animation-fill-mode: forwards;
  }

  @keyframes progress {
    from {
      width: 100%;
    }
    to {
      width: 0%;
    }
  }
</style>
