<template>
  <div>
    <label v-if="label" :for="id" class="form__field-label form__field-label--upper">
      {{ label }}
    </label>
    <label
      :for="id"
      :class="{
        'form__field': true,
        'form__field--clickable': true,
        'form__field--has-value': !!fieldValue,
        'form__field--focused': isFocused,
        'form__field--has-error': !!error,
        'form__field--readonly': readonly,
      }"
    >
      <i class="fas fa-file-upload"></i>
      <span v-if="fieldValue">{{ fieldValue }}</span>
      <span v-else>Choose a file...</span>
    </label>
    <input
      :id="id"
      v-bind="$attrs"
      :name="name"
      :disabled="readonly"
      type="file"
      class="form__field--file-input"
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
  name: 'FileUploadField',
  components: {
    'field-error': FieldError,
  },
  extends: Field,
  props: {
    change: { type: Function, default: null },
  },
  data() {
    return {
      changed: false,
      isFocused: false,
      fieldValue: this.value,
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
      this.fieldValue = e.target.value.split(/[/\\]+/).slice(-1)[0]
      this.changed = true
      this.error = null
      if (this.change) { this.change(e) }
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
