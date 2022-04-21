<template>
  <div v-if="values.length" class="person-card__frame-field">
    <div v-if="name" class="person-card__frame-field-name">
      <slot name="name">{{ name }}</slot>:
    </div>
    <div class="person-card__frame-field-value">
      <slot name="value">
        <div v-for="(val, i) in values" :key="i">{{ val }}</div>
      </slot>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    name: { type: String, required: true },
    value: { type: [String, Number, Array, Object], default: null },
  },
  computed: {
    values() {
      const values = Array.isArray(this.value) ? this.value : [this.value]
      return values.filter(val => val != null)
    },
  },
}
</script>
