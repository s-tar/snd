<template>
  <Field :name="name" :value="value">
    <template #value>
      <a v-for="(value, i) in values" :key="i" :href="value" :target="target" class="link">
        {{ value }}
      </a>
    </template>
  </Field>
</template>

<script>
import Field from './Field'

export default {
  props: {
    target: { type: String, default: null },
  },
  components: {
    Field,
  },
  extends: Field,
}
</script>
