<template>
  <Field :name="name" :value="value">
    <template #name>
      <span>
        <i v-if="name === 'ok'" class="fa-brands fa-odnoklassniki"></i>
        <i v-else-if="name === 'vk'" class="fa-brands fa-vk"></i>
        <i v-else-if="name === 'fb'" class="fa-brands fa-facebook"></i>
      </span>
    </template>
    <template #value>
      <div>
        <div v-for="(value, i) in values" :key="i">
          <a :href="value" target="_blank" class="link">{{ value }}</a>
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
}
</script>
