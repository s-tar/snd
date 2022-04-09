<template>
  <div class="form__error">{{ text }}</div>
</template>

<script>
export default {
  name: 'FieldError',
  props: {
    text: { type: String, required: true },
  },
}
</script>
