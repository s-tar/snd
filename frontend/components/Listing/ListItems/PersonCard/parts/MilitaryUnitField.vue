<template>
  <Field :name="name" :value="value">
    <template #value>
      <div>
        <div v-if="value.name">{{ value.name }}</div>
        <div v-if="value.number">в/ч {{ value.number }}</div>
        <div v-if="value.address">
          <i class="fa-solid fa-location-dot"></i> {{ value.address }}
        </div>
      </div>
    </template>
  </Field>
</template>

<script>
import Field from './Field'

export default {
  components: {
    Field,
  },
  extends: Field,
  props: {
    value: { type: Object, default: null },
  },
  values() {
    return Object.values(this.value || {})
  },
}
</script>
