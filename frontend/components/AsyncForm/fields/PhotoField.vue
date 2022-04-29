<template>
  <div class="form__field-container">
    <label v-if="label" :for="id" class="form__field-label form__field-label--upper">
      {{ label }}
    </label>
    <label
      :for="id"
      :class="{
        'form__field': true,
        'form__field--photo': true,
        'form__field--no-underline': true,
        'form__field--clickable': true,
        'form__field--has-value': true,
        'form__field--has-error': !!error,
        'form__field--readonly': readonly,
      }"
    >
      <div class="form__field-photo">
        <div v-if="!value">
          <i class="fa-solid fa-file-arrow-down"></i>
        </div>
        <img v-else class="form__field-photo-image" :src="value" alt="" />
      </div>
    </label>
    <div v-if="showPopup" class="form__field-photo-popup">
      <div class="form__field-photo-window">
        <cropper
          class="form__field-photo-popup-image"
          :src="fileData"
          :stencil-props="{ aspectRatio: 1 }"
          @change="onCrop"
        />
        <div class="form__field-photo-buttons">
          <button class="button button--danger" @click.prevent="onCropCancel">Отмена</button>
          <button class="button button--success" @click.prevent="onCropApply">Применить</button>
        </div>
      </div>
    </div>
    <input
      :id="id"
      ref="file"
      v-bind="$attrs"
      :name="name"
      :disabled="readonly"
      type="file"
      class="form__field--file-input"
      @change="onChange"
    />
    <field-error v-if="error" :text="error" />
  </div>
</template>

<script>
import Field from './Field'
import FieldError from './FieldError.vue'

export default {
  components: {
    'field-error': FieldError,
  },
  extends: Field,
  props: {
    name: { type: String, required: true },
    value: { type: String, default: null },
    change: { type: Function, default: null },
  },
  data() {
    return {
      file: null,
      fileData: null,
      showPopup: false,
      coordinates: null,
      canvas: null,
    }
  },
  methods: {
    isImage(file) {
      return file && file.type.split('/')[0] === 'image'
    },
    onCrop({ coordinates, canvas }) {
      this.coordinates = coordinates
      this.canvas = canvas
    },
    onChange(e) {
      this.error = null
      this.file = e.target.files[0]
      if (!this.isImage(this.file)) {
        this.error = 'Файл не является картинкой'
        return
      }
      const reader = new FileReader()
      reader.onload = (e) => {
        this.onFileLoaded(e.target.result)
      }
      reader.readAsDataURL(this.file)
    },
    onFileLoaded(fileData) {
      this.fileData = fileData
      this.showPopup = true
    },
    onCropApply() {
      if (this.$listeners.change) {
        this.$listeners.change(this.file, this.coordinates, this.canvas)
      }
      if (this.$listeners.update) {
        this.$listeners.update(this.name, this.coordinates, this.$refs.file.files[0])
      }

      this.showPopup = false
    },
    onCropCancel() {
      this.showPopup = false
      this.file = null
      this.fileData = null
      this.$refs.file.value = ''
      this.coordinates = null
    },
    processData(e) {
      const data = new FormData(e.target)
      return data
    },
  },
}
</script>
