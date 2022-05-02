<template>
  <Field :name="name" :value="value">
    <template #value>
      <a v-for="(value, i) in values" :key="i" :href="value" class="link">
        {{ value }}
      </a>
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
}
</script>
