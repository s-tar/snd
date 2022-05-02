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
    <datepicker
      :id="id"
      ref="field"
      v-model="fieldValue"
      :language="dateLocale"
      format="dd.MM.yyyy"
      monday-first
      calendar-button-icon="fa-solid fa-calendar-days"
      v-bind="$attrs"
      :disabled="readonly"
      :input-class="{
        'form__field': true,
        'form__field--has-value': !!fieldValue,
        'form__field--focused': isFocused,
        'form__field--has-error': !!error,
        'form__field--readonly': readonly,
        ...fieldClass,
      }"
      v-on="$listeners"
      @selected="onSelect"
      @focus="onFocus"
      @blur="onBlur"
    />
    <field-error v-if="error" :text="error" />
  </div>
</template>

<script>
import { ru } from 'vuejs-datepicker/dist/locale'

import Field from './Field.vue'
import FieldError from './FieldError.vue'

export default {
  components: {
    'field-error': FieldError,
  },
  extends: Field,
  data() {
    return {
      dateLocale: ru,
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
    onSelect(date) {
      this.changed = true
      this.error = null
      if (this.$listeners.update) {
        try {
          date = date.toISOString().split('T')[0]
          this.$listeners.update(this.name, date, null)
        } catch (e) {
          this.fieldValue = ''
        }
      }
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
