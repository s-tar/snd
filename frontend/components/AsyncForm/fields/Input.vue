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
    <input
      ref="field"
      :id="id"
      v-model="fieldValue"
      v-bind="$attrs"
      v-on="$listeners"
      :name="name"
      :disabled="readonly"
      :type="type"
      :class="{
        'form__field': true,
        'form__field--has-value': !!fieldValue,
        'form__field--focused': isFocused,
        'form__field--has-error': !!error,
        'form__field--readonly': readonly,
        ...fieldClass,
      }"
      @change="onChange"
      @focus="onFocus"
      @blur="onBlur"
    />
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
      autofilled: false,
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
      this.error = null
    },
    onFocus(e) {
      this.isFocused = true
    },
    onBlur() {
      this.isFocused = false
    },
  },
}
</script>
