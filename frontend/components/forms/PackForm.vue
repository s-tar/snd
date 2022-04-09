<template>
  <div class="card card--elastic">
    <div class="card__body">
      <AsyncForm
        v-slot="form"
        :action="`/project/${projectCode}/category/${categoryCode}/pack/new`"
        method="post"
        class="form"
        :on-success="onSuccess"
        :process-data="processData"
      >
        <div class="form__row">
          <SelectField id="platform" name="platform" :value="platform || 'Android'" label="Platform">
            <option v-for="(name, key) in platforms" :key="key" :value="key">{{ name }}</option>
          </SelectField>
        </div>
        <div class="form__row">
          <TextAreaField id="description" name="description" :value="description" label="Description" />
        </div>
        <div class="form__row">
          <FileUploadField id="pack" ref="pack" name="pack" label="Pack.json" :change="onPackChange" />
        </div>
        <div class="form__row">
          <FileUploadField id="bundles_zip" name="bundles_zip" label="Bundles.zip" :change="onBundlesZipChange" />
        </div>
        <div class="form__row">
          <CheckboxField id="active" name="active" :value="false" label="Active" />
        </div>
        <div class="form__row form__row--align-right">
          <nuxt-link :to="`/project/${projectCode}/category/${categoryCode}`" class="button button--danger">Cancel</nuxt-link>
          <Submit type="submit" class="button button--success" :processing="form.processing">Create</Submit>
        </div>
      </AsyncForm>
    </div>
  </div>
</template>

<script>
import AsyncForm from '~/components/AsyncForm'
import TextAreaField from '~/components/AsyncForm/fields/Textarea'
import SelectField from '~/components/AsyncForm/fields/Select'
import FileUploadField from '~/components/AsyncForm/fields/FileUpload'
import CheckboxField from '~/components/AsyncForm/fields/Checkbox'
import Submit from '~/components/AsyncForm/fields/Submit'

export default {
  name: 'PackForm',
  components: {
    AsyncForm,
    TextAreaField,
    SelectField,
    FileUploadField,
    CheckboxField,
    Submit,
  },
  props: {
    projectCode: { type: String, required: true },
    categoryCode: { type: String, required: true },
    description: { type: String, default: '' },
    platform: { type: String, default: '' },
    platforms: { type: Object, required: true },
  },
  data() {
    return {
      bundles: [],
      bundlesZip: null,
    }
  },
  methods: {
    onBundlesZipChange(e) {
      this.bundlesZip = e.target.files[0]
    },
    onPackChange(e) {
      const file = e.target.files[0]
      if (!file) { return }

      const reader = new FileReader()
      reader.onload = (e) => {
        try {
          this.bundles = JSON.parse(e.target.result).bundles
        } catch (exc) {
          this.$refs.pack.$emit('errors', { pack: 'Bad pack json file.' })
        }
      }
      reader.readAsText(file)
    },
    processData(e) {
      if (!this.bundles || this.bundles.length === 0) {
        this.$refs.pack.$emit('errors', { pack: 'Bundles not found.' })
        return false
      }

      const form = new FormData(e.target)
      form.delete('pack')
      form.delete('bundles_zip')
      const dataJson = Object.fromEntries(form)
      dataJson.bundles = this.bundles

      const finalForm = new FormData()
      finalForm.append('data', JSON.stringify(dataJson))
      if (this.bundlesZip) {
        finalForm.append('bundles_zip', this.bundlesZip)
      }
      return finalForm
    },
    onSuccess() {
      this.$router.push(`/project/${this.projectCode}/category/${this.categoryCode}`)
    },
  },
}
</script>
