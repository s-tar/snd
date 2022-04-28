<template>
  <div v-if="isVisible" class="info-frame">
    <div v-if="title" class="info-frame__title">{{ title }}</div>
    <div class="info-frame__body">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: { type: String },
  },
  computed: {
    isVisible() {
      return !!this.$slots.default
    },
  },
}
</script>
