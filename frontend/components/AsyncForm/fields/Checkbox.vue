<template>
  <div>
    <input
      :id="id"
      v-model="fieldValue"
      v-bind="$attrs"
      v-on="$listeners"
      :name="name"
      :disabled="readonly"
      type="checkbox"
      class="form__field--invisible"
      @change="onChange"
    />
    <div
      :class="{
        'form__field-checkbox': true,
        'form__field-checkbox--checked': !!fieldValue,
        'form__field-checkbox--has-error': !!error,
        'form__field-checkbox--readonly': readonly,
      }"
      @click="toggle"
    >
    </div>
    <label v-if="label" :for="id" class="form__field-label--inline">{{ label }}</label>
    <field-error v-if="error" :text="error" />
  </div>
</template>

<script>
import Field from './Field.vue'
import FieldError from './FieldError.vue'

export default {
  name: 'CheckboxField',
  components: {
    'field-error': FieldError,
  },
  extends: Field,
  props: {
    value: { type: Boolean, default: false },
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
    toggle() {
      if (this.readonly) { return }

      this.fieldValue = !this.fieldValue
      this.onChange()
    },
    onChange() {
      this.changed = true
      this.error = null
    },
  },
}
</script>
