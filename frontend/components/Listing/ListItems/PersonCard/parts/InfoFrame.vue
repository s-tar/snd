<template>
  <div v-if="isVisible" class="person-card__frame">
    <div v-if="title" class="person-card__frame-title">{{ title }}</div>
    <div class="person-card__frame-body">
      <div :class="{
        'person-card__frame-fields': true,
        'person-card__frame-fields--table': type === 'table'
      }">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: { type: String },
    type: { type: String },
  },
  computed: {
    isVisible() {
      return !!this.$slots.default
    },
  },
}
</script>
