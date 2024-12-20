<script>
  import MoonIcon from "./icons/MoonIcon.svelte";
  import SunIcon from "./icons/SunIcon.svelte";

  let theme;

  // This ensures the code runs only in the browser
  if (typeof window !== "undefined") {
    theme = localStorage.getItem("theme") || "light";

    // Set initial theme based on localStorage
    if (theme === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }

  function handleClick() {
    theme = theme === "light" ? "dark" : "light";

    if (theme === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }

    localStorage.setItem("theme", theme);
  }
</script>

<button
  on:click={handleClick}
  class="hover:bg-slate-100 py-2 px-3 rounded-lg dark:hover:bg-neutral-800"
>
  {#if theme === "light"}
    <MoonIcon />
  {:else}
    <SunIcon />
  {/if}
</button>
