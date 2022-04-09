<template>
  <div>
    <label
      v-if="label"
      :for="id"
      :class="{
        'form__field-label': true,
        'form__field-label--upper': true,
      }"
    >
      {{ label }}
    </label>
    <select
      :id="id"
      v-model="fieldValue"
      v-bind="$attrs"
      v-on="$listeners"
      :name="name"
      :disabled="readonly"
      :class="{
        'form__field': true,
        'form__field--has-value': !!fieldValue,
        'form__field--focused': isFocused,
        'form__field--has-error': !!error,
        'form__field--readonly': readonly,
      }"
      @change="onChange"
      @focus="onFocus"
      @blur="onBlur"
    >
      <slot></slot>
    </select>
    <field-error v-if="error" :text="error" />
  </div>
</template>

<script>
import Field from './Field.vue'
import FieldError from './FieldError.vue'

export default {
  name: 'InputField',
  components: {
    'field-error': FieldError,
  },
  extends: Field,
  data() {
    return {
      changed: false,
      isFocused: false,
      fieldValue: this.value,
    }
  },
  watch: {
    value(value) {
      this.fieldValue = value
    },
  },
  methods: {
    onChange(e) {
      this.changed = true
      this.error = null
      if (this.$listeners.change) { this.$listeners.change(e) }
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
