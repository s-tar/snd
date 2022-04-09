<template>
  <button>
    <span v-if="processing" class="button__processing">
      <span class="fas fa-spinner fa-pulse"></span>
    </span>
    <span :class="{'button__text': true, 'button__text--hidden': processing}">
      <slot></slot>
    </span>
  </button>
</template>

<script>
export default {
  name: 'Submit',
  props: {
    processing: Boolean,
  },
}
</script>
