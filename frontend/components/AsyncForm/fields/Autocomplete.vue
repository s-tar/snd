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
      <input type="hidden" :name="name" :value="selectedValue" />
      <input
        :id="id"
        ref="field"
        v-model="fieldValue"
        :disabled="readonly"
        :type="type"
        v-bind="$attrs"
        :class="{
          'form__field': true,
          'form__field--wrapped': true,
          'form__field--has-value': !!fieldValue,
          'form__field--focused': isFocused,
          'form__field--has-error': !!error,
          'form__field--readonly': readonly,
          ...fieldClass,
        }"
        v-on="$listeners"
        @input="onChange"
        @focus="onFocus"
        @blur="onBlur"
      />
      <div
        v-if="isFocused"
        ref="list"
        :class="{
          'form__field-autocomplete-options': true,
          'form__field-autocomplete-options--upper': isUpper
        }"
      >
        <div
          v-for="(value, key) of options"
          :key="key"
          :data-key="key"
          class="form__field-autocomplete-option"
          @mousedown.self="onSelectValue(key, value)"
        >
          {{ value }}
        </div>
      </div>
    </div>
    <field-error v-if="error" :text="error" />
  </div>
</template>

<script>
import Field from './Field.vue'
import FieldError from './FieldError.vue'

export default {
  components: {
    'field-error': FieldError,
  },
  extends: Field,
  props: {
    items: { type: [Function, Object], required: true },
    term: { type: String, default: null },
  },
  data() {
    return {
      changed: false,
      isFocused: false,
      fieldValue: this.term,
      selectedValue: this.value,
      isUpper: false,
      options: {},
      searchTimer: null,
    }
  },
  watch: {
    isFocused(value) {
      if (value) {
        this.isUpper = false
        this.$nextTick(() => {
          const rect = this.$refs.list.getBoundingClientRect()
          this.isUpper = window.innerHeight < rect.bottom
        })
      }
    },
    selectedValue(value) {
      if (this.$listeners.update) {
        this.$listeners.update(this.name, value, null)
      }
    },
    value(value) {
      if (!this.changed) {
        this.fieldValue = value
      }
    },
  },
  methods: {
    updateOptionsPosition() {
      this.isUpper = false
      this.$nextTick(() => {
        if (this.$refs.list) {
          const rect = this.$refs.list.getBoundingClientRect()
          this.isUpper = window.innerHeight < rect.bottom
        }
      })
    },
    async refreshItems() {
      if (typeof this.items === 'function') {
        this.options = await this.items(this.fieldValue)
      } else {
        this.options = this.items
      }
      this.updateOptionsPosition()
    },
    async onSelectValue(value, term) {
      this.selectedValue = value
      this.fieldValue = term
      this.isFocused = false
      await this.refreshItems()
    },
    onChange(e) {
      this.changed = true
      this.error = null
      this.selectedValue = null
      if (this.searchTimer) {
        clearTimeout(this.searchTimer)
      }
      this.searchTimer = setTimeout(async() => await this.refreshItems(), 500)
    },
    onFocus(e) {
      this.isFocused = true
      this.updateOptionsPosition()
    },
    onBlur() {
      this.isFocused = false
    },
  },
}
</script>
