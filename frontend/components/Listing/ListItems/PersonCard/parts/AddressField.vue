
<template>
  <Field :name="name" :value="value">
    <template #value>
      <div v-for="(value, i) in values" :key="i">
        <i class="fa-solid fa-location-dot"></i> {{ value }}
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
}
</script>
