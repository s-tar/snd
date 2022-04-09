<template>
  <div class="card card--elastic">
    <div class="card__body">
      <AsyncForm
        v-slot="form"
        action="/persons/save"
        json
        method="post"
        class="form"
        :on-success="onSuccess"
        :process-data="processData"
      >
        <div class="form__row">
          <div class="form__col">
            <FileUploadField id="photo" name="photo" label="Photo" />
          </div>
          <div class="form__col">
            <div class="form__row">
              <div class="form__col">
                <InputField id="last_name" type="text" name="last_name" label="Last name" :value="person.last_name" />
              </div>
              <div class="form__col">
                <InputField id="first_name" type="text" name="first_name" label="First name" :value="person.first_name" />
              </div>
              <div class="form__col">
                <InputField id="middle_name" type="text" name="middle_name" label="Middle name" :value="person.middle_name" />
              </div>
            </div>
          </div>
        </div>
        <div class="form__row form__row--align-right">
          <nuxt-link :to="`/`" class="button button--danger">Cancel</nuxt-link>
          <Submit type="submit" class="button button--success" :processing="form.processing">{{ id ? 'Save' : 'Add' }}</Submit>
        </div>
      </AsyncForm>
    </div>
  </div>
</template>

<script>
import AsyncForm from '~/components/AsyncForm'
import InputField from '~/components/AsyncForm/fields/Input'
import FileUploadField from '~/components/AsyncForm/fields/FileUpload'
import Submit from '~/components/AsyncForm/fields/Submit'

export default {
  name: 'PersonForm',
  components: {
    AsyncForm,
    InputField,
    FileUploadField,
    Submit,
  },
  props: {
    id: { type: String, default: '' },
    person: { type: Object, default: () => {} },
  },
  data() {
    return {}
  },
  methods: {

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
