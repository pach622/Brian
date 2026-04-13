<script>
  let isOpen = false;

  function toggle() {
    isOpen = !isOpen;
  }

  function close() {
    isOpen = false;
  }
</script>

<div class="md:hidden">
  <button
    on:click={toggle}
    class="hover:bg-slate-100 py-2 px-3 rounded-lg dark:hover:bg-neutral-800"
    aria-label="Toggle menu"
  >
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      {#if isOpen}
        <line x1="18" y1="6" x2="6" y2="18" />
        <line x1="6" y1="6" x2="18" y2="18" />
      {:else}
        <line x1="3" y1="12" x2="21" y2="12" />
        <line x1="3" y1="6" x2="21" y2="6" />
        <line x1="3" y1="18" x2="21" y2="18" />
      {/if}
    </svg>
  </button>

  {#if isOpen}
    <div class="absolute top-16 left-0 right-0 bg-white dark:bg-primary-dark border-b border-gray-200 dark:border-neutral-800 shadow-lg z-50">
      <nav class="flex flex-col px-6 py-4 space-y-2">
        <a on:click={close} href="/" class="py-2 px-3 rounded-lg hover:bg-slate-100 dark:hover:bg-neutral-800 font-medium">Home</a>
        <a on:click={close} href="/caseStudies" class="py-2 px-3 rounded-lg hover:bg-slate-100 dark:hover:bg-neutral-800 font-medium">Projects</a>
        <a on:click={close} href="/workExperience" class="py-2 px-3 rounded-lg hover:bg-slate-100 dark:hover:bg-neutral-800 font-medium">Work</a>
        <a on:click={close} href="/aboutMe" class="py-2 px-3 rounded-lg hover:bg-slate-100 dark:hover:bg-neutral-800 font-medium">About</a>
      </nav>
    </div>
  {/if}
</div>
