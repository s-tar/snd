<template>
  <div class="form__field-container">
    <label
      v-if="label"
      :for="id"
      :class="{
        'form__field-label': true,
        'form__field-label--upper': !!fieldValue || isFocused,
      }"
    >
      {{ label }}
    </label>
    <div class="form__field-wrapper">
      <textarea
        :id="id"
        v-model="fieldValue"
        v-bind="$attrs"
        v-on="$listeners"
        :name="name"
        :disabled="readonly"
        :class="{
          'form__field': true,
          'form__field--textarea': true,
          'form__field--has-value': !!fieldValue,
          'form__field--focused': isFocused,
          'form__field--has-error': !!error,
          'form__field--readonly': readonly,
        }"
        @change="onChange"
        @keypress="onChange"
        @focus="onFocus"
        @blur="onBlur"
      ></textarea>
      <div :class="{'form__field-placeholder': true, 'form__field-placeholder--readonly': readonly}">{{ fieldValue + '\n' }}</div>
    </div>
    <field-error v-if="error" :text="error" />
  </div>
</template>

<script>
import Field from './Field.vue'
import FieldError from './FieldError.vue'

export default {
  name: 'TextareaField',
  components: {
    'field-error': FieldError,
  },
  extends: Field,
  data() {
    return {
      changed: false,
      fieldValue: this.value || (this.$slots.default ? this.$slots.default[0].text : ''),
      isFocused: false,
    }
  },
  watch: {
    value(value) {
      if (!this.changed) {
        this.fieldValue = value
      }
    },
  },
  methods: {
    onChange(e) {
      this.changed = true
      this.$forceUpdate()
      this.error = null
    },
    onFocus() {
      this.isFocused = true
    },
    onBlur() {
      this.isFocused = false
    },
  },
}
</script>
