<template>
  <div class="form__field-container">
    <label v-if="label" :for="id" class="form__field-label form__field-label--upper">
      {{ label }}
    </label>
    <label
      :for="id"
      :class="{
        'form__field': true,
        'form__field--no-underline': true,
        'form__field--clickable': true,
        'form__field--has-value': true,
        'form__field--focused': isFocused,
        'form__field--has-error': !!error,
        'form__field--readonly': readonly,
      }"
      v-for="(file, index) in filesList"
      :key="index"
    >
      <div class="form__field-file-container">
        <div class="form__field-file-placeholder"></div>
        <div class="form__field-file-preview"></div>
      </div>
      <div class="form__field-file-preview">
          <img v-if="file && (file.isImage || isImage(file.url))" class="form__field-file-preview-image" :src="file.url" alt="" />
          <div v-else-if="file">
            <div class="fa-solid fa-file-arrow-down"></div>
            <div>.{{ getExtension(file.url) }}</div>
          </div>
      </div>
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
import uniqid from 'uniqid'
import Field from './Field.vue'
import FieldError from './FieldError.vue'

const IMAGES_EXTENSIONS = ['png', 'jpg', 'gif', 'tiff', 'svg']

export default {
  name: 'FileUploadField',
  components: {
    'field-error': FieldError,
  },
  extends: Field,
  props: {
    value: [Array, String],
    change: { type: Function, default: null },
    type: { type: String, default: null },
    withPreview: { type: Boolean, default: true },
    multiple: { type: Boolean, default: false },
  },
  data() {
    return {
      changed: false,
      isFocused: false,
      fieldValue: this.value,
      files: [],
    }
  },
  created() {
    if (this.value) {
      if (typeof this.value === 'string') {
        this.files.push({ id: uniqid(), url: this.value })
      } else {
        this.value.forEach(url => this.files.push({ id: uniqid(), url }))
      }
    }
  },
  computed: {
    hasUploadPlaceholder() {
      return this.multiple || this.files.length === 0
    },
    filesList() {
      const files = [...this.files].reverse()
      if (this.hasUploadPlaceholder) {
        files.splice(0, 0, null)
      }
      return files
    },
  },
  watch: {
    value(value) {
      if (!this.changed) {
        this.fieldValue = value
      }
    },
  },
  methods: {
    getExtension(name) {
      return name.split('.').pop().toLowerCase()
    },
    isImage(name) {
      return IMAGES_EXTENSIONS.includes(this.getExtension(name))
    },
    addNewFile(id, url, isImage = false) {
      const file = { id, url, isImage }
      this.files = this.multiple ? [...this.files, file] : [file]
    },
    onDelete(e, index) {
      this.files.splice(index, 1)
    },
    onChange(e) {
      [...e.target.files].forEach((file) => {
        const id = uniqid()
        if (this.isImage(file.name)) {
          const reader = new FileReader()
          reader.onload = (e) => {
            this.addNewFile(id, e.target.result, true)
          }
          reader.readAsDataURL(file)
        } else {
          this.addNewFile(id, file.name)
        }
      })
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
